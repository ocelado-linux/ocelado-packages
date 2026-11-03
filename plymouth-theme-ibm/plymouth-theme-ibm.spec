#
# spec file for package plymouth-theme-ibm
#
# "ibm" boot splash from adi1090x/plymouth-themes (pack_3/ibm), the default
# Plymouth theme of Ocelado Linux.
#

Name:           plymouth-theme-ibm
Version:        0+git20230822
Release:        0
Summary:        IBM-style animated Plymouth boot splash
License:        GPL-3.0-only
URL:            https://github.com/adi1090x/plymouth-themes
# pack_3/ibm of the repository above (+ its LICENSE)
Source0:        ibm.tar.xz
BuildArch:      noarch
Requires:       plymouth
# the theme is a Plymouth script
Requires:       plymouth-plugin-script
Requires(posttrans): plymouth
# %%regenerate_initrd_* macros
BuildRequires:  suse-module-tools
%{?regenerate_initrd_requires}

%description
Animated boot splash (rotating squares) by Aditya Shakya (adi1090x).
Set as the default Plymouth theme when installed.

%prep
%setup -q -n ibm

%build

%install
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/ibm
install -m 0644 ibm.plymouth ibm.script *.png %{buildroot}%{_datadir}/plymouth/themes/ibm/

%post
%{?regenerate_initrd_post}

%posttrans
# make it the default theme (the splash lives in the initrd: regenerate it)
if [ "$(plymouth-set-default-theme 2>/dev/null)" != ibm ]; then
    plymouth-set-default-theme ibm || :
    %{?regenerate_initrd_posttrans}
fi

%files
%license LICENSE
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%{_datadir}/plymouth/themes/ibm

%changelog
