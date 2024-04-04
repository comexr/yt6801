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

package: package-deb package-rpm

package-deb:
	cd tuxedo-yt6801-1.0.28 && debuild --no-sign

package-rpm:
	mkdir -p $(shell rpm --eval "%{_sourcedir}")
	cp tuxedo-yt6801_1.0.28.orig.tar.gz $(shell rpm --eval "%{_sourcedir}")
	rpmbuild -ba tuxedo-yt6801.spec
