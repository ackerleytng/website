---
slug: remapping-caps-lock-to-ctrl
date: "2017-02-12T00:00:00Z"
description: Remapping Caps Lock to Ctrl
tags:
- keyboard
- remap
- caps lock
- ctrl
- udev
title: Remapping Caps Lock to Ctrl
---
There are many other ways to do this, but most of the remapping happens at a higher level in the stack. Remapping at udev changes key mappings at the device level, so hopefully it works consistently throughout the whole OS.

Usually, remapping keys using `setxkbmap` doesn't work very well with VMware Workstation. On MacOS, remapping Caps Lock to Control works even in the VMs! Pressing Caps Lock while controlling VMs sends a Ctrl keypress to the VM. In Linux, I've previously tried remapping using `setxkbmap` on Linux Mint, and that doesn't work with VMs.

I've tried this on Ubuntu GNOME 16.04.2, and this remapping not only works in X and on the console, but also within VMs (if you press Caps Lock while the VM is in focus, the VM gets Ctrl).

All of this was done on a console (not a terminal in GNOME) because X also captures the keystrokes and works with it another way.

So press `ctrl-alt-f1`, and login on the console.

You've to create a file to update the udev hardware database. I created mine in `/lib/udev/hwdb.d/90-keyboard-remap.hwdb`. I believe you've to pick a number greater than `60`, since `60` was used for keyboards.

```
$ cat /lib/udev/hwdb.d/90-keyboard-remap.hwdb
evdev:input:b0003v258Ap1006*
 KEYBOARD_KEY_70039=leftctrl
$
```

The first line allows you to match the keyboard you're using.

The format is described in

```
$ less /lib/udev/hwdb.d/60-keyboard.hwdb
```

To find out my keyboard's vendor and product ID, I used

```
$ dmesg | grep input
```

and looked up the correct values. Note that the format requires four hex digits with capitalized alphabets.

To find out the scancode, I used `evtest`. Some guides tell you to use `showkey`, but `showkey` doesn't seem to be giving the correct scancodes. I suppose `showkey` only works for PS2 keyboards?

Anyway, I had to install `evtest` first:

```
$ sudo apt install evtest
```

then run `evtest`

```
$ evtest
```

Press the Caps Lock key and see what scancode was captured. Append that number after `KEYBOARD_KEY_` in `/lib/udev/hwdb.d/90-keyboard-remap.hwdb`.

Note: The second line, where you define the mapping, must be prefixed by one and only one space character.

Then, update the `hwdb` with

```
$ sudo udevadm hwdb --update
```

And then reboot

```
$ sudo reboot
```
