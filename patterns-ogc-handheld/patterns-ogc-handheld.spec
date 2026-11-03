#
# spec file for package patterns-ogc-handheld
#
# Based on patterns-yuga (devel:microos:yuga:stable). Lines changed for
# ogc-handheld are marked with "# ogc:". Yuga branding packages are
# replaced by openSUSE branding; packages are taken from Tumbleweed whenever
# they exist there.
#

Name:           patterns-ogc-handheld
Version:        20261108
Release:        0
Summary:        Patterns for the ogc-handheld gaming image
License:        MIT
Group:          Metapackages
URL:            http://en.opensuse.org/Patterns
ExclusiveArch:  x86_64

%description
This is an internal package that is used to create the patterns of the
ogc-handheld image (SteamOS-like openSUSE with the OGC kernel).

################################################################
%package base-core
Summary:        Ocelado Linux core system
Group:          Metapackages
Provides:       pattern() = ogc_handheld_base_core
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9199
# ogc: SDDM is the only display manager; keep LightDM out (it is still
# recommended by other packages, so a plain update could pull it back in)
Conflicts:      lightdm
Conflicts:      lightdm-gtk-greeter
Conflicts:      lightdm-kde-greeter
# ogc: no openSUSE default kernel, every edition brings its own
# (OGC + linux-tkg on every edition, chosen in GRUB);
# on updates "dup" removes a kernel-default left from older images
Conflicts:      kernel-default
Conflicts:      kernel-default-base

### Packages formerly provided by minimal_base
Requires:       branding
Requires:       build-key
Requires:       distribution-release
Requires:       filesystem

### Packages formerly provided by base/basesystem
Requires:       /usr/bin/hostname
Requires:       aaa_base
Requires:       bash
Requires:       branding-openSUSE
Requires:       btrfsprogs
Requires:       ca-certificates
Requires:       ca-certificates-mozilla
Requires:       coreutils
Requires:       coreutils-systemd
Requires:       glibc
Suggests:       busybox-hostname
Requires:       NetworkManager
Requires:       NetworkManager-bluetooth
Requires:       NetworkManager-wifi
Requires:       iproute2
Requires:       lastlog2
Requires:       libnss_usrfiles2
Requires:       openSUSE-build-key
Requires:       pam
Requires:       pam-config
Requires:       procps
Requires:       rpm
Requires:       shadow
Requires:       systemd
Requires:       util-linux
Requires:       group(nobody)
Requires:       user(nobody)

####
Requires:       btrfsmaintenance
Requires:       busybox
# ogc: real GNU tar, not busybox-tar (Steam and others need it)
Requires:       tar
Requires:       chrony
# curl indirectly needed by ignition via dracut's url-lib
Requires:       curl
# ogc: needed by the Decky Loader installer (on the Deck it also comes
# with jupiter-hw-support, but generic handhelds need it too)
Requires:       jq
# probably needed for fsck.fat on efi partitions
Requires:       /usr/bin/gzip
# ogc: openSUSE Tumbleweed release/branding instead of Yuga
Requires:       openSUSE-release
Requires:       ocelado-release
Requires:       dosfstools
Requires:       glibc-locale-base
Suggests:       busybox-gzip
Requires:       health-checker
Requires:       health-checker-plugins-MicroOS
Requires:       iputils
Requires:       less
Requires:       microos-tools
Requires:       snapper
Requires:       vim-small
Requires:       wtmpdb
# people are addicted to sudo
Requires:       sudo
# let users authorize with their own password
Requires:       sudo-policy-wheel-auth-self
Requires:       systemd-presets-branding-openSUSE
Requires:       terminfo-base
Requires:       timezone
Conflicts:      gettext-runtime-mini
Conflicts:      krb5-mini
Obsoletes:      suse-build-key < 12.1
Requires:       exfatprogs
Requires:       distribution-logos-openSUSE-Tumbleweed

### Packages formerly provided by base_zypper
Requires:       transactional-update
Requires:       transactional-update-zypp-config
Requires:       zypper
# zypper ps is useless in transactional mode. It also checks for
# /run/reboot-needed though which is created by transactional-update
Requires:       zypper-needs-restarting

### Packages formerly provided by defaults
Requires:       audit
Requires:       systemd-coredump

### Packages formerly provided by hardware
Requires:       ethtool
Requires:       irqbalance
Requires:       hwinfo

### Packages formerly provided by selinux
Requires:       container-selinux
Requires:       policycoreutils
Requires:       selinux-policy-targeted
Requires:       selinux-tools

### Packages formerly provided by x11
Requires:       xorg-x11-fonts-core
# ogc: Wayland only (Plasma 6.8 dropped X11); Xwayland for X11 apps like Steam
Requires:       xwayland
# ogc: SDDM (like SteamOS) instead of LightDM; Game Mode autologin by deckifier
Requires:       sddm-qt6

### Packages formerly provided by desktop-common
# PipeWire is the default sound server
Requires:       gstreamer-plugin-pipewire
Requires:       pipewire-alsa
Requires:       pipewire-pulseaudio
Requires:       alsa-ucm-conf
# Add thunderbolt device management (boo#1208150)
Requires:       bolt
# Common tools
Requires:       bash-completion
Requires:       bluez-firmware
Requires:       glibc-locale
Requires:       hicolor-icon-theme-branding-openSUSE
Requires:       policycoreutils-python-utils
Requires:       polkit-default-privs
Requires:       systemd-icon-branding-openSUSE
Requires:       udisks2
Requires:       unzip
Requires:       upower
Requires:       wget
Requires:       xdg-utils
# Support ntfs drives
Requires:       ntfs-3g
Requires:       ntfsprogs
# More "comfortable" base package versions
Requires:       gzip
Requires:       hostname
# Desktop notifications about transactional update succeeding/failing
# for the masses
Requires:       transactional-update-notifier
# Needed by both GNOME and KDE for theming of GTK-based flatpak apps properly
Requires:       xdg-desktop-portal-gtk
# Needed to ensure MicroOS Desktop systems are be able to handle varied hardware out
# of the box, and not only during the system installation.
Requires:       kernel-firmware-all
Requires:       sof-firmware

Requires:       system-group-wheel

# from data/COMMON-DESKTOP
Requires:       desktop-file-utils

Requires:       flatpak
Requires:       dejavu-fonts
Requires:       noto-coloremoji-fonts
Requires:       noto-emoji-fonts
Requires:       noto-sans-fonts
Requires:       google-noto-coloremoji-fonts

# We need this for accessability and the lack of it causes big performance issues (boo#1204564)
Requires:       at-spi2-core
# #509829
Requires:       xdg-user-dirs-gtk
Requires:       power-profiles-daemon

### Kernel: chosen per edition (ogc: no kernel-default)
#   every edition: kernel-ogc + linux-tkg (BORE), selectable in GRUB
#   handhelds (ogc_handheld_gamemode): kernel-tkgv3, OGC first by default
#   desktop (ogc_handheld_desktop): kernel-tkgv2/v3, tkg first by default
### systemd-zram stuff
Requires:       systemd-zram-service

Requires:       pkexec

Requires:       systemd-experimental
# ogc: bootloader (and sdbootutil / TPM FDE tooling) is chosen by the image,
# not by the pattern. First image uses classic GRUB2 + grub2-snapper-plugin.
Requires:       efibootmgr

Requires:       shim
Requires:       uefi_mbr
Requires:       iio-sensor-proxy
Requires:       plymouth
Requires:       plymouth-dracut
Requires:       plymouth-branding-openSUSE
# ogc: Ocelado boot splash (adi1090x "ibm" theme), set as default
Requires:       plymouth-theme-ibm
#Vulkan
Requires:       kernel-firmware-amdgpu
Requires:       libdrm_amdgpu1
Requires:       libdrm_radeon1
Requires:       libvulkan_radeon
Requires:       libvulkan1
Requires:       libvulkan_intel

# ogc: xpad-noone-kmp-yuga dropped (KMP built for kernel-yuga, not kernel-ogc)

# ogc: deckrypt moved to pattern ogc_handheld_deck

#configure wireless devices
Requires:       wireless-regdb

%description base-core
Ocelado Linux core system: immutable openSUSE Tumbleweed (transactional
updates, snapshots), networking, audio, firmware and the SDDM login screen.

################################################################
%package base
Summary:        ogc-handheld base system
Group:          Metapackages
Provides:       pattern() = ogc_handheld_base
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9200
# ogc: everything essential is in ogc_handheld_base_core
Requires:       pattern() = ogc_handheld_base_core

%ifnarch %{arm}
Requires:       kdump
%endif
Requires:       yast2-logs
%ifnarch s390x
%endif
Requires:       fcoe-utils
# Allow users to print (and add some common printer drivers)
Requires:       OpenPrintingPPDs
Requires:       bluez-cups
Requires:       cups
Requires:       cups-filters
Requires:       cups-pk-helper
Requires:       epson-inkjet-printer-escpr
Requires:       ghostscript
Requires:       hplip-hpijs
Requires:       system-config-printer-common
Requires:       system-config-printer-dbus-service
Requires:       udev-configure-printer
Requires:       sane-backends
%if 0%{is_opensuse}
Requires:       avahi
%endif

# Some fonts
Requires:       adobe-sourcecodepro-fonts
Requires:       adobe-sourcesanspro-fonts
Requires:       adobe-sourceserifpro-fonts
Requires:       ghostscript-fonts-other
Requires:       ghostscript-fonts-std
Requires:       google-carlito-fonts
Requires:       google-droid-fonts
Requires:       google-opensans-fonts
Requires:       google-roboto-fonts
Requires:       noto-sans-math-fonts
Requires:       google-noto-sans-cjk-fonts

# So that GNOME prompt for ssh password works
Requires:       openssh-askpass-gnome
Requires:       samba
### Virtualisation support
Requires:       spice-vdagent
Requires:       qemu-guest-agent
Requires:       distrobox
Requires:       podman

Requires:       tpm2-0-tss
Requires:       tpm2.0-abrmd
Requires:       tpm2.0-tools
# ogc: systemd-repart-branding-Yuga dropped (partitioning handled in the image)
### Firstboot Configuration
Requires:       ignition-dracut
Requires:       combustion

# ogc: Steam Deck hardware moved to pattern ogc_handheld_deck
# ogc: Game Mode (gamescope, deckifier...) moved to pattern ogc_handheld_gamemode
Requires:       steam
Requires:       steam-devices
# ogc: extest-32bit (Yuga) dropped: not needed with Plasma 6 Wayland
# ogc: Wine/Proton launcher for non-Steam games (in Tumbleweed)
Requires:       faugus-launcher
# ogc: Proton-GE / Wine-GE / compatibility tools manager (official Tumbleweed)
Requires:       ProtonPlus
Requires:       libdrm_amdgpu1-32bit
Requires:       libdrm_radeon1-32bit
Requires:       libvulkan_radeon-32bit
Requires:       libvulkan1-32bit
#sdcard checking
Requires:       f3

Requires:       fprintd
Requires:       fprintd-pam

Requires:       bluez-obexd
Requires:       cifs-utils
#extra
Recommends:     ryzenadj

%description base
Ocelado Linux base system: immutable openSUSE Tumbleweed with the OGC
kernel, Steam and gaming tools. Game Mode lives in ogc_handheld_gamemode.

################################################################
%package kde-core
Summary:        Ocelado Linux minimal KDE Plasma desktop
Group:          Metapackages
Provides:       pattern() = ogc_handheld_kde_core
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9209
Requires:       pattern() = ogc_handheld_base_core
# ogc: plasma-branding-Yuga dropped, default openSUSE Plasma branding
Requires:       polkit-kde-agent-6
Requires:       konsole

# Recommended by kde_plasma
Requires:       bluedevil6
Requires:       dolphin
Requires:       plasma6-nm

Requires:       kio-extras
#Requires:	plasma6-addons
Requires:       plasma6-pa
Requires:       plasma6-session
Requires:       kde-gtk-config6
Requires:       kde-gtk-config6-gtk3
Requires:       kf6-qqc2-desktop-style
Requires:       xdg-desktop-portal-kde6

# Breeze GTK2, GTK3, and GTK4
Requires:       (gtk4-metatheme-breeze6 if gtk4)
Requires:       (gtk2-metatheme-breeze6 if gtk2)
Requires:       (gtk3-metatheme-breeze6 if gtk3)

# For seeing thumbnails in Dolphin
Requires:       qt6-imageformats
Requires:       kf6-kimageformats

# Add kcm_flatpak for managing flatpak permissions (boo#1208256)
Requires:       flatpak-kcm6

# Add pam_kwallet to unlock the password store automatically
Requires:       pam_kwallet6

# For crisp status notifier systray icons
Requires:       libappindicator-gtk3

# Ocelado: breaks the kde-baloo / plasma-workspace.target systemd ordering
# cycle that hung the Plasma logout (all editions)
Requires:       ocelado-plasma-fixes

%description kde-core
Minimal KDE Plasma (Wayland) for Ocelado Linux: Plasma session, network,
audio and Bluetooth applets, Konsole and Dolphin.

################################################################
%package kde
Summary:        ogc-handheld KDE Plasma desktop
Group:          Metapackages
Provides:       pattern() = ogc_handheld_kde
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9210
Provides:       pattern-visible()
Requires:       pattern() = ogc_handheld_base
Requires:       pattern() = ogc_handheld_kde_core

# Some basic system tools
Requires:       featherpad
# Add KDE Partition Manager (boo#1212925)
Requires:       partitionmanager

# Add ksshaskpass5 (boo#1215407)
Requires:       ksshaskpass6
Requires:       breeze6-wallpapers
Requires:       kde-print-manager
Requires:       plasma6-print-manager
Requires:       kgamma6
Requires:       phonon-vlc-qt6
Requires:       plasma6-workspace-wallpapers

# Manually pull in baloo5-file to better support desktip search functions/desktop integration
Requires:       kf6-baloo-file

# For NetworkManager support of openVPN Connections
Requires:       NetworkManager-openvpn
Requires:       openvpn-auth-pam-plugin
Requires:       plasma6-nm-openconnect
Requires:       plasma6-nm-openvpn
Requires:       kwalletmanager
Suggests:       kwalletmanager
Requires:       pinentry-qt5

# Recommends and Supplements won't work so pull in manually
Requires:       discover6-backend-flatpak
Requires:       discover6-backend-fwupd
Requires:       plasma-browser-integration
Requires:       kf6-purpose

# Doesnt depend on PackageKit, but also works for other backends
Requires:       discover6-notifier

# Spectacle to be able to take screenshots out of the box
Requires:       spectacle

# KAccounts to be installed by default (boo#1216397)
Requires:       kaccounts-integration
Requires:       kaccounts-providers
Requires:       kio-gdrive

# Default Plasma app to quickly use emojis
Requires:       plasma6-desktop-emojier

# Default Plasma/Oxygen sounds for applications
Requires:       oxygen5-sounds

# Plasma system monitor
Requires:       plasma6-systemmonitor
Requires:       ffmpegthumbs
Requires:       kdegraphics-thumbnailers

# Add for mounting network shares in userspace (boo#1210125)
Requires:       kio-fuse
Requires:       kdenetwork-filesharing

# KDE Connect to communicate to phone devices
Requires:       kdeconnect-kde

# Warn when apps are using all inotify watches and prompts the user to raise it
Requires:       kde-inotify-survey

# ogc: steamdeck-kde-presets moved to pattern ogc_handheld_deck
# ogc: deckifier-session-kde (Desktop Mode of the handhelds) moved to
# pattern ogc_handheld_gamemode, so the KDE desktop works without it

%description kde
KDE Plasma desktop (Wayland) for Ocelado Linux.

################################################################
%package gamemode
Summary:        Ocelado Linux Steam Game Mode (SteamOS-like)
Group:          Metapackages
Provides:       pattern() = ogc_handheld_gamemode
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9205
Requires:       pattern() = ogc_handheld_base
Requires:       pattern() = ogc_handheld_kde
# ogc: both kernels, chosen in GRUB (it boots the type used last; OGC
# before the first choice). OGC: handheld patches (Open Gaming Collective)
Requires:       kernel-ogc
# linux-tkg (BORE). Every supported handheld (Steam Deck Zen 2, AOKZOE A1X
# Zen 3) is x86-64-v3
Requires:       kernel-tkgv3
# ogc: Factory gamescope / gamescope-session-plus instead of Yuga's forks
Requires:       gamescope
Requires:       gamescope-session-plus
Requires:       gamescope-session-steam
# ogc: Valve's fully bootstrapped Steam client: first Game Mode start goes
# straight to the Steam setup screen (no client download, no black screen)
Requires:       steam-jupiter-bootstrap
Requires:       mangoapp
# Game Mode / Desktop Mode switching, trup updates from Steam, SDDM autologin
Requires:       deckifier
Requires:       deckifier-session-kde
Requires:       inputplumber
# ogc: InputPlumber hides the physical gamepad with setfacl; without acl it
# fails ("Unable to determine setfacl command location") and Steam sees
# two controllers (the real one and the virtual one)
Requires:       acl
# ogc: official Tumbleweed power button daemon
Requires:       steamos-powerbuttond
# ogc: Game Mode services (steamos-startup autologin, InputPlumber, fans)
Requires:       ocelado-config-gamemode
# ogc: no Baloo file indexing on handhelds (Deck and AOKZOE/OneXPlayer)
Requires:       ocelado-baloo-off

%description gamemode
SteamOS-like Steam Game Mode for Ocelado Linux handhelds: gamescope
session, Game Mode / Desktop Mode switching and Steam integration.

################################################################
%package desktop
Summary:        Ocelado Linux Desktop (KDE Plasma, linux-tkg kernel)
Group:          Metapackages
Provides:       pattern() = ogc_handheld_desktop
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9240
Provides:       pattern-visible()
Requires:       pattern() = ogc_handheld_base
Requires:       pattern() = ogc_handheld_kde
# linux-tkg (BORE). The first alternative (v2, runs on any x86-64-v2 CPU)
# is the one installed; on first boot ocelado-kernel-select swaps it for
# kernel-tkgv3 when the CPU supports x86-64-v3
Requires:       (kernel-tkgv2 or kernel-tkgv3)
# ogc: OGC kernel too, chosen in GRUB (it boots the type used last; tkg
# before the first choice)
Requires:       kernel-ogc
# SDDM login screen, background updates, kernel selection
Requires:       ocelado-config-desktop
# ogc: GPU control (fans, power limit, clocks, undervolt) for AMD/Nvidia;
# daemon lactd enabled by ocelado-config-desktop
Requires:       lact
# no Steam Game Mode on the desktop edition
Conflicts:      pattern() = ogc_handheld_gamemode

%description desktop
Ocelado Linux for desktop PCs and laptops: KDE Plasma with the linux-tkg
kernel, without the Steam Game Mode session.

################################################################
%package desktop-minimal
Summary:        Ocelado Linux Desktop Minimal (bare KDE Plasma, linux-tkg kernel)
Group:          Metapackages
Provides:       pattern() = ogc_handheld_desktop_minimal
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9245
Provides:       pattern-visible()
Requires:       pattern() = ogc_handheld_base_core
Requires:       pattern() = ogc_handheld_kde_core
# same kernels and system configuration as ogc_handheld_desktop
Requires:       (kernel-tkgv2 or kernel-tkgv3)
Requires:       kernel-ogc
Requires:       ocelado-config-desktop
# apps from Flatpak (no Discover: flatpak CLI / Flathub)
Requires:       flatpak
Conflicts:      pattern() = ogc_handheld_gamemode

%description desktop-minimal
Ocelado Linux Desktop Minimal: bare KDE Plasma with Konsole, Dolphin and
Flatpak, for users who want to build their own setup.

################################################################
%package deck
Summary:        ogc-handheld Valve Steam Deck hardware support
Group:          Metapackages
Provides:       pattern() = ogc_handheld_deck
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9220
Provides:       pattern-visible()
Requires:       pattern() = ogc_handheld_base
Requires:       pattern() = ogc_handheld_gamemode

Requires:       jupiter-fan-control
Requires:       jupiter-hw-support
# ogc: jupiter-dock-updater-bin dropped: it downloads the dock firmware at
# install time, which fails in offline image builds
Requires:       sdgyrodsu
# ogc: steamdeck-firmware (Yuga) dropped: the Deck OLED wifi/bt firmware
# (ath11k QCA2066, qca hpbtfw21/hpnv21) is upstream, in kernel-firmware-all
Requires:       steamdeck-dsp
Requires:       galileo-mura
# ogc: steamdeck-kde-presets (Yuga) dropped: its /etc/xdg/kwinrulesrc
# conflicts with kwin6 >= 6.8, which now ships that file itself
# Encryption unlock with the Deck controller
Recommends:     deckrypt

%description deck
Hardware support for the Valve Steam Deck (LCD "Jupiter" and OLED "Galileo").

################################################################
%package aokzoe
Summary:        ogc-handheld AOKZOE / OneXPlayer hardware support
Group:          Metapackages
Provides:       pattern() = ogc_handheld_aokzoe
Provides:       pattern-category() = ogc-handheld
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9230
Provides:       pattern-visible()
Requires:       pattern() = ogc_handheld_base
Requires:       pattern() = ogc_handheld_gamemode

# TDP control (RGB and buttons: hid-oxp in kernel + InputPlumber)
Requires:       ryzenadj
# Steam system helpers (update, timezone, reboot...); on the Deck they
# come from jupiter-hw-support
# (first alternative is the one picked when neither is installed)
Requires:       (deckifier-steamos-helpers or jupiter-hw-support)

%description aokzoe
Hardware support for AOKZOE / OneXPlayer handhelds (e.g. AOKZOE A1X).

################################################################
%prep
# empty on purpose

%build
# empty on purpose

%install
mkdir -p %{buildroot}%{_docdir}/patterns-ogc-handheld/
for i in base-core base kde-core kde gamemode desktop desktop-minimal deck aokzoe; do
    echo "This file marks the pattern ogc_handheld_$i to be installed." \
        > %{buildroot}%{_docdir}/patterns-ogc-handheld/${i}.txt
done

%files base-core
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/base-core.txt

%files base
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/base.txt

%files kde-core
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/kde-core.txt

%files kde
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/kde.txt

%files gamemode
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/gamemode.txt

%files desktop
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/desktop.txt

%files desktop-minimal
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/desktop-minimal.txt

%files deck
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/deck.txt

%files aokzoe
%dir %{_docdir}/patterns-ogc-handheld
%{_docdir}/patterns-ogc-handheld/aokzoe.txt

%changelog
