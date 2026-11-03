#
# spec file for package deckifier (ogc-handheld)
#
# Sources: github.com/ocelado-linux/deckifier (fork of YugaLinux/deckifier
# with the Ocelado changes as commits; pinned in _service).
# Changes:
#  - no hard dependency on Steam Deck hardware support (jupiter-hw-support)
#  - autologin user is detected at runtime instead of hardcoded "deck"
#  - trup points to home:Luthenis:ogc-handheld
#  - SDDM instead of LightDM for Game Mode / Desktop Mode switching
#

%define TRUP_SOURCE /etc/trup/source.conf
%define TRUP_NAME   ogc-handheld
%define BRANCH      stable
%define REPO        home:Luthenis:ogc-handheld

Name:           deckifier
Version:        0
Release:        0
Summary:        Missing bits for gamescope-session
License:        MIT
URL:            https://github.com/ocelado-linux/deckifier
Source0:        %{name}-%{version}.tar.xz
Source1:        gamescope-powerbuttond.conf
Source2:        powerbuttond-gamescope.conf
BuildRequires:  polkit
# symlinks in /etc/skel point to steam.desktop: needed by the brp symlink check
BuildRequires:  steam
BuildRequires:  sudo
Requires:       gamescope-session-steam
Requires:       sddm-qt6
Requires:       dbus-1
Requires:       polkit
Requires:       steam
Requires:       steamos-powerbuttond
Requires:       sudo
Recommends:     (deckifier-session-kde or deckifier-session-gnome)
Conflicts:      gamescope-session-steam-generic
BuildArch:      noarch

%description
Missing bits for gamescope-session to run the Steam session
(Game Mode / Desktop switching, Steam updater integration, polkit rules).
Hardware-agnostic: Steam Deck specific support lives in separate packages.

%package steamos-helpers
Summary:        SteamOS polkit helpers for handhelds other than the Steam Deck
Requires:       deckifier
Requires:       polkit
Requires:       systemd
# on the Steam Deck the same helpers come from jupiter-hw-support
Conflicts:      jupiter-hw-support

%description steamos-helpers
Root helpers that the Steam client calls by fixed path
(/usr/bin/steamos-polkit-helpers/*): system update, update branch,
timezone, hostname, reboot, power off and display manager restart,
allowed through polkit for the active local session.

%prep
%autosetup -p1 -n %{name}-%{version}

%build

%install
cp -rv deckifier/usr %{buildroot}/usr
cp -rv deckifier/etc %{buildroot}/etc
cp -rv deckifier-steamos-helpers/usr %{buildroot}/
mkdir -p %{buildroot}/etc/sddm.conf.d
# power button in Game Mode: steamos-powerbuttond started with the session
install -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/user/gamescope-session-plus@.service.d/50-ogc-powerbuttond.conf
install -D -m 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/user/steamos-powerbuttond.service.d/50-ogc-gamescope.conf
# steam-browser registered Steam as the default web browser (http/https),
# so it showed up as "steam-browser" in the Plasma favorites: drop it
rm -f %{buildroot}/usr/share/applications/steam-browser.desktop
# fix /bin/env RPM dependencies
%{__sed} -i '1s|^#!/usr/bin/env xdg-open|#!/usr/bin/xdg-open|' %{buildroot}/usr/share/applications/*.desktop
# trup repository and branch
%{__sed} -i "s/^NAME=.*/NAME=%{TRUP_NAME}/" %{buildroot}%{TRUP_SOURCE}
%{__sed} -i "s/^REPO=.*/REPO=%{REPO}/" %{buildroot}%{TRUP_SOURCE}
%{__sed} -i "s/^BRANCH=.*/BRANCH=%{BRANCH}/" %{buildroot}%{TRUP_SOURCE}
%{__sed} -i "s/^OLD_REPO=.*/OLD_REPO=%{REPO}/" %{buildroot}%{TRUP_SOURCE}
%{__sed} -i "s/^OLD_BRANCH=.*/OLD_BRANCH=%{BRANCH}/" %{buildroot}%{TRUP_SOURCE}

# Steam shortcut on the desktop (no extest needed: Plasma 6 handles Steam
# Input emulation on Wayland by itself)
mkdir -p %{buildroot}/etc/skel/Desktop
# Steam autostart in Desktop Mode is system-wide now (deckifier-session-kde,
# /etc/xdg/autostart/steam-desktop-mode.desktop): drop the per-user link
rm -rf %{buildroot}/etc/skel/.config
ln -sf /usr/share/applications/steam.desktop %{buildroot}/etc/skel/Desktop/steam.desktop

%post
%systemd_post bluetooth-workaround.service
%systemd_post steamos-startup.service

%preun
%systemd_preun bluetooth-workaround.service
%systemd_preun steamos-startup.service

%postun
%systemd_postun_with_restart bluetooth-workaround.service
%systemd_postun steamos-startup.service

%files
%license LICENSE
%dir /etc/bluetooth
%config(noreplace) /etc/bluetooth/*
%dir /etc/dconf
%config(noreplace) /etc/dconf/*
%config(noreplace) /etc/xdg/*
%dir /etc/ogc-handheld
%config(noreplace) /etc/ogc-handheld/boot-session.conf
%dir /etc/trup
%config(noreplace) %{TRUP_SOURCE}
%config(noreplace) /etc/sudoers.d/*
%dir /etc/sddm.conf.d
%ghost %config(noreplace) /etc/sddm.conf.d/zz-steamos-autologin.conf
%dir /etc/skel/Desktop
/etc/skel/Desktop/*
/usr/lib/systemd/*
/usr/lib/udev/rules.d/30-steamdeck.rules
/usr/lib/udev/rules.d/31-handheld-backlight.rules
/usr/share/polkit-1/rules.d/*
/usr/share/polkit-1/actions/org.ogchandheld.session-select.policy
/usr/share/applications/*
/usr/share/icons/valve
/usr/share/color
/usr/bin/factory-reset
/usr/bin/steam-vr-launcher
/usr/bin/steamos-factory-reset-config
/usr/bin/steamos-select-branch
/usr/bin/steamos-session-select
/usr/bin/steamos-startup-gamescope
/usr/bin/steamos-update
/usr/bin/trup
%dir /usr/bin/steamos-polkit-helpers
/usr/bin/steamos-polkit-helpers/steamos-factory-reset
/usr/bin/steamos-polkit-helpers/steamos-set-autologin


%files steamos-helpers
/usr/bin/steamos-polkit-helpers/steamos-update
/usr/bin/steamos-polkit-helpers/steamos-select-branch
/usr/bin/steamos-polkit-helpers/steamos-set-timezone
/usr/bin/steamos-polkit-helpers/steamos-set-hostname
/usr/bin/steamos-polkit-helpers/steamos-reboot-now
/usr/bin/steamos-polkit-helpers/steamos-poweroff-now
/usr/bin/steamos-polkit-helpers/steamos-restart-sddm
/usr/share/polkit-1/actions/org.ogchandheld.steamos-helpers.policy

%changelog
