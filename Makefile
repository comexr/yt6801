#
# Copyright (c) 2023 TUXEDO Computers GmbH <tux@tuxedocomputers.com>
#
# This file is part of tuxedo-yt6801.
#
# tuxedo-yt6801 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

.PHONY: package package-deb package-rpm package-kmp package-kmp-simple

PACKAGE_NAME := $(shell grep -Pom1 '.*(?= \(.*\) .*; urgency=.*)' debian/changelog)
PACKAGE_VERSION := $(shell grep -Pom1 '.* \(\K.*(?=\) .*; urgency=.*)' debian/changelog)
KERNEL_VERSION := $(shell uname -r)

# Find a kernel version that has build directory available
BUILD_KERNEL := $(shell find /lib/modules -name "build" -type l | head -n1 | cut -d'/' -f4)
ifeq ($(BUILD_KERNEL),)
BUILD_KERNEL := $(KERNEL_VERSION)
endif

package: package-deb package-rpm

# Original DKMS-based RPM package
package-rpm-dkms: package-rpm

# New OpenSUSE KMP package
package-kmp: package-kmp-simple

package-deb:
	debuild --no-tgz-check --no-sign

# Original DKMS-based RPM package (kept for compatibility)
package-rpm:
	sed 's/#MODULE_VERSION#/$(PACKAGE_VERSION)/' debian/tuxedo-yt6801.dkms > src/dkms.conf
	sed 's/#MODULE_VERSION#/$(PACKAGE_VERSION)/' tuxedo-yt6801.spec.in > tuxedo-yt6801.spec
	echo >> tuxedo-yt6801.spec
	./debian-changelog-to-rpm-changelog.awk debian/changelog >> tuxedo-yt6801.spec
	mkdir -p $(shell rpm --eval "%{_sourcedir}")
	tar --create --file $(shell rpm --eval "%{_sourcedir}")/$(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.xz\
		--transform="s/src/$(PACKAGE_NAME)-$(PACKAGE_VERSION)\/usr\/src\/$(PACKAGE_NAME)-$(PACKAGE_VERSION)/"\
		--transform="s/debian\/copyright/$(PACKAGE_NAME)-$(PACKAGE_VERSION)\/LICENSE/"\
		--exclude=*.cmd\
		--exclude=*.d\
		--exclude=*.ko\
		--exclude=*.mod\
		--exclude=*.mod.c\
		--exclude=*.o\
		--exclude=modules.order\
		src debian/copyright
	rpmbuild -ba tuxedo-yt6801.spec

# New OpenSUSE KMP package (recommended for OpenSUSE)
package-kmp-simple:
	@echo "Building OpenSUSE KMP package..."
	sed 's/#MODULE_VERSION#/$(PACKAGE_VERSION)/g' tuxedo-yt6801-kmp-simple.spec.in > tuxedo-yt6801-kmp-simple.spec
	sed -i 's/#KERNEL_VERSION#/$(BUILD_KERNEL)/g' tuxedo-yt6801-kmp-simple.spec
	echo >> tuxedo-yt6801-kmp-simple.spec
	./debian-changelog-to-rpm-changelog.awk debian/changelog >> tuxedo-yt6801-kmp-simple.spec
	mkdir -p $(shell rpm --eval "%{_sourcedir}")
	tar --create --file $(shell rpm --eval "%{_sourcedir}")/$(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.xz\
		--transform="s/src/$(PACKAGE_NAME)-$(PACKAGE_VERSION)\/usr\/src\/$(PACKAGE_NAME)-$(PACKAGE_VERSION)/"\
		--transform="s/debian\/copyright/$(PACKAGE_NAME)-$(PACKAGE_VERSION)\/LICENSE/"\
		--exclude=*.cmd\
		--exclude=*.d\
		--exclude=*.ko\
		--exclude=*.mod\
		--exclude=*.mod.c\
		--exclude=*.o\
		--exclude=modules.order\
		src debian/copyright
	rpmbuild -ba tuxedo-yt6801-kmp-simple.spec

# Advanced OpenSUSE KMP package (using kernel_module_package macro)
package-kmp-advanced:
	@echo "Building OpenSUSE KMP package with kernel_module_package macro..."
	sed 's/#MODULE_VERSION#/$(PACKAGE_VERSION)/g' tuxedo-yt6801-kmp.spec.in > tuxedo-yt6801-kmp.spec
	echo >> tuxedo-yt6801-kmp.spec
	./debian-changelog-to-rpm-changelog.awk debian/changelog >> tuxedo-yt6801-kmp.spec
	mkdir -p $(shell rpm --eval "%{_sourcedir}")
	cp tuxedo-yt6801-preamble $(shell rpm --eval "%{_sourcedir}")/tuxedo-yt6801-preamble
	tar --create --file $(shell rpm --eval "%{_sourcedir}")/$(PACKAGE_NAME)-$(PACKAGE_VERSION).tar.xz\
		--transform="s/src/$(PACKAGE_NAME)-$(PACKAGE_VERSION)\/usr\/src\/$(PACKAGE_NAME)-$(PACKAGE_VERSION)/"\
		--transform="s/debian\/copyright/$(PACKAGE_NAME)-$(PACKAGE_VERSION)\/LICENSE/"\
		--exclude=*.cmd\
		--exclude=*.d\
		--exclude=*.ko\
		--exclude=*.mod\
		--exclude=*.mod.c\
		--exclude=*.o\
		--exclude=modules.order\
		src debian/copyright
	rpmbuild -ba tuxedo-yt6801-kmp.spec

# Test building the kernel module locally
test-build:
	@echo "Testing kernel module build..."
	@echo "Running kernel: $(KERNEL_VERSION)"
	@echo "Build kernel: $(BUILD_KERNEL)"
	make -C /lib/modules/$(BUILD_KERNEL)/build M=$(PWD)/src modules
	@echo "Build successful! Module: src/yt6801.ko"

# Clean build artifacts
clean:
	make -C /lib/modules/$(BUILD_KERNEL)/build M=$(PWD)/src clean || true
	rm -f tuxedo-yt6801.spec tuxedo-yt6801-kmp.spec tuxedo-yt6801-kmp-simple.spec
	rm -f src/dkms.conf
