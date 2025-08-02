# Makefile for DKMS kernel module build
# This Makefile is used by DKMS to build the yt6801 kernel module

# Include Kbuild for the actual build configuration
include Kbuild

# DKMS will set KERNEL_DIR, fall back to current kernel if not set
# Find the first available kernel build directory
KERNEL_DIR ?= $(shell find /lib/modules -name "build" -type l | head -n1 | xargs -r dirname | xargs -r basename | xargs -I {} echo /lib/modules/{}/build)

# Fallback to current kernel if no build dir found
ifeq ($(KERNEL_DIR),)
KERNEL_DIR := /lib/modules/$(shell uname -r)/build
endif

# Default target for DKMS
all:
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) clean

install:
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) INSTALL_MOD_DIR=updates modules_install

.PHONY: all clean install
