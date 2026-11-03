#
# spec file for package deckifier-session-kde (ogc-handheld)
#
# Built from the same deckifier sources (_multibuild flavor).
# One-shot Plasma session for Desktop Mode: switching back to Game Mode
# is restored on logout / reboot (SDDM autologin, see deckifier).
#

Name:           deckifier-session-kde
Version:        0
Release:        0
Summary:        KDE Plasma Desktop Mode session for deckifier
License:        MIT
URL:            https://github.com/ocelado-linux/deckifier
Source0:        deckifier-%{version}.tar.xz
Source1:        ocelado-steam-autostart.desktop
Source2:        steam-desktop-autostart
# on-screen keyboard on by default (handhelds have no physical keyboard)
Source3:        kwinrc
Requires:       deckifier
Requires:       plasma6-workspace
# on-screen keyboard for Desktop Mode (no physical keyboard on handhelds)
Requires:       plasma6-keyboard
Conflicts:      deckifier-session-gnome
# owned /etc/xdg/kwinrc before (dropped by ocelado-release)
Conflicts:      plasma6-branding-openSUSE
BuildArch:      noarch

%description
One-shot KDE Plasma (Wayland) session used by deckifier for Desktop Mode.

%prep
%autosetup -p1 -n deckifier-%{version}

%build

%install
cp -rv deckifier-session-kde/usr %{buildroot}/usr
cp -rv deckifier-session-kde/etc %{buildroot}/etc
# Steam starts in the background in Desktop Mode, like SteamOS
install -D -m 0644 %{SOURCE1} %{buildroot}/etc/xdg/autostart/ocelado-steam-autostart.desktop
install -D -m 0755 %{SOURCE2} %{buildroot}/usr/bin/steam-desktop-autostart
# Plasma on-screen keyboard enabled system-wide (users can turn it off in
# System Settings > Keyboard > Virtual Keyboard)
install -D -m 0644 %{SOURCE3} %{buildroot}/etc/xdg/kwinrc

%posttrans
# old name of the autostart entry (kept by the immutable /etc on updates)
rm -f /etc/xdg/autostart/steam-desktop-mode.desktop

%files
%dir /etc/trup
%config(noreplace) /etc/trup/session.conf
/usr/bin/plasma-session-oneshot
/usr/bin/steam-desktop-autostart
%dir /etc/xdg
%dir /etc/xdg/autostart
%config /etc/xdg/autostart/ocelado-steam-autostart.desktop
%config /etc/xdg/kwinrc
%dir /usr/share/wayland-sessions
/usr/share/wayland-sessions/plasmawayland-session-oneshot.desktop

%changelog
