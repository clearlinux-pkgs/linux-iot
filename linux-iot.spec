Name:           linux-iot
Version:        4.4.12
Release:        10
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.4.12.tar.xz
Source1:        config
Source2:        cmdline

%define kversion %{version}-%{release}.iot

BuildRequires:  bash >= 2.03
BuildRequires:  bc
# For bfd support in perf/trace
BuildRequires:  binutils-dev
BuildRequires:  elfutils
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

Patch1:  0001-init-don-t-wait-for-PS-2-at-boot.patch
Patch2:  0002-sched-tweak-the-scheduler-to-favor-CPU-0.patch
Patch3:  0003-kvm-silence-kvm-unhandled-rdmsr.patch
Patch4:  0004-intel_idle-tweak-HSW-cpuidle-cstates.patch
Patch5:  0005-intel_idle-tweak-BDW-cpuidle-cstates.patch
Patch6:  0006-i8042-decrease-debug-message-level-to-info.patch
Patch7:  0007-raid6-reduce-boot-time.patch
Patch8:  0008-net-tcp-reduce-minimal-ack-time-down-from-40-msec.patch

# low speed spidev module
Patch20: 2000-Add-low-speed-spidev-module.patch

# i2c gpio param module
Patch21: 2001-Add-i2c-gpio-param-module.patch

# i2c designware do not disable adapter after transfer
Patch22: 2002-i2c-designware-do-not-disable-adapter-after-transfer.patch

# cpuidle's governors set
Patch30: 3000-cpuidle-x86-increase-forced-cut-off-for-polling-to-2.patch
Patch31: 3001-cpuidle-menu-use-interactivity_req-to-disable-pollin.patch
Patch32: 3002-cpuidle-menu-smooth-out-measured_us-calculation.patch
Patch33: 3003-cpuidle-menu-Fix-menu_select-for-CPUIDLE_DRIVER_STAT.patch
Patch34: 3004-cpuidle-menu-Avoid-pointless-checks-in-menu_select.patch
Patch35: 3005-cpuidle-menu-avoid-expensive-square-root-computation.patch
Patch36: 3006-cpuidle-menu-help-gcc-generate-slightly-better-code.patch
Patch37: 3007-cpuidle-menu-use-high-confidence-factors-only-when-c.patch
Patch38: 3008-cpuidle-menu-Fall-back-to-polling-if-next-timer-even.patch

# ads1015 + uvc drivers
Patch40: 4000-iio-adc-Add-TI-ADS1015-ADC-driver-support.patch
Patch41: 4001-uvc-driver-Add-support-for-F200-color-formats.patch
Patch42: 4002-uvc-driver-Add-support-for-R200-color-formats.patch

# ACPI overlay
Patch5000: 5000-ACPI-OSL-Clean-up-initrd-table-override-code.patch
Patch5001: 5001-ACPI-OSL-Add-support-to-install-tables-via-initrd.patch
Patch5002: 5002-kernel-add-TAINT_OVERLAY_ACPI_TABLE.patch
Patch5003: 5003-acpi-decouple-initrd-table-install-from-CONFIG_ACPI_.patch
Patch5004: 5004-acpi-fix-enumeration-visited-flags-for-bus-rescans.patch
Patch5005: 5005-acpi-add-support-for-ACPI-reconfiguration-notifiers.patch
Patch5006: 5006-i2c-add-support-for-ACPI-reconfigure-notifications.patch
Patch5007: 5007-spi-add-support-for-ACPI-reconfigure-notifications.patch
Patch5008: 5008-efi-load-SSTDs-from-EFI-variables.patch
Patch5009: 5009-acpi-add-support-for-configfs.patch
Patch5010: 5010-acpi-add-support-for-loading-SSDTs-via-configfs.patch
Patch5011: 5011-HACK-acpi-configfs-add-unload_hanlde_path-attribute-.patch
Patch5012: 5012-configfs-implement-binary-attributes.patch
Patch5013: 5013-configfs-fix-CONFIGFS_BIN_ATTR_-RW-O-definitions.patch

# enable RealSense on uvc
Patch70:  7000-Script-for-building-uvcvideo.ko.patch

%description
The Linux kernel for iot cases.


%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel

%description extra
Linux kernel extra files


%prep
%setup -q -n linux-4.4.12

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# low speed spidev module
%patch20 -p1

# i2c gpio param module
%patch21 -p1

# i2c designware do not disable adapter after transfer
%patch22 -p1

# cpuidle's governors set
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1

# ads1015 + uvc drivers
%patch40 -p1
%patch41 -p1
%patch42 -p1

# ACPI overlay
%patch5000 -p1
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

# enable RealSense on uvc
%patch70 -p1

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
    make -s CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} ARCH=$Arch $MakeTarget %{?sparse_mflags}
    make -s CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} ARCH=$Arch modules %{?sparse_mflags} || exit 1
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
