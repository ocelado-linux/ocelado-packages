#
# spec file for package jupiter-hw-support (ogc-handheld / Ocelado Linux)
#
# Steam Deck hardware support from Valve, built from the upstream SteamOS
# repository (mirror: github.com/evlav/jupiter-hw-support).
#
# Notes:
#  - SteamOS 3.8 stable series: Steam calls the helpers in
#    /usr/bin/steamos-polkit-helpers/ (3.9 renamed them to holo-*)
#  - BIOS / controller firmware update services are shipped but NOT enabled
#    at boot (SteamOS enables them); run jupiter-biosupdate or
#    jupiter-controller-update by hand, or enable the services
#  - SteamOS-only bits not installed: /etc/default/grub-steamos and the
#    alsa-restore.service mask
#

# rpmlint would reject Valve's prebuilt vendor tools (RPATHs) and the
# SteamOS polkit policies (not whitelisted by the SUSE security team), and
# those errors cannot be filtered: skip it for this package
#!BuildIgnore:  rpmlint-mini
%global debug_package %{nil}
%global __strip /bin/true
# prebuilt Valve/vendor tools live in /usr/share: no automatic deps from them
%global __provides_exclude_from ^/usr/share/.*$
%global __requires_exclude_from ^/usr/share/.*$

Name:           jupiter-hw-support
Version:        0
Release:        0
Summary:        Steam Deck hardware support files from SteamOS
License:        MIT AND SUSE-NonFree
URL:            https://gitlab.steamos.cloud/jupiter/jupiter-hw-support
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  systemd-rpm-macros
# /usr/share/polkit-1/{actions,rules.d} belong to polkit (rules.d with its own
# mode/owner): do not own them here, or polkit updates fail with a file
# conflict on the directory. polkit in the buildroot satisfies the OBS
# filelist check.
BuildRequires:  polkit
# builds the Steam cursor (icons/steam/cursors/default) like SteamOS does
BuildRequires:  xcursorgen
Requires:       bash
Requires:       dmidecode
Requires:       jq
Requires:       polkit
Requires:       python3
Requires:       systemd
Requires:       udisks2
Requires:       util-linux
# controller firmware updater (python scripts)
Recommends:     python3-click
Recommends:     python3-crcmod
Recommends:     python3-hidapi
Recommends:     python3-progressbar2
# the generic helpers for non-Deck handhelds install the same files
Conflicts:      deckifier-steamos-helpers
ExclusiveArch:  x86_64

%description
Steam Deck (Jupiter/Galileo) hardware support from SteamOS: polkit helpers
used by the Steam client (updates, timezone, hostname, SD card formatting,
fan/amp control...), udev rules, BIOS and controller firmware updaters,
thumbstick/trigger calibration tools and the SteamOS Plymouth theme.

%prep
%autosetup -p1

%build

%install
cp -a usr %{buildroot}/
# Steam cursor theme: the cursor links point to "default", generated here
(cd usr/share/steamos && xcursorgen steamos-cursor-config \
    %{buildroot}/usr/share/icons/steam/cursors/default)
# SteamOS-specific, not for openSUSE
rm -f  %{buildroot}%{_unitdir}/multi-user.target.wants/jupiter-biosupdate.service
rm -f  %{buildroot}%{_unitdir}/multi-user.target.wants/jupiter-controller-update.service
rmdir  %{buildroot}%{_unitdir}/multi-user.target.wants 2>/dev/null || :

%pre
%service_add_pre jupiter-biosupdate.service jupiter-controller-update.service

%post
%systemd_post jupiter-biosupdate.service jupiter-controller-update.service

%preun
%systemd_preun jupiter-biosupdate.service jupiter-controller-update.service

%postun
%systemd_postun jupiter-biosupdate.service jupiter-controller-update.service

%files
%license usr/share/jupiter_controller_fw_updater/RA_bootloader_updater/linux_host_tools/rfp-linux-x64/License_Agreement.txt
/usr/bin/amd_system_info
/usr/bin/foxnet-biosupdate
/usr/bin/jupiter-biosupdate
/usr/bin/jupiter-check-support
/usr/bin/jupiter-controller-update
/usr/bin/jupiter-initial-firmware-update
/usr/bin/thumbstick_cal
/usr/bin/thumbstick_fine_cal
/usr/bin/trigger_cal
%dir /usr/bin/steamos-polkit-helpers
/usr/bin/steamos-polkit-helpers/*
/usr/lib/hwsupport
/usr/lib/modprobe.d/*.conf
%{_unitdir}/jupiter-biosupdate.service
%{_unitdir}/jupiter-controller-update.service
/usr/lib/udev/rules.d/*.rules
/usr/share/icons/steam
/usr/share/jupiter_bios
/usr/share/jupiter_bios_updater
/usr/share/jupiter_controller_fw_updater
%dir /usr/share/plymouth
%dir /usr/share/plymouth/themes
/usr/share/plymouth/themes/steamos
/usr/share/polkit-1/actions/org.valve.steamos.policy
/usr/share/polkit-1/rules.d/*.rules
/usr/share/steamos

%changelog
