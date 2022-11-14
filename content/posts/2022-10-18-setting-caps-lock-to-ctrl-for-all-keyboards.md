---
slug: setting-caps-lock-to-ctrl-for-all-keyboards
date: 2022-10-18T18:13:48-07:00
description: Setting Caps Lock to Ctrl for all keyboards
tags:
- keyboard
- remap
- caps lock
- ctrl
- x11
title: Setting Caps Lock to Ctrl for all keyboards
---

If

+ you don't really care about VMs and
+ just need this to work on the host for ALL keyboards, including those that you plug in after boot, and
+ you're using X11,

X11 uses XKB (X Keyboard Extension) to control the keyboard layout.

You can set the default with this

```
$ sudo localectl set-x11-keymap us pc105 '' 'ctrl:nocaps'
```

And then reboot

```
$ sudo reboot
```

`localectl` will automatically create/update the right configuration file (`/etc/default/keyboard` if you're using Debian/Ubuntu or `/etc/X11/xorg.conf.d/00-keyboard.conf`) for you.
