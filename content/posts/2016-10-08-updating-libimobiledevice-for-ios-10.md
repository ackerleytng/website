---
slug: updating-libimobiledevice-for-ios-10
date: "2016-10-08T00:00:00Z"
description: How to update libimobiledevice for iOS 10 on Linux Mint 18
tags:
- libimobiledevice
- iPhone
- Linux Mint 18
- iOS 10
title: Updating libimobiledevice for iOS 10 on Linux Mint 18
---
If you connect your iPhone to Linux Mint 18 over USB after the iOS 10 update, and an empty nemo window pops up (as if your iPhone has no photos), you probably need to update `libimobiledevice`

Install dependencies for `libimobiledevice`:

```bash
sudo apt install git build-essential automake libtool libusbmuxd-dev libplist-dev libplist++-dev python-dev libssl-dev
```

Get the latest sources and compile it

```bash
git clone https://github.com/libimobiledevice/libimobiledevice.git
cd libimobiledevice
./autogen.sh
make
sudo make install
```

Make the system use the new library

```
sudo mv /usr/lib/x86_64-linux-gnu/libimobiledevice.so.6.0.0{,.bak}   # This makes a backup of the original library
sudo ln -s /usr/local/lib/libimobiledevice.so.6.0.0 /usr/lib/x86_64-linux-gnu/
```

Reboot.

After connecting the iPhone to Linux Mint for the first time, I had to eject the iPhone (using the eject icon next to iPhone in nemo) once and then mount it again before everything started behaving normally.
