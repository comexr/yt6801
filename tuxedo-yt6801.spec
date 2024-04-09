Name:           tuxedo-yt6801
Version:        1.0.28
Release:        1%{?dist}
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

%files
%{_usrsrc}/%{name}-%{version}

%post
# Install modules via DKMS
dkms add -m %{name} -v %{version} --rpm_safe_upgrade
dkms build -m %{name} -v %{version}
dkms install -m %{name} -v %{version}
# Attempt to (re-)load module, fail silently if not possible
echo "(Re)load module if possible"
rmmod yt6801 > /dev/null 2>&1 || true
modprobe yt6801 > /dev/null 2>&1 || true

%preun
# Remove modules via DKMS
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade
# Attempt to (re-)load module, fail silently if not possible
echo "(Re)load module if possible"
rmmod yt6801 > /dev/null 2>&1 || true
modprobe yt6801 > /dev/null 2>&1 || true

%changelog
* Wed Apr 03 2024 Werner Sembach <tux@tuxedocomputers.com> 1.0.28-1
- Initial release
