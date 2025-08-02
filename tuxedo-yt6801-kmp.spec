# Spec file for OpenSUSE KMP with DKMS integration
# Provides automatic kernel module rebuilds

%define mod_name tuxedo-yt6801
%define mod_version 1.0.30tux2

Name:           %{mod_name}-kmp
Version:        %{mod_version}
Release:        1%{?dist}
Summary:        Kernel module for Motorcomm YT6801 ethernet controller
License:        GPL-2.0+
Group:          System/Kernel
URL:            https://www.tuxedocomputers.com
Source0:        %{mod_name}-%{version}.tar.xz
BuildRequires:  kernel-devel
BuildRequires:  dkms
Requires:       dkms
Requires:       kernel-devel
Requires:       kernel-source
Requires:       gcc
Requires:       make
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExclusiveArch:  %ix86 x86_64
BuildArch:      noarch

%description
This package contains the kernel module for the Motorcomm YT6801 gigabit
ethernet controller. It uses DKMS to automatically rebuild the module
for any installed kernel version on OpenSUSE Tumbleweed.

%prep
%setup -q -n %{mod_name}-%{version}

%build
# Nothing to build - DKMS will handle compilation

%install
# Install source to DKMS tree
mkdir -p %{buildroot}/usr/src/%{mod_name}-%{version}
cp -r src/* %{buildroot}/usr/src/%{mod_name}-%{version}/

# Create DKMS configuration
cat > %{buildroot}/usr/src/%{mod_name}-%{version}/dkms.conf << EOF
PACKAGE_NAME="%{mod_name}"
PACKAGE_VERSION="%{version}"
BUILT_MODULE_NAME[0]="yt6801"
DEST_MODULE_LOCATION[0]="/kernel/drivers/net/ethernet/motorcomm"
AUTOINSTALL="yes"
REMAKE_INITRD="yes"
EOF

%files
/usr/src/%{mod_name}-%{version}/

%post
# Add to DKMS tree
dkms add -m %{mod_name} -v %{version} --rpm_safe_upgrade

# Build and install for all installed kernels
if [ -z "$DURING_INSTALL" ]; then
    for kernel in /lib/modules/*; do
        if [ -d "$kernel" ]; then
            kernel_version=$(basename "$kernel")
            dkms build -m %{mod_name} -v %{version} -k "$kernel_version" 2>/dev/null || true
            dkms install -m %{mod_name} -v %{version} -k "$kernel_version" 2>/dev/null || true
        fi
    done
fi

%preun
# Remove from DKMS tree on uninstall
if [ $1 -eq 0 ]; then
    dkms remove -m %{mod_name} -v %{version} --all 2>/dev/null || true
fi

%changelog
# Changelog will be appended by the build process

%changelog
* Wed Jul 16 2025 Tuxedo BOT <tux@tuxedocomputers.com 1.0.30tux2-1
- Dynamically switch power mode on some devices for lower sleep power draw
* Thu Jun 12 2025 Tuxedo BOT <tux@tuxedocomputers.com 1.0.30tux1-1
- Update source to 1.0.30 from upstream
- Update Makefile
- Fix compile error with linux kernel >= v6.15
* Tue Mar 25 2025 Werner Sembach <tux@tuxedocomputers.com 1.0.29tux1-1
- Fix wrong name in Makefile
- Fix compile error because of bogus debug print define
* Wed Aug 28 2024 Werner Sembach <tux@tuxedocomputers.com 1.0.29tux0-1
- Update codebase to 1.0.29
- Convert to native package
* Tue Aug 13 2024 Werner Sembach <tux@tuxedocomputers.com 1.0.28-6-1
- Fix install error
* Tue Aug 13 2024 Werner Sembach <tux@tuxedocomputers.com 1.0.28-5-1
- Don't print warning for normal behaviour
- Fix rpm
* Tue Aug 13 2024 Maximilian Arnold <tux@tuxedocomputers.com 1.0.28-4-1
- Removed reload of the module for chroot environments
* Mon Aug 12 2024 Werner Sembach <tux@tuxedocomputers.com 1.0.28-3-1
- Switch build process to Kbuild instead of Makefile
* Wed Jul 31 2024 Christoffer Sandberg <tux@tuxedocomputers.com 1.0.28-2-1
- Build fix for kernel version
* Wed Apr 03 2024 Werner Sembach <tux@tuxedocomputers.com 1.0.28-1-1
- Initial release.
