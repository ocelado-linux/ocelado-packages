#
# spec file for package steam-jupiter-bootstrap (Ocelado Linux)
#
# Valve's "fat" Steam bootstrap: the full Steam client, Steam Deck stable
# branch, exactly as SteamOS ships it in steam-jupiter-stable. Installed
# where gamescope-session-steam looks for it, so on the first Game Mode
# start Steam goes straight to its setup screen instead of downloading the
# whole client with a black screen.
#
# The file is redistributed unmodified (Steam install agreement: distribute
# the program in its entirety, do not modify "bootstrap" files).
#

# prebuilt Valve archive: nothing for rpmlint to check
#!BuildIgnore:  rpmlint-mini

Name:           steam-jupiter-bootstrap
Version:        20251031.0
Release:        0
Summary:        Fully bootstrapped Steam client for the first Game Mode start
License:        SUSE-NonFree
URL:            https://store.steampowered.com/
Source0:        steam_jupiter_stable_bootstrapped_%{version}.tar.xz
Requires:       gamescope-session-steam
Requires:       steam
BuildArch:      noarch

%description
Valve's fully bootstrapped Steam client (Steam Deck stable branch), the same
archive SteamOS ships. gamescope-session-steam unpacks it into the user's
Steam directory on the first Game Mode start, so Steam starts directly at
its setup screen.

%prep

%build

%install
install -D -m 0644 %{SOURCE0} \
    %{buildroot}%{_sysconfdir}/first-boot/bootstraplinux_ubuntu12_32.tar.xz

%files
%dir %{_sysconfdir}/first-boot
%{_sysconfdir}/first-boot/bootstraplinux_ubuntu12_32.tar.xz

%changelog
