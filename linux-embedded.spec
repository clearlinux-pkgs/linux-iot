Name:           linux-embedded
Version:        4.2.3
Release:        1
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.2.3.tar.xz
Source1:        config
Source2:        cmdline

%define kversion %{version}-%{release}.embedded

BuildRequires:  bash >= 2.03
BuildRequires:  bc
# For bfd support in perf/trace
BuildRequires:  binutils-dev
BuildRequires:  elfutils
BuildRequires:  elfutils-dev
BuildRequires:  kmod
BuildRequires:  make >= 3.78
BuildRequires:  openssl
BuildRequires:  flex bison
BuildRequires:  ncurses-dev
BuildRequires:  binutils-dev
BuildRequires:  slang-dev
BuildRequires:  libunwind-dev
BuildRequires:  python-dev
BuildRequires:  zlib-dev
# For initrd binary package
BuildRequires:  dracut
BuildRequires:  util-linux
BuildRequires:  systemd
BuildRequires:  lz4

# don't srip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

Patch1:  0001-Don-t-wait-for-PS-2-at-boot.patch
Patch2:  0002-tweak-the-scheduler-to-favor-CPU-0.patch
Patch3:  0003-Silence-kvm-unhandled-rdmsr.patch
Patch4:  0004-intel-idle.patch
Patch5:  0005-i8042-Decrease-debug-message-level-to-info.patch
Patch6:  0006-Tweak-Intel-idle.patch
Patch7:  0007-raid6-boottime.patch
Patch8:  0008-reduce-the-damage-from-intel_pt-by-bailing-out-on-cp.patch
Patch9:  0009-reduce-minimal-ack-time-down-from-40-msec.patch

# low speed spidev module
Patch20: 2000-Add-low-speed-spidev-module.patch

# i2c gpio param module
Patch21: 2001-Add-i2c-gpio-param-module.patch

# i2c enable on resume instead initialization
#Patch22: 2002-i2c-enable-resume-instead-init.patch

# kdbus
Patch701: 701-kdbus.patch



%description
The Linux kernel for embedded cases.


%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel

%description extra
Linux kernel extra files


%prep
%setup -q -n linux-4.2.3

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# low speed spidev module
%patch20 -p1

# i2c gpio param module
%patch21 -p1

# i2c enable on resume instead initialization
#%patch22 -p1

# kdbus
%patch701 -p1

cp %{SOURCE1} .

%build
BuildKernel() {
    MakeTarget=$1

    Arch=x86_64
    ExtraVer="-%{release}".embedded

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
    cp  $KernelImage ${KernelDir}/org.clearlinux.embedded.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.embedded.%{version}-%{release}

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

ln -s org.clearlinux.embedded.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-embedded

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/org.clearlinux.embedded.%{version}-%{release}
/usr/lib/kernel/default-embedded
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*


%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}


