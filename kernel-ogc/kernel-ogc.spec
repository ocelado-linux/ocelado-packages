#
# spec file for package kernel-ogc
#
# Kernel del Open Gaming Collective (github.com/OpenGamingCollective/linux)
# empaquetado para openSUSE Tumbleweed.
#
# Config: base = config de kernel-default de Tumbleweed
#         + config/ogc.config.set / ogc.config.unset de OGC kernel-packages
#

# --- Cambiar SOLO estas dos lineas al subir de release OGC -------------
%define ogcrev  3
Version:        7.2.14
# ------------------------------------------------------------------------

%define flavor   ogc
%define krel     %{version}-%{ogcrev}
%define kfull    %{krel}-%{flavor}
%define moddir   /usr/lib/modules/%{kfull}
%define scriptlets /usr/lib/module-init-tools/kernel-scriptlets

Name:           kernel-ogc
Release:        0
Summary:        Open Gaming Collective kernel for handheld/gaming PCs
License:        GPL-2.0-only
URL:            https://github.com/OpenGamingCollective/linux
Source0:        linux-%{version}-ogc%{ogcrev}.tar.gz
Source1:        ogc.config.set
Source2:        ogc.config.unset
ExclusiveArch:  x86_64

# Para sacar la config base de Tumbleweed
BuildRequires:  kernel-default
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

# Permite tener varias versiones instaladas a la vez (fallback si una falla)
# Ocelado: NOT multiversion(kernel). The module path only carries the kernel
# version (e.g. 7.2.14-3-ogc), so an OBS rebuild of the same version would
# install the same files next to the old package and conflict. Updates
# replace the package; older kernels stay available in previous snapshots.
Provides:       kernel-base = %{version}

%description
Linux kernel from the Open Gaming Collective (OGC), with gaming and
handheld hardware support patches (Bazzite, ChimeraOS, Nobara, PikaOS...).
Built on top of the openSUSE Tumbleweed kernel-default configuration.

%prep
%setup -q -n linux-%{version}-ogc%{ogcrev}

%build
# 1. Config base: la de kernel-default instalado en el buildroot
BASECFG=$(ls -1 /usr/lib/modules/*-default/config 2>/dev/null | sort -V | tail -n1)
if [ -z "$BASECFG" ]; then
    echo "ERROR: no encuentro la config de kernel-default" >&2
    exit 1
fi
echo "Config base: $BASECFG"
cp "$BASECFG" .config

# 2. Capa OGC: =valor -> set ; nombre suelto -> disable
./scripts/kconfig/merge_config.sh -m .config %{SOURCE1}
grep -E '^CONFIG_[A-Za-z0-9_]+$' %{SOURCE2} | while read -r opt; do
    ./scripts/config --disable "${opt#CONFIG_}"
done

# Ocelado: Bosch BMI260 IMU (AOKZOE/OneXPlayer/GPD gyro, ACPI BMI0160);
# not enabled in the Tumbleweed config. Needs bmi260-init-data.fw
# (kernel-firmware)
./scripts/config --module BMI270 --module BMI270_I2C

# 3. Ajustes para compilar fuera del arbol de SUSE
./scripts/config --set-str LOCALVERSION "-%{ogcrev}-%{flavor}"
./scripts/config --disable LOCALVERSION_AUTO
./scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
./scripts/config --set-str SYSTEM_REVOCATION_KEYS ""
./scripts/config --set-str MODULE_SIG_KEY "certs/signing_key.pem"

make olddefconfig

# Comprobacion: la version tiene que coincidir con la ruta de modulos
KR=$(make -s kernelrelease)
if [ "$KR" != "%{kfull}" ]; then
    echo "ERROR: kernelrelease=$KR, esperado %{kfull}" >&2
    exit 1
fi

export KBUILD_BUILD_HOST=obs
export KBUILD_BUILD_USER=ogc-handheld
make %{?_smp_mflags} bzImage modules

%install
mkdir -p %{buildroot}%{moddir}

make INSTALL_MOD_PATH=%{buildroot}/usr INSTALL_MOD_STRIP=1 \
     DEPMOD=/bin/true modules_install

install -m 0644 "$(make -s image_name)" %{buildroot}%{moddir}/vmlinuz
install -m 0644 System.map %{buildroot}%{moddir}/System.map
install -m 0644 .config    %{buildroot}%{moddir}/config

# sysctl.conf: el que trae kernel-default, o vacio
SYSCTL=$(ls -1 /usr/lib/modules/*-default/sysctl.conf 2>/dev/null | tail -n1)
if [ -n "$SYSCTL" ]; then
    install -m 0644 "$SYSCTL" %{buildroot}%{moddir}/sysctl.conf
else
    : > %{buildroot}%{moddir}/sysctl.conf
fi

# Enlaces build/source no se empaquetan (no hay -devel todavia)
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
