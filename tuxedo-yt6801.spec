Name:           tuxedo-yt6801
Version:        1.0.28
Release:        5%{?dist}
Summary:        Driver for Motorcomm YT6801

License:        GPLv3+
Url:            https://www.tuxedocomputers.com
Source0:        tuxedo-yt6801_1.0.28.orig.tar.gz

Requires:       dkms >= 2.1

BuildArch:      noarch

Group:          Hardware/Other
Packager:       TUXEDO Computers GmbH <tux@tuxedocomputers.com>

%description
A driver for the Motorcomm YT6801 ethernet controller.

%prep
%setup -c -q

%install
mkdir -p %{buildroot}%{_usrsrc}/%{name}-%{version}
cp -r * %{buildroot}%{_usrsrc}/%{name}-%{version}
find %{buildroot}%{_usrsrc}/%{name}-%{version} -type f -exec chmod 0644 {} +
sed -i 's/\r$//' %{buildroot}%{_usrsrc}/%{name}-%{version}/dkms.conf
sed -i '/^REMAKE_INITRD=/d' %{buildroot}%{_usrsrc}/%{name}-%{version}/dkms.conf
sed -i 's/PACKAGE_NAME="yt6801"/PACKAGE_NAME="tuxedo-yt6801"/' %{buildroot}%{_usrsrc}/%{name}-%{version}/dkms.conf
rm %{buildroot}%{_usrsrc}/%{name}-%{version}/Makefile
printf "yt6801-objs :=  fuxi-gmac-common.o fuxi-gmac-desc.o fuxi-gmac-ethtool.o fuxi-gmac-hw.o fuxi-gmac-net.o fuxi-gmac-pci.o fuxi-gmac-phy.o fuxi-efuse.o fuxi-dbg.o fuxi-gmac-debugfs.o\nobj-m += yt6801.o\n" > %{buildroot}%{_usrsrc}/%{name}-%{version}/Kbuild

%files
%{_usrsrc}/%{name}-%{version}

%post
# Function to detect if we are inside a chroot environment
detect_chroot() {
    local root_path="/"
    local proc_root_path="/proc/1/root/."

    # Get device and inode of the root directory
    local root_stat
    root_stat=$(stat -c "%d:%i" "$root_path")

    # Get device and inode of /proc/1/root directory
    local proc_root_stat
    proc_root_stat=$(stat -c "%d:%i" "$proc_root_path")

    # Compare the two; if they differ, we are in a chroot
    if [ "$root_stat" != "$proc_root_stat" ]; then
        return 0  # In chroot
    else
        return 1  # Not in chroot
    fi
}
# Install modules via DKMS
dkms add -m %{name} -v %{version} --rpm_safe_upgrade
dkms build -m %{name} -v %{version}
dkms install -m %{name} -v %{version}
# Attempt to (re-)load module
if detect_chroot; then
    echo "Detected chroot environment. Skipping module (re)load."
else
    echo "(Re)load module if possible"
    rmmod yt6801 > /dev/null 2>&1
    if ! modprobe yt6801 > /dev/null 2>&1; then
        echo "Warning: Could not load module yt6801." >&2
    fi
fi

%preun
# Function to detect if we are inside a chroot environment
detect_chroot() {
    local root_path="/"
    local proc_root_path="/proc/1/root/."

    # Get device and inode of the root directory
    local root_stat
    root_stat=$(stat -c "%d:%i" "$root_path")

    # Get device and inode of /proc/1/root directory
    local proc_root_stat
    proc_root_stat=$(stat -c "%d:%i" "$proc_root_path")

    # Compare the two; if they differ, we are in a chroot
    if [ "$root_stat" != "$proc_root_stat" ]; then
        return 0  # In chroot
    else
        return 1  # Not in chroot
    fi
}
# Remove modules via DKMS
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade
# Attempt to (re-)load module, fail silently if not possible
if detect_chroot; then
    echo "Detected chroot environment. Skipping module (re)load."
else
    echo "(Re)load module if possible"
    rmmod yt6801 > /dev/null 2>&1
    modprobe yt6801 > /dev/null 2>&1
fi

%changelog
* Tue Aug 13 2024 Werner Sembach <tux@tuxedocomputers.com> 1.0.28-5
- Don't print warning for normal behaviour
- Fix rpm
* Tue Aug 13 2024 Maximilian Arnold <tux@tuxedocomputers.com> 1.0.28-4
- Removed reload of the module for chroot environments
* Mon Aug 12 2024 Werner Sembach <tux@tuxedocomputers.com> 1.0.28-3
- Switch build process to Kbuild instead of Makefile
* Wed Jul 31 2024 Christoffer Sandberg <tux@tuxedocomputers.com> 1.0.28-2
- Build fix for kernel version
* Wed Apr 03 2024 Werner Sembach <tux@tuxedocomputers.com> 1.0.28-1
- Initial release
