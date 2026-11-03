#
# spec file for package ocelado-agama
#
# Ocelado Linux products and appearance for the Agama installer.
# Installed only in the installer image (ocelado-installer), not in the
# installed system.
#

Name:           ocelado-agama
Version:        0.3
Release:        0
Summary:        Ocelado Linux for the Agama installer
License:        MIT
URL:            https://build.opensuse.org/project/show/home:Luthenis:ogc-handheld
Source0:        ocelado_deck.yaml
Source1:        ocelado_handheld.yaml
Source2:        ocelado_desktop.yaml
Source3:        brand.css
Source4:        Ocelado.svg
# signing key of the OBS project: Agama trusts /usr/lib/rpm/gnupg/keys/gpg-*
# (same file as ocelado-repo.key in ocelado-release)
Source5:        ocelado-repo.key
Source6:        ocelado_desktop_minimal.yaml
BuildArch:      noarch

%description
Ocelado Linux products and branding for the Agama installer.

%package -n ocelado-agama-products
Summary:        Ocelado Linux products for the Agama installer
Requires:       agama

%description -n ocelado-agama-products
Ocelado Linux products for the Agama installer: Steam Deck, AMD handhelds
(AOKZOE, OneXPlayer...), Desktop and Desktop Minimal.

%package -n ocelado-agama-branding
Summary:        Ocelado Linux appearance for the Agama installer
Requires:       agama-web-ui
# a medium carries one brand appearance (doc/theming_packaging.md)
Provides:       agama-branding
Conflicts:      agama-branding

%description -n ocelado-agama-branding
Ocelado Linux colors and logo for the Agama web installer.

%prep

%build

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/agama/products.d/ocelado_deck.yaml
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/agama/products.d/ocelado_handheld.yaml
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/agama/products.d/ocelado_desktop.yaml
install -D -m 0644 %{SOURCE6} %{buildroot}%{_datadir}/agama/products.d/ocelado_desktop_minimal.yaml
install -D -m 0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/rpm/gnupg/keys/gpg-ocelado-obs.asc
install -D -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/agama/web_ui/assets/appearance/brand.css
install -D -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/agama/web_ui/assets/logos/Ocelado.svg

%files -n ocelado-agama-products
%dir %{_datadir}/agama
%dir %{_datadir}/agama/products.d
%{_datadir}/agama/products.d/ocelado_*.yaml
%dir %{_prefix}/lib/rpm
%dir %{_prefix}/lib/rpm/gnupg
%dir %{_prefix}/lib/rpm/gnupg/keys
%{_prefix}/lib/rpm/gnupg/keys/gpg-ocelado-obs.asc

%files -n ocelado-agama-branding
%dir %{_datadir}/agama
%dir %{_datadir}/agama/web_ui
%dir %{_datadir}/agama/web_ui/assets
%dir %{_datadir}/agama/web_ui/assets/appearance
%dir %{_datadir}/agama/web_ui/assets/logos
%{_datadir}/agama/web_ui/assets/appearance/brand.css
%{_datadir}/agama/web_ui/assets/logos/Ocelado.svg

%changelog
