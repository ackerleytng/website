---
slug: linux-jffs-mini2440
date: "2015-04-06T00:00:00Z"
description: Putting Linux on mini2440 with a jffs2 filesystem
tags:
- mini2440 jffs jffs2 linux
title: Putting Linux on mini2440 with jffs2 filesystem
---
The [previous post]({% post_url 2015-04-05-linux-mini2440 %}) showed how to put Linux on the mini2440.

If you log in at the login prompt by entering the username root, you would be taken to `/root`. If you try writing to the filesystem,

```
# touch test
```

and you restart the device

```
# reboot
```

you will find that the file is not saved. To be able to write to the flash, we can place a jffs2 filesystem on the mini2440.

## Building the kernel and root file system

Using the same version of buildroot from the [previous post]({% post_url 2015-04-05-linux-mini2440 %}), I did `make menuconfig`.

Deselect `initial RAM filesystem linked into linux kernel` and deselect `cpio the root filesystem (for use as an initial RAM filesystem)`

I also selected `jffs2 root filesystem` and for `Flash Type`, I selected `NAND flash with 2kB Page and 128 kB erasesize`

Then...

```
make
```

## Conceptually,

You want to put U-Boot, a bootloader, into NAND flash, which will then load your linux kernel, which would in turn load your root filesystem.

You can use the U-Boot bootloader if it is already on the mini2440's NAND flash.

## Transferring uImage into NAND flash

Find the address of the kernel partition:

```
MINI2440 # mtdparts

device nand0 <mini2440-nand>, # parts = 4
 #: name                        size            offset          mask_flags
 0: u-boot              0x00040000      0x00000000      0
 1: u-boot_env          0x00020000      0x00040000      0
 2: kernel              0x00500000      0x00060000      0
 3: rootfs              0x0faa0000      0x00560000      0

active partition: nand0,0 - (u-boot) 0x00040000 @ 0x00000000

defaults:
mtdids  : nand0=mini2440-nand
mtdparts: <NULL>
```

Erase the kernel partition:

```
MINI2440# nand erase 60000 500000
```

Download uImage from Linux PC over LAN into RAM, at 0x32000000 again. First place `uImage` into `/tftpboot` (Google how to set up tftp).

```
MINI2440# tftp 32000000 uImage
```

Copy uImage from ram into NAND

```
MINI2440# nand write.e 32000000 60000 <size-of-uImage-in-hex>
```

Set the boot command to load kernel image from NAND flash.

```
MINI2440# setenv bootcmd 'nboot.e kernel;bootm'
MINI2440# saveenv
```

## Transferring `rootfs.jffs2` into NAND flash

Copy `rootfs.jffs2` from `buildroot-2015.02/output/images/` into `/tftpboot/`.


Erase the rootfs partition:

```
MINI2440# nand erase rootfs
```

Download `rootfs.jffs2` from Linux PC over LAN into RAM, at 0x32000000 again.

```
MINI2440# tftp 32000000 rootfs.jffs2
```

Copy uImage from ram into NAND

```
MINI2440# nand write.e 32000000 560000 <size-of-rootfs.jffs2-in-hex>
```

Set the boot command to load kernel image from NAND flash.

```
MINI2440# setenv bootcmd 'nboot.e kernel;bootm'
MINI2440# setenv bootargs 'root=/dev/mtdblock3 rootfstype=jffs2 console=ttySAC0,115200'
MINI2440# saveenv
```

Power cycle the mini2440.

## Full U-Boot environment for reference

```
MINI2440 # printenv
bootargs=root=/dev/mtdblock3 rootfstype=jffs2 console=ttySAC0,115200
bootdelay=3
baudrate=115200
ethaddr=08:08:11:18:12:27
usbtty=cdc_acm
mini2440=mini2440=0tb
bootargs_base=console=ttySAC0,115200 noinitrd
bootargs_init=init=/sbin/init
root_nand=root=/dev/mtdblock3 rootfstype=jffs2
root_mmc=root=/dev/mmcblk0p2 rootdelay=2
root_nfs=/mnt/nfs
set_root_nfs=setenv root_nfs root=/dev/nfs rw nfsroot=${serverip}:${root_nfs}
ifconfig_static=run setenv ifconfig ip=${ipaddr}:${serverip}::${netmask}:mini2440:eth0
ifconfig_dhcp=run setenv ifconfig ip=dhcp
ifconfig=ip=dhcp
set_bootargs_mmc=setenv bootargs ${bootargs_base} ${bootargs_init} ${mini2440} ${root_mmc}
set_bootargs_nand=setenv bootargs ${bootargs_base} ${bootargs_init} ${mini2440} ${root_nand}
set_bootargs_nfs=run set_root_nfs; setenv bootargs ${bootargs_base} ${bootargs_init} ${mini2440} ${root_nfs} ${ifconfig}
mtdids=nand0=mini2440-nand
mtdparts=mtdparts=mini2440-nand:0x00040000(u-boot),0x00020000(u-boot_env),0x00500000(kernel),0x0faa0000(rootfs)
bootcmd=nboot.e kernel;bootm
filesize=51A630
fileaddr=32000000
netmask=255.255.255.0
ipaddr=192.168.1.60
serverip=192.168.1.50
partition=nand0,0
mtddevnum=0
mtddevname=u-boot
```
