#
# This is a special configuration of the Linux kernel, based on linux package
# for long-term support for iot
#

Name:           linux-iot
Version:        4.4.21
Release:        19
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.4.21.tar.xz
Source1:        config
Source2:        cmdline

%define kversion %{version}-%{release}.iot

BuildRequires:  bash >= 2.03
BuildRequires:  bc
BuildRequires:  binutils-dev
BuildRequires:  elfutils-dev
BuildRequires:  kmod
BuildRequires:  make >= 3.78
BuildRequires:  openssl-dev
BuildRequires:  flex
BuildRequires:  bison

# don't srip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

# Serie    00XX: mainline, CVE, bugfixes patches

# Serie    01XX: Clear Linux patches
#Patch0101: 0101-init-don-t-wait-for-PS-2-at-boot.patch
#Patch0102: 0102-sched-tweak-the-scheduler-to-favor-CPU-0.patch
Patch0103: 0103-kvm-silence-kvm-unhandled-rdmsr.patch
Patch0104: 0104-i8042-decrease-debug-message-level-to-info.patch
Patch0105: 0105-net-tcp-reduce-minimal-ack-time-down-from-40-msec.patch
Patch0106: 0106-init-do_mounts-recreate-dev-root.patch
Patch0107: 0107-Increase-the-ext4-default-commit-age.patch
Patch0108: 0108-silence-rapl.patch
Patch0109: 0109-pci-pme-wakeups.patch
Patch0110: 0110-ksm-wakeups.patch
Patch0111: 0111-intel_idle-tweak-cpuidle-cstates.patch
Patch0112: 0112-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0113: 0113-init_task-faster-timerslack.patch
#Patch0114: 0114-KVM-x86-Add-hypercall-KVM_HC_RETURN_MEM.patch
Patch0115: 0115-fs-ext4-fsync-optimize-double-fsync-a-bunch.patch
Patch0116: 0116-overload-on-wakeup.patch
Patch0117: 0117-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0118: 0118-fix-initcall-timestamps.patch
Patch0119: 0119-smpboot-reuse-timer-calibration.patch
Patch0120: 0120-raid6-add-Kconfig-option-to-skip-raid6-benchmarking.patch
Patch0121: 0121-Initialize-ata-before-graphics.patch
Patch0122: 0122-reduce-e1000e-boot-time-by-tightening-sleep-ranges.patch
Patch0123: 0123-xor-skip-benchmark-allocations-for-short-circuit-pat.patch

# Serie    XYYY: Extra features modules

# Extra backported features
Patch1001: 1001-crypto-testmgr-Add-a-flag-allowing-the-self-tests-to.patch
Patch1002: 1002-crypto-allow-testmgr-to-be-skipped.patch

# Minnowboard stuff
Patch2001: 2001-Add-low-speed-spidev-module.patch
Patch2002: 2002-Add-i2c-gpio-param-module.patch
Patch2003: 2003-i2c-designware-do-not-disable-adapter-after-transfer.patch

# cpuidle's governors set
Patch3001: 3001-cpuidle-x86-increase-forced-cut-off-for-polling-to-2.patch
Patch3002: 3002-cpuidle-menu-use-interactivity_req-to-disable-pollin.patch
Patch3003: 3003-cpuidle-menu-smooth-out-measured_us-calculation.patch
Patch3004: 3004-cpuidle-menu-Fix-menu_select-for-CPUIDLE_DRIVER_STAT.patch
Patch3005: 3005-cpuidle-menu-Avoid-pointless-checks-in-menu_select.patch
Patch3006: 3006-cpuidle-menu-avoid-expensive-square-root-computation.patch
Patch3007: 3007-cpuidle-menu-help-gcc-generate-slightly-better-code.patch
Patch3008: 3008-cpuidle-menu-use-high-confidence-factors-only-when-c.patch
Patch3009: 3009-cpuidle-menu-Fall-back-to-polling-if-next-timer-even.patch

# ads1015 + uvc drivers
Patch4001: 4001-iio-adc-Add-TI-ADS1015-ADC-driver-support.patch
#Patch4002: 4002-uvc-driver-Add-support-for-F200-color-formats.patch
#Patch4003: 4003-uvc-driver-Add-support-for-R200-color-formats.patch

# ACPI overlay
Patch5001: 5001-ACPI-OSL-Clean-up-initrd-table-override-code.patch
Patch5002: 5002-ACPI-OSL-Add-support-to-install-tables-via-initrd.patch
Patch5003: 5003-kernel-add-TAINT_OVERLAY_ACPI_TABLE.patch
Patch5004: 5004-acpi-decouple-initrd-table-install-from-CONFIG_ACPI_.patch
Patch5005: 5005-acpi-fix-enumeration-visited-flags-for-bus-rescans.patch
Patch5006: 5006-acpi-add-support-for-ACPI-reconfiguration-notifiers.patch
Patch5007: 5007-i2c-add-support-for-ACPI-reconfigure-notifications.patch
Patch5008: 5008-spi-add-support-for-ACPI-reconfigure-notifications.patch
Patch5009: 5009-efi-load-SSTDs-from-EFI-variables.patch
Patch5010: 5010-acpi-add-support-for-configfs.patch
Patch5011: 5011-acpi-add-support-for-loading-SSDTs-via-configfs.patch
Patch5012: 5012-HACK-acpi-configfs-add-unload_hanlde_path-attribute-.patch
Patch5013: 5013-configfs-implement-binary-attributes.patch
Patch5014: 5014-configfs-fix-CONFIGFS_BIN_ATTR_-RW-O-definitions.patch

%description
The Linux kernel for iot cases.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel

%description extra
Linux kernel extra files


%prep
%setup -q -n linux-4.4.21

# Serie    00XX: mainline, CVE, bugfixes patches

# Serie    01XX: Clear Linux patches
#%patch0101 -p1
#%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
#%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1

# Serie    XYYY: Extra features modules

# Extra backported features
%patch1001 -p1
%patch1002 -p1

# Minnowboard stuff
%patch2001 -p1
%patch2002 -p1
%patch2003 -p1

# cpuidle's governors set
%patch3001 -p1
%patch3002 -p1
%patch3003 -p1
%patch3004 -p1
%patch3005 -p1
%patch3006 -p1
%patch3007 -p1
%patch3008 -p1
%patch3009 -p1

# ads1015 + uvc drivers
%patch4001 -p1
#%patch4002 -p1
#%patch4003 -p1

# ACPI overlay
%patch5001 -p1
%patch5002 -p1
%patch5003 -p1
%patch5004 -p1
%patch5005 -p1
%patch5006 -p1
%patch5007 -p1
%patch5008 -p1
%patch5009 -p1
%patch5010 -p1
%patch5011 -p1
%patch5012 -p1
%patch5013 -p1
%patch5014 -p1

cp %{SOURCE1} .

%build
BuildKernel() {
    MakeTarget=$1

    Arch=x86_64
    ExtraVer="-%{release}".iot

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make -s mrproper
    cp config .config

    make -s ARCH=$Arch oldconfig > /dev/null
    make -s CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} ARCH=$Arch %{?sparse_mflags}
}

BuildKernel bzImage

%install

InstallKernel() {
    KernelImage=$1

    Arch=x86_64
    KernelVer=%{kversion}
    KernelDir=%{buildroot}/usr/lib/kernel

    mkdir   -p ${KernelDir}
    install -m 644 .config    ${KernelDir}/config-${KernelVer}
    install -m 644 System.map ${KernelDir}/System.map-${KernelVer}
    install -m 644 %{SOURCE2} ${KernelDir}/cmdline-${KernelVer}
    cp  $KernelImage ${KernelDir}/org.clearlinux.iot.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.iot.%{version}-%{release}

    mkdir -p %{buildroot}/usr/lib/modules/$KernelVer
    make -s ARCH=$Arch INSTALL_MOD_PATH=%{buildroot}/usr modules_install KERNELRELEASE=$KernelVer

    rm -f %{buildroot}/usr/lib/modules/$KernelVer/build
    rm -f %{buildroot}/usr/lib/modules/$KernelVer/source
}

InstallKernel arch/x86/boot/bzImage

rm -rf %{buildroot}/usr/lib/firmware

# Erase some modules index and then re-crate them
for i in alias ccwmap dep ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols usbmap softdep devname
do
    rm -f %{buildroot}/usr/lib/modules/%{kversion}/modules.${i}*
done
rm -f %{buildroot}/usr/lib/modules/%{kversion}/modules.*.bin

# Recreate modules indices
depmod -a -b %{buildroot}/usr %{kversion}

ln -s org.clearlinux.iot.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-iot

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/org.clearlinux.iot.%{version}-%{release}
/usr/lib/kernel/default-iot
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*

%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}
