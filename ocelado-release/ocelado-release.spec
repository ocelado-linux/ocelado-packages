#
# spec file for package ocelado-release
#
# Ocelado Linux: SteamOS-like openSUSE Tumbleweed for handhelds.
#
# Rebrands the os-release name on top of openSUSE-release instead of
# replacing it: ID, VERSION_ID (snapshot date) and the product files stay
# the ones from Tumbleweed, so zypper, transactional-update and the
# openSUSE tooling keep working unchanged.
#

Name:           ocelado-release
Version:        1.24
Release:        0
# Ocelado Linux release shown in os-release (IMAGE_VERSION)
%define ocelado_version 0.3
Summary:        Ocelado Linux branding: name, logo, wallpaper and GRUB entry
License:        MIT
URL:            https://build.opensuse.org/project/show/home:Luthenis:ogc-handheld
Source0:        ocelado-apply-branding
Source1:        ocelado-icons.tar.xz
Source2:        ocelado-wallpaper.tar.xz
Source3:        ocelado-plasma-defaults
Source4:        ocelado-plasma-defaults.desktop
Source5:        zram-generator.conf
# system setup formerly done by the KIWI config.sh (needed by Agama installs)
Source6:        ogc-handheld.repo
Source7:        80-ocelado.preset
Source8:        ocelado-setup-system
Source9:        ocelado-firstboot
Source10:       ocelado-firstboot.service
Source11:       81-ocelado-gamemode.preset
Source12:       81-ocelado-desktop.preset
Source13:       10-ocelado-desktop.conf
Source14:       ocelado-kernel-select
Source15:       ocelado-kernel-select.service
Source16:       ocelado-grub-default
Source17:       ocelado-kernel-flavor.service
Source18:       20-ocelado-greeter.conf
# signing key of the OBS project (repodata/repomd.xml.key of the repo)
Source19:       ocelado-repo.key
# GRUB theme: openSUSE theme with Ocelado logo and colors
Source20:       grub-theme.txt
Source21:       grub-logo.png
Source22:       grub-highlight_c.png
Source23:       ocelado-flathub.service
# gaming defaults: NTSYNC/BBR modules, max_map_count, BBR
Source24:       ocelado-gaming.modules
Source25:       90-ocelado-gaming.conf
# KDE "About this System": Ocelado logo, release and website
Source26:       kcm-about-distrorc
# transactional-update: no automatic reboots after updates
Source27:       50-ocelado-reboot.conf
# fonts and scrollbar images are taken from the openSUSE theme
BuildRequires:  grub2-branding-openSUSE
# grub2-branding-openSUSE needs (grub2 or grub2-common): pick one
BuildRequires:  grub2
BuildRequires:  systemd-rpm-macros
# owns the systemd unit/preset directories (filelist check)
BuildRequires:  systemd
%{?systemd_ordering}
Requires:       openSUSE-release
Requires(post): sed
# owns /usr/share/icons/hicolor/* (needed by the OBS filelist check)
BuildRequires:  hicolor-icon-theme
Requires:       hicolor-icon-theme
# first-login Plasma defaults (wallpaper, launcher icon)
Requires:       dbus-1
# zram swap (config below, units created by the generator at boot)
Requires:       zram-generator
# SDDM login screen on Wayland (KWin), Breeze theme (plasma6-desktop)
Requires:       kwin6
Requires(post): systemd
Requires(posttrans): systemd
Requires(posttrans): update-alternatives
# openSUSE KDE defaults (openSUSE Plasma/lock screen theme, Kickoff favorites
# for apps we do not ship, openSUSE IRC...): Ocelado uses plain Breeze and
# ships its own /etc/xdg files (kcm-about-distrorc here, kwinrc in
# deckifier-session-kde, baloofilerc in ocelado-baloo-off)
Obsoletes:      plasma6-branding-openSUSE
BuildArch:      noarch

%description
Sets NAME and PRETTY_NAME to "Ocelado Linux" in /usr/lib/os-release
(shown by KDE, fastfetch, the login screen...), LOGO to the Ocelado
logo (ocelado-logo icon) and the GRUB menu entry name, keeping the
openSUSE Tumbleweed ID and snapshot version.
Reapplied automatically every time openSUSE-release is updated.

%package -n ocelado-config-gamemode
Summary:        Ocelado Linux handheld (Steam Game Mode) system configuration
Requires:       ocelado-release = %{version}
Conflicts:      ocelado-config-desktop
Requires(posttrans): ocelado-release = %{version}

%description -n ocelado-config-gamemode
Enables the Game Mode services: session selection and SDDM autologin of the
first user into Steam (deckifier steamos-startup), InputPlumber and, on the
Steam Deck, the fan control daemon.

%package -n ocelado-config-desktop
Summary:        Ocelado Linux Desktop system configuration
Requires:       ocelado-release = %{version}
Requires:       transactional-update
Conflicts:      ocelado-config-gamemode
Requires(posttrans): ocelado-release = %{version}

%description -n ocelado-config-desktop
Desktop edition settings: SDDM login screen with Plasma (Wayland) by default,
daily background updates (transactional-update.timer) and automatic choice
of the linux-tkg kernel build for this CPU (x86-64-v2 or x86-64-v3).

%prep
%setup -q -c -T -a 1 -a 2

%build

%install
install -D -m 0755 %{SOURCE0} %{buildroot}%{_libexecdir}/ocelado/apply-branding
sed -i "s/@OCELADO_VERSION@/%{ocelado_version}/" %{buildroot}%{_libexecdir}/ocelado/apply-branding
# logo: os-release LOGO=ocelado-logo (KDE "About this System", etc.)
mkdir -p %{buildroot}%{_datadir}/icons
cp -a hicolor %{buildroot}%{_datadir}/icons/
# wallpaper (KDE wallpaper package) + first-login Plasma defaults:
# Ocelado wallpaper and launcher icon, applied once per user
mkdir -p %{buildroot}%{_datadir}/wallpapers
cp -a Ocelado %{buildroot}%{_datadir}/wallpapers/
install -D -m 0755 %{SOURCE3} %{buildroot}%{_libexecdir}/ocelado/plasma-defaults
install -D -m 0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/systemd/zram-generator.conf
install -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xdg/autostart/ocelado-plasma-defaults.desktop
install -D -m 0644 %{SOURCE26} %{buildroot}%{_sysconfdir}/xdg/kcm-about-distrorc
sed -i "s/@OCELADO_VERSION@/%{ocelado_version}/" %{buildroot}%{_sysconfdir}/xdg/kcm-about-distrorc
install -D -m 0644 %{SOURCE27} %{buildroot}%{_prefix}/etc/transactional-update.conf.d/50-ocelado-reboot.conf
# repository of Ocelado Linux (Tumbleweed repos come from openSUSE-repos)
install -D -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/zypp/repos.d/ogc-handheld.repo
# its signing key, next to the openSUSE ones (imported by the image build)
install -D -m 0644 %{SOURCE19} %{buildroot}%{_prefix}/lib/rpm/gnupg/keys/gpg-pubkey-ocelado.asc
# services + first boot
install -D -m 0644 %{SOURCE7} %{buildroot}%{_presetdir}/80-ocelado.preset
install -D -m 0755 %{SOURCE8} %{buildroot}%{_libexecdir}/ocelado/setup-system
install -D -m 0755 %{SOURCE9} %{buildroot}%{_libexecdir}/ocelado/firstboot
install -D -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}/ocelado-firstboot.service
# GRUB: boot the kernel type (ogc/tkg) chosen last
install -D -m 0755 %{SOURCE16} %{buildroot}%{_libexecdir}/ocelado/grub-default
install -D -m 0644 %{SOURCE17} %{buildroot}%{_unitdir}/ocelado-kernel-flavor.service
# Flathub remote, added once network is up
install -D -m 0644 %{SOURCE23} %{buildroot}%{_unitdir}/ocelado-flathub.service
install -D -m 0644 %{SOURCE24} %{buildroot}%{_prefix}/lib/modules-load.d/ocelado-gaming.conf
install -D -m 0644 %{SOURCE25} %{buildroot}%{_prefix}/lib/sysctl.d/90-ocelado-gaming.conf
# GRUB theme (GRUB_THEME set by grub-default)
t=%{buildroot}/boot/grub2/themes/Ocelado
mkdir -p $t
o=/usr/share/grub2/themes/openSUSE
cp -a $o/slider_*.png $o/COPYING.CC-BY-SA-3.0 $t/
cp -a $o/*.pf2 $t/ 2>/dev/null || cp -a /boot/grub2/themes/openSUSE/*.pf2 $t/
ls $t/*.pf2
install -m 0644 %{SOURCE20} $t/theme.txt
install -m 0644 %{SOURCE21} $t/logo.png
install -m 0644 %{SOURCE22} $t/highlight_c.png
# SDDM greeter on Wayland (no Xorg)
install -D -m 0644 %{SOURCE18} %{buildroot}%{_prefix}/lib/sddm/sddm.conf.d/20-ocelado-greeter.conf
# Game Mode edition
install -D -m 0644 %{SOURCE11} %{buildroot}%{_presetdir}/81-ocelado-gamemode.preset
# Desktop edition
install -D -m 0644 %{SOURCE12} %{buildroot}%{_presetdir}/81-ocelado-desktop.preset
install -D -m 0644 %{SOURCE13} %{buildroot}%{_prefix}/lib/sddm/sddm.conf.d/10-ocelado-desktop.conf
install -D -m 0755 %{SOURCE14} %{buildroot}%{_libexecdir}/ocelado/kernel-select
install -D -m 0644 %{SOURCE15} %{buildroot}%{_unitdir}/ocelado-kernel-select.service

%pre
%service_add_pre ocelado-firstboot.service ocelado-kernel-flavor.service ocelado-flathub.service

%post
%service_add_post ocelado-firstboot.service ocelado-kernel-flavor.service ocelado-flathub.service
# first installation (image build, Agama): system setup in %%posttrans, once
# all the packages of the transaction (sshd, sddm...) are installed
if [ "$1" -eq 1 ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/ocelado
    touch %{_localstatedir}/lib/rpm-state/ocelado/setup
fi
# drop Pillow's PIL.pth if it is already installed (see %filetriggerin)
rm -f %{_prefix}/lib64/python3*/site-packages/PIL.pth || :
# refresh the hicolor icon cache, otherwise Qt/KDE may not find ocelado-logo
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor || :
fi

%posttrans
if [ -e %{_localstatedir}/lib/rpm-state/ocelado/setup ]; then
    %{_libexecdir}/ocelado/setup-system || :
    rm -f %{_localstatedir}/lib/rpm-state/ocelado/setup
fi
# GRUB kernel selection (also on systems installed before 1.8)
systemctl enable ocelado-kernel-flavor.service >/dev/null 2>&1 || :
systemctl enable ocelado-flathub.service >/dev/null 2>&1 || :
%{_libexecdir}/ocelado/grub-default --refresh || :

# a kernel was installed or removed: newest kernel of the last used type on
# top. grub.cfg is regenerated afterwards by the kernel scriptlets themselves
%filetriggerin -- /boot
%{_libexecdir}/ocelado/grub-default || :

%filetriggerpostun -- /boot
%{_libexecdir}/ocelado/grub-default || :

# end of the transaction: regenerate grub.cfg if a trigger changed anything
%transfiletriggerin -- /boot
%{_libexecdir}/ocelado/grub-default --refresh || :

%transfiletriggerpostun -- /boot
%{_libexecdir}/ocelado/grub-default --refresh || :

%preun
%service_del_preun ocelado-firstboot.service ocelado-kernel-flavor.service ocelado-flathub.service

%postun
%service_del_postun_without_restart ocelado-firstboot.service ocelado-kernel-flavor.service ocelado-flathub.service
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor || :
fi

# runs when this package is installed and every time openSUSE-release is
# installed or updated (which rewrites /usr/lib/os-release)
%triggerin -- openSUSE-release
%{_libexecdir}/ocelado/apply-branding || :

# openSUSE's Pillow ships site-packages/PIL.pth, which puts the PIL/ package
# directory itself on sys.path for every Python program: modules named like
# Pillow's (report, features, Image...) then shadow other code, e.g. Decky
# plugins ("from report import ..." loads PIL/report.py). SteamOS has no such
# file: remove it every time Pillow is installed or updated.
%filetriggerin -- %{_prefix}/lib64
for f in $(grep -E '/site-packages/PIL\.pth$' 2>/dev/null); do
    rm -f "$f"
done
for f in %{_prefix}/lib64/python3*/site-packages/PIL.pth; do
    [ -e "$f" ] && rm -f "$f"
done
:

%post -n ocelado-config-gamemode
if [ "$1" -eq 1 ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/ocelado
    touch %{_localstatedir}/lib/rpm-state/ocelado/setup-gamemode
fi

%posttrans -n ocelado-config-gamemode
if [ -e %{_localstatedir}/lib/rpm-state/ocelado/setup-gamemode ]; then
    %{_libexecdir}/ocelado/setup-system || :
    rm -f %{_localstatedir}/lib/rpm-state/ocelado/setup-gamemode
fi
%{_libexecdir}/ocelado/apply-branding || :

%pre -n ocelado-config-desktop
%service_add_pre ocelado-kernel-select.service

%post -n ocelado-config-desktop
%service_add_post ocelado-kernel-select.service
if [ "$1" -eq 1 ]; then
    mkdir -p %{_localstatedir}/lib/rpm-state/ocelado
    touch %{_localstatedir}/lib/rpm-state/ocelado/setup-desktop
fi

%posttrans -n ocelado-config-desktop
if [ -e %{_localstatedir}/lib/rpm-state/ocelado/setup-desktop ]; then
    %{_libexecdir}/ocelado/setup-system || :
    rm -f %{_localstatedir}/lib/rpm-state/ocelado/setup-desktop
fi
%{_libexecdir}/ocelado/apply-branding || :

%preun -n ocelado-config-desktop
%service_del_preun ocelado-kernel-select.service

%postun -n ocelado-config-desktop
%service_del_postun_without_restart ocelado-kernel-select.service

%files
%dir %{_libexecdir}/ocelado
%{_libexecdir}/ocelado/apply-branding
%{_datadir}/icons/hicolor/*/apps/ocelado-logo*
%{_libexecdir}/ocelado/plasma-defaults
%dir %{_datadir}/wallpapers
%{_datadir}/wallpapers/Ocelado
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/xdg/autostart
%config %{_sysconfdir}/xdg/autostart/ocelado-plasma-defaults.desktop
%config %{_sysconfdir}/xdg/kcm-about-distrorc
%dir %{_prefix}/etc/transactional-update.conf.d
%{_prefix}/etc/transactional-update.conf.d/50-ocelado-reboot.conf
%dir %{_prefix}/lib/systemd
%{_prefix}/lib/systemd/zram-generator.conf
%dir %{_sysconfdir}/zypp
%dir %{_sysconfdir}/zypp/repos.d
%config(noreplace) %{_sysconfdir}/zypp/repos.d/ogc-handheld.repo
%dir %{_prefix}/lib/rpm
%dir %{_prefix}/lib/rpm/gnupg
%dir %{_prefix}/lib/rpm/gnupg/keys
%{_prefix}/lib/rpm/gnupg/keys/gpg-pubkey-ocelado.asc
%{_presetdir}/80-ocelado.preset
%{_libexecdir}/ocelado/setup-system
%{_libexecdir}/ocelado/firstboot
%{_unitdir}/ocelado-firstboot.service
%{_libexecdir}/ocelado/grub-default
%{_unitdir}/ocelado-kernel-flavor.service
%{_unitdir}/ocelado-flathub.service
%dir %{_prefix}/lib/modules-load.d
%{_prefix}/lib/modules-load.d/ocelado-gaming.conf
%dir %{_prefix}/lib/sysctl.d
%{_prefix}/lib/sysctl.d/90-ocelado-gaming.conf
%dir %{_prefix}/lib/sddm
%dir %{_prefix}/lib/sddm/sddm.conf.d
%{_prefix}/lib/sddm/sddm.conf.d/20-ocelado-greeter.conf
%dir /boot/grub2
%dir /boot/grub2/themes
/boot/grub2/themes/Ocelado

%files -n ocelado-config-gamemode
%{_presetdir}/81-ocelado-gamemode.preset

%files -n ocelado-config-desktop
%{_presetdir}/81-ocelado-desktop.preset
%{_prefix}/lib/sddm/sddm.conf.d/10-ocelado-desktop.conf
%{_libexecdir}/ocelado/kernel-select
%{_unitdir}/ocelado-kernel-select.service

%changelog
