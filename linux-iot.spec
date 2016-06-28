Name:           linux-iot
Version:        4.4.13
Release:        12
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.4.13.tar.xz
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

# Serie    00XX: mainline, CVE, bugfixes patches

Patch0002: cve-2016-4440.patch
Patch0003: cve-2016-4470.patch
Patch0004: cve-2016-5829.patch
#Patch0005: cve-2016-5828.nopatch # No x86 arch

# Serie    01XX: Clear Linux patches
Patch0101: 0101-init-don-t-wait-for-PS-2-at-boot.patch
Patch0102: 0102-sched-tweak-the-scheduler-to-favor-CPU-0.patch
Patch0103: 0103-kvm-silence-kvm-unhandled-rdmsr.patch
Patch0104: 0104-intel_idle-tweak-HSW-cpuidle-cstates.patch
Patch0105: 0105-intel_idle-tweak-BDW-cpuidle-cstates.patch
Patch0106: 0106-i8042-decrease-debug-message-level-to-info.patch
Patch0107: 0107-raid6-reduce-boot-time.patch
Patch0108: 0108-net-tcp-reduce-minimal-ack-time-down-from-40-msec.patch

# Minnowboard stuff
Patch1001: 1001-Add-low-speed-spidev-module.patch
Patch1002: 1002-Add-i2c-gpio-param-module.patch
Patch1003: 1003-i2c-designware-do-not-disable-adapter-after-transfer.patch

# cpuidle's governors set
Patch2001: 2001-cpuidle-x86-increase-forced-cut-off-for-polling-to-2.patch
Patch2002: 2002-cpuidle-menu-use-interactivity_req-to-disable-pollin.patch
Patch2003: 2003-cpuidle-menu-smooth-out-measured_us-calculation.patch
Patch2004: 2004-cpuidle-menu-Fix-menu_select-for-CPUIDLE_DRIVER_STAT.patch
Patch2005: 2005-cpuidle-menu-Avoid-pointless-checks-in-menu_select.patch
Patch2006: 2006-cpuidle-menu-avoid-expensive-square-root-computation.patch
Patch2007: 2007-cpuidle-menu-help-gcc-generate-slightly-better-code.patch
Patch2008: 2008-cpuidle-menu-use-high-confidence-factors-only-when-c.patch
Patch2009: 2009-cpuidle-menu-Fall-back-to-polling-if-next-timer-even.patch

# ads1015 + uvc drivers
Patch3001: 3001-iio-adc-Add-TI-ADS1015-ADC-driver-support.patch
Patch3002: 3002-uvc-driver-Add-support-for-F200-color-formats.patch
Patch3003: 3003-uvc-driver-Add-support-for-R200-color-formats.patch

# ACPI overlay
Patch4001: 4001-ACPI-OSL-Clean-up-initrd-table-override-code.patch
Patch4002: 4002-ACPI-OSL-Add-support-to-install-tables-via-initrd.patch
Patch4003: 4003-kernel-add-TAINT_OVERLAY_ACPI_TABLE.patch
Patch4004: 4004-acpi-decouple-initrd-table-install-from-CONFIG_ACPI_.patch
Patch4005: 4005-acpi-fix-enumeration-visited-flags-for-bus-rescans.patch
Patch4006: 4006-acpi-add-support-for-ACPI-reconfiguration-notifiers.patch
Patch4007: 4007-i2c-add-support-for-ACPI-reconfigure-notifications.patch
Patch4008: 4008-spi-add-support-for-ACPI-reconfigure-notifications.patch
Patch4009: 4009-efi-load-SSTDs-from-EFI-variables.patch
Patch4010: 4010-acpi-add-support-for-configfs.patch
Patch4011: 4011-acpi-add-support-for-loading-SSDTs-via-configfs.patch
Patch4012: 4012-HACK-acpi-configfs-add-unload_hanlde_path-attribute-.patch
Patch4013: 4013-configfs-implement-binary-attributes.patch
Patch4014: 4014-configfs-fix-CONFIGFS_BIN_ATTR_-RW-O-definitions.patch

%description
The Linux kernel for iot cases.


%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel

%description extra
Linux kernel extra files


%prep
%setup -q -n linux-4.4.13

# Serie    00XX: mainline, CVE, bugfixes patches

%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
#%patch0005 -p1 # # No x86 arch

# Serie    01XX: Clear Linux patches
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1

# Minnowboard stuff
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1

# cpuidle's governors set
%patch2001 -p1
%patch2002 -p1
%patch2003 -p1
%patch2004 -p1
%patch2005 -p1
%patch2006 -p1
%patch2007 -p1
%patch2008 -p1
%patch2009 -p1

# ads1015 + uvc drivers
%patch3001 -p1
%patch3002 -p1
%patch3003 -p1

# ACPI overlay
%patch4001 -p1
%patch4002 -p1
%patch4003 -p1
%patch4004 -p1
%patch4005 -p1
%patch4006 -p1
%patch4007 -p1
%patch4008 -p1
%patch4009 -p1
%patch4010 -p1
%patch4011 -p1
%patch4012 -p1
%patch4013 -p1
%patch4014 -p1

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
