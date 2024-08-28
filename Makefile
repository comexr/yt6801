#
# Copyright (c) 2023 TUXEDO Computers GmbH <tux@tuxedocomputers.com>
#
# This file is part of tuxedo-soc-button-array.
#
# tuxedo-soc-button-array is free software; you can redistribute it and/or
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

.PHONY: package package-deb package-rpm

PACKAGE_NAME := $(shell grep -Pom1 '.*(?= \(.*\) .*; urgency=.*)' debian/changelog)
PACKAGE_VERSION := $(shell grep -Pom1 '.* \(\K.*(?=\) .*; urgency=.*)' debian/changelog)

package: package-deb package-rpm

package-deb:
	debuild --no-tgz-check --no-sign

package-rpm:
	sed 's/#MODULE_VERSION#/$(PACKAGE_VERSION)/' debian/tuxedo-yt6801.dkms > src/dkms.conf
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
