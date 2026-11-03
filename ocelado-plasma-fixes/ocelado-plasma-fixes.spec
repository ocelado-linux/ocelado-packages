#
# spec file for package ocelado-plasma-fixes
#
# Ocelado Linux fixes for the KDE Plasma session.
#

Name:           ocelado-plasma-fixes
Version:        1.2
Release:        0
Summary:        Ocelado Linux fixes for the KDE Plasma session
License:        MIT
URL:            https://build.opensuse.org/project/show/home:Luthenis:ogc-handheld
Source0:        50-ocelado-no-cycle.conf
Source1:        baloofilerc
BuildRequires:  systemd-rpm-macros
BuildArch:      noarch

%description
Breaks the systemd ordering cycle between plasma-workspace.target,
kde-baloo.service and graphical-session.target, which made the Plasma
logout hang and left KWin running into the next session (black screen
after leaving Desktop Mode).

%package -n ocelado-baloo-off
Summary:        Disable Baloo file indexing by default (Ocelado handhelds)
Requires:       %{name}
# owned /etc/xdg/baloofilerc before (dropped by ocelado-release)
Conflicts:      plasma6-branding-openSUSE

%description -n ocelado-baloo-off
Turns off Baloo file indexing by default on Ocelado Linux handheld
editions. Users can still enable it in System Settings > Search.

%prep

%build

%install
install -D -m 0644 %{SOURCE0} \
    %{buildroot}%{_userunitdir}/kde-baloo.service.d/50-ocelado-no-cycle.conf
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/baloofilerc

%files
%dir %{_userunitdir}/kde-baloo.service.d
%{_userunitdir}/kde-baloo.service.d/50-ocelado-no-cycle.conf

%files -n ocelado-baloo-off
%config %{_sysconfdir}/xdg/baloofilerc

%changelog
