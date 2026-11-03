#
# spec file for package kernel-tkg (Ocelado Linux desktop kernels)
#
# linux-tkg (github.com/Frogging-Family/linux-tkg) for openSUSE Tumbleweed.
# Sources are prepared by the Ocelado GitHub workflow (OBS builds have no
# network, linux-tkg needs it): it runs `install.sh config` with the
# openSUSE Tumbleweed kernel-default config as base and uploads here
#   - linux-tkg-<version>.tar.xz   patched kernel tree (BORE + tkg patches)
#   - config-v2 / config-v3        final .config for each CPU level
#
# Flavors (_multibuild): v2 -> kernel-tkgv2 (-march=x86-64-v2)
#                        v3 -> kernel-tkgv3 (-march=x86-64-v3, AVX2)
#

# --- updated by the workflow ------------------------------------------
%define tkgrel     2
%define tkgcommit  6227ce308da8
Version:        7.3.1
# ------------------------------------------------------------------------

%define build_flavor @BUILD_FLAVOR@%{nil}
%if "%{build_flavor}" == ""
ExclusiveArch:  do_not_build
%define build_flavor v3
%endif

%define flavor     tkg%{build_flavor}
%define krel       %{version}-%{tkgrel}
%define kfull      %{krel}-%{flavor}
%define moddir     /usr/lib/modules/%{kfull}
%define scriptlets /usr/lib/module-init-tools/kernel-scriptlets

Name:           kernel-%{flavor}
Release:        0
Summary:        linux-tkg kernel (BORE) for Ocelado Linux, x86-64-%{build_flavor}
License:        GPL-2.0-only
URL:            https://github.com/Frogging-Family/linux-tkg
Source0:        linux-tkg-%{version}.tar.xz
Source1:        config-v2
Source2:        config-v3
ExclusiveArch:  x86_64

BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  dwarves
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  hostname
BuildRequires:  kmod
BuildRequires:  libdw-devel
BuildRequires:  libelf-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  python3-base
BuildRequires:  rsync
BuildRequires:  xz
BuildRequires:  zstd

Requires(pre):  suse-kernel-rpm-scriptlets
Requires(post): suse-kernel-rpm-scriptlets
Requires(preun): suse-kernel-rpm-scriptlets
Requires(postun): suse-kernel-rpm-scriptlets
Requires(posttrans): suse-kernel-rpm-scriptlets
Requires(post): dracut
Requires(post): kmod
Recommends:     kernel-firmware-all

# Ocelado: NOT multiversion(kernel). The module path only carries the kernel
# version (e.g. 7.2.14-3-ogc), so an OBS rebuild of the same version would
# install the same files next to the old package and conflict. Updates
# replace the package; older kernels stay available in previous snapshots.
Provides:       kernel-base = %{version}
Provides:       kernel-tkg = %{version}-%{release}

%description
Linux kernel built with linux-tkg (BORE CPU scheduler, Zen/Glitched
desktop tweaks, 1000 Hz timer) on top of the openSUSE Tumbleweed
kernel-default configuration, optimized for x86-64-%{build_flavor} CPUs.
tkg commit: %{tkgcommit}

%prep
%setup -q -n linux-tkg-%{version}

%build
# linux-tkg sets the CPU level in the top Makefile (KBUILD_CFLAGS/CPPFLAGS
# -march=..., KBUILD_RUSTFLAGS -Ctarget-cpu=...). The uploaded tree is the
# x86-64-v3 one: switch it to this flavor's level and check the result.
sed -i -E 's/(-march=|-Ctarget-cpu=)x86-64-v[0-9]+/\1x86-64-%{build_flavor}/g' Makefile
grep -nE -- '(-march=|-Ctarget-cpu=)x86-64-' Makefile
if ! grep -q -- "-march=x86-64-%{build_flavor}" Makefile; then
    echo "ERROR: -march=x86-64-%{build_flavor} not set in Makefile" >&2
    exit 1
fi
if grep -E -- '(-march=|-Ctarget-cpu=)x86-64-v[0-9]+' Makefile | grep -qv -- "x86-64-%{build_flavor}"; then
    echo "ERROR: Makefile still has another x86-64 level" >&2
    exit 1
fi

# The uploaded tree comes from "install.sh config" and keeps its generated
# files (include/config/kernel.release = 7.x.y-1-default from the Tumbleweed
# config). Kernel >= 6.3 reads kernelrelease from that file, so clean first.
# Drop any localversion* files too: they would be appended to the release.
make mrproper
rm -f localversion*

cp %{_sourcedir}/config-%{build_flavor} .config

# Out-of-tree build settings (same as kernel-ogc)
# Ocelado: Bosch BMI260 IMU (AOKZOE/OneXPlayer/GPD gyro, ACPI BMI0160);
# not enabled in the Tumbleweed config. Needs bmi260-init-data.fw
# (kernel-firmware)
./scripts/config --module BMI270 --module BMI270_I2C

./scripts/config --set-str LOCALVERSION "-%{tkgrel}-%{flavor}"
./scripts/config --disable LOCALVERSION_AUTO
./scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
./scripts/config --set-str SYSTEM_REVOCATION_KEYS ""
./scripts/config --set-str MODULE_SIG_KEY "certs/signing_key.pem"

make olddefconfig

KR=$(make -s kernelrelease)
if [ "$KR" != "%{kfull}" ]; then
    echo "ERROR: kernelrelease=$KR, expected %{kfull}" >&2
    exit 1
fi

export KBUILD_BUILD_HOST=obs
export KBUILD_BUILD_USER=ocelado
make %{?_smp_mflags} bzImage modules

%install
mkdir -p %{buildroot}%{moddir}
make INSTALL_MOD_PATH=%{buildroot}/usr INSTALL_MOD_STRIP=1 \
     DEPMOD=/bin/true modules_install
install -m 0644 "$(make -s image_name)" %{buildroot}%{moddir}/vmlinuz
install -m 0644 System.map %{buildroot}%{moddir}/System.map
install -m 0644 .config    %{buildroot}%{moddir}/config
: > %{buildroot}%{moddir}/sysctl.conf
rm -f %{buildroot}%{moddir}/build %{buildroot}%{moddir}/source

%define scriptlet_args --name %{name} --version %{version} --release %{release} --kernelrelease %{krel} --flavor %{flavor} --variant "" --image vmlinuz

%pre
%{scriptlets}/rpm-pre %{scriptlet_args} "$@"

%post
%{scriptlets}/rpm-post %{scriptlet_args} "$@"

%preun
%{scriptlets}/rpm-preun %{scriptlet_args} "$@"

%postun
%{scriptlets}/rpm-postun %{scriptlet_args} "$@"

%posttrans
%{scriptlets}/rpm-posttrans %{scriptlet_args} "$@"

%files
%dir %{moddir}
%{moddir}/vmlinuz
%{moddir}/System.map
%{moddir}/config
%{moddir}/sysctl.conf
%{moddir}/kernel
%{moddir}/modules.*

%changelog
