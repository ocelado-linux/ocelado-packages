#!/bin/bash
# ogc-handheld image configuration (runs inside the image root at build time)
set -euxo pipefail

declare kiwi_profiles=${kiwi_profiles:-}

# shellcheck disable=SC1091
test -f /.kconfig && . /.kconfig

#======================================
# Console font
#--------------------------------------
echo FONT="eurlatgr.psfu" >> /etc/vconsole.conf

#======================================
# Reset machine-specific state
#--------------------------------------
rm -f \
    /etc/machine-id \
    /var/lib/zypp/AnonymousUniqueId \
    /var/lib/systemd/random-seed \
    /var/lib/dbus/machine-id

#======================================
# Default user: wheel (sudo/polkit) and device groups
#--------------------------------------
for g in wheel video audio input render; do
    if getent group "$g" >/dev/null; then
        usermod -aG "$g" gamer
    fi
done

#======================================
# Repositories: Tumbleweed + ogc-handheld
#--------------------------------------
# (openSUSE-release-appliance-* does not ship add-yast-repos, so add the
#  standard Tumbleweed repositories explicitly)
zypper --non-interactive ar -f -p 99 \
    "https://download.opensuse.org/tumbleweed/repo/oss/" repo-oss || true
zypper --non-interactive ar -f -p 99 \
    "https://download.opensuse.org/tumbleweed/repo/non-oss/" repo-non-oss || true
zypper --non-interactive ar -f -p 99 \
    "https://download.opensuse.org/update/tumbleweed/" repo-update || true
zypper --non-interactive ar -f -p 90 \
    "https://download.opensuse.org/repositories/home:/Luthenis:/ogc-handheld/openSUSE_Tumbleweed/" \
    ogc-handheld || true

#=====================================
# Trust the repository signing keys (openSUSE + Ocelado OBS project).
# Must happen here: on the installed system the rpm database is read-only
# and non-interactive updates reject unknown keys.
#-------------------------------------
for k in /usr/lib/rpm/gnupg/keys/*.asc; do
    rpm --import "$k" || true
done

#=====================================
# Snapper (root is a read-only snapshot)
#-------------------------------------
if [ "${kiwi_btrfs_root_is_snapshot-false}" = 'true' ]; then
    cp /usr/share/snapper/config-templates/default /etc/snapper/configs/root
    baseUpdateSysConfig /etc/sysconfig/snapper SNAPPER_CONFIGS root
    sed -i'' 's/^TIMELINE_CREATE=.*$/TIMELINE_CREATE="no"/g' /etc/snapper/configs/root
    sed -i'' 's/^NUMBER_LIMIT=.*$/NUMBER_LIMIT="2-10"/g' /etc/snapper/configs/root
    sed -i'' 's/^NUMBER_LIMIT_IMPORTANT=.*$/NUMBER_LIMIT_IMPORTANT="4-10"/g' /etc/snapper/configs/root
fi

#=====================================
# Boot: GRUB_DEFAULT/GRUB_SAVEDEFAULT/GRUB_TOP_LEVEL are managed by
# ocelado-release (boots the kernel type used last); only the timeout here
#-------------------------------------
if [ -f /etc/default/grub ]; then
    sed -i 's/^GRUB_TIMEOUT=.*/GRUB_TIMEOUT=3/' /etc/default/grub
fi

#=====================================
# Ocelado Linux branding (os-release + GRUB_DISTRIBUTOR)
#-------------------------------------
/usr/libexec/ocelado/apply-branding || true

#=====================================
# Edition: handhelds (Generic/Deck) have Steam Game Mode, Desktop does not
#-------------------------------------
GAMEMODE=1
case ",${kiwi_profiles}," in
    *,Desktop,*) GAMEMODE=0 ;;
esac

#=====================================
# Display manager: SDDM (Game Mode autologin handled by deckifier)
#-------------------------------------
if [ -f /etc/sysconfig/displaymanager ] && grep -q '^DISPLAYMANAGER=' /etc/sysconfig/displaymanager; then
    sed -i 's/^DISPLAYMANAGER=.*/DISPLAYMANAGER="sddm"/' /etc/sysconfig/displaymanager
else
    echo 'DISPLAYMANAGER="sddm"' >> /etc/sysconfig/displaymanager
fi
if update-alternatives --list default-displaymanager >/dev/null 2>&1; then
    update-alternatives --set default-displaymanager \
        /usr/lib/X11/displaymanagers/sddm || true
fi
if systemctl cat sddm.service >/dev/null 2>&1; then
    systemctl enable --force sddm.service
else
    systemctl enable --force display-manager.service || true
fi
if [ "$GAMEMODE" = 1 ]; then
    # first boot straight into Game Mode (Steam setup screen, like SteamOS);
    # later boots follow /etc/ogc-handheld/boot-session.conf (last mode used)
    /usr/bin/steamos-polkit-helpers/steamos-set-autologin gamescope-session-steam.desktop gamer || true
else
    # Desktop edition: normal SDDM login screen, Plasma (Wayland) by default
    mkdir -p /etc/sddm.conf.d
    printf '[General]\nDefaultSession=plasmawayland.desktop\n' > /etc/sddm.conf.d/10-ocelado-desktop.conf
    sed -i 's/^DISPLAYMANAGER_AUTOLOGIN=.*/DISPLAYMANAGER_AUTOLOGIN=""/' /etc/sysconfig/displaymanager || true
fi
echo "** display manager:"
ls -l /etc/systemd/system/display-manager.service || true
cat /etc/sddm.conf.d/zz-steamos-autologin.conf || true
# make sure no LightDM leftovers can take over display-manager.service
systemctl disable lightdm.service 2>/dev/null || true
rm -rf /etc/lightdm
systemctl set-default graphical.target

#=====================================
# Services
#-------------------------------------
for unit in \
    sshd.service \
    NetworkManager.service \
    bluetooth.service \
    chronyd.service \
    power-profiles-daemon.service ; do
    systemctl enable "$unit" || true
done

if [ "$GAMEMODE" = 1 ]; then
    # Game Mode: session selection at boot (deckifier) and controllers
    for unit in steamos-startup.service inputplumber.service; do
        systemctl enable "$unit" || true
    done
else
    # Desktop: daily background updates in a new snapshot, applied on the
    # next reboot (there is no Steam "Check for updates" here)
    systemctl enable transactional-update.timer || true
fi

#=====================================
# Steam Deck only services
#-------------------------------------
case ",${kiwi_profiles}," in
    *,Deck,*)
        systemctl enable jupiter-fan-control.service || true
        ;;
esac

# zram swap: no unit to enable, zram-generator creates systemd-zram-setup@zram0
# at boot from /usr/lib/systemd/zram-generator.conf (ocelado-release)

# To make x-systemd.growfs work from inside the initrd
cat >/etc/dracut.conf.d/50-microos-growfs.conf <<EOF
install_items+=" /usr/lib/systemd/systemd-growfs "
EOF

exit 0
