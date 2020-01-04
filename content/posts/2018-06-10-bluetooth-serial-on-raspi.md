---
slug: bluetooth-serial-on-raspi
date: "2018-06-10T00:00:00Z"
description: Bluetooth Serial on Raspberry Pi
tags:
- bluetooth
- serial
- raspberry pi
title: Bluetooth Serial on Raspberry Pi
---

To enable serial over bluetooth on the raspberry pi, do these.

## 1. Restart `bluetoothd` with the `-C` flag to "provide deprecated command line interfaces".

To do this, you can kill `bluetoothd` and restart it on the command line, or edit `/etc/systemd/system/bluetooth.target.wants/bluetooth.service`

Add `-C` like this:

```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
```

Then restart `bluetoothd`

```
sudo systemctl restart bluetooth
```

## 2. Advertise a serial port service on your raspberry pi

```
$ sudo sdptool add SP
Serial Port service registered
$
```

## 3. Connect/pair your client to the raspberry pi

Do this by making the raspberry pi discoverable. You can either do this on the GUI, or

```
$ bluetoothctl
[NEW] Controller B8:27:EB:15:63:10 raspberrypi [default]
[bluetooth]# discoverable on
Changing discoverable on succeeded
[CHG] Controller B8:27:EB:15:63:10 Discoverable: yes
[bluetooth]# quit
[DEL] Controller B8:27:EB:15:63:10 raspberrypi [default]
pi@raspberrypi:~ $
```

I used my mac to connect to the raspberry pi, so on the mac, I used the GUI.

## 4. Start rfcomm. This watches `hci0` and listens so that it can run the command, which is `getty rfcomm0 115200 vt100 -a pi`

The command gives you a shell on the raspberry pi

```
$ sudo rfcomm watch hci0 1 getty rfcomm0 115200 vt100 -a pi
Waiting for connection on channel 1

```

## 5. Connect to the raspberry pi from the client.

On my mac, I used

```
screen /dev/cu.raspberrypi-SerialPort 115200
```

`/dev/cu.raspberrypi-SerialPort` appears after you pair successfully with the raspberry pi.
If you didn't advertise the serial port service, this device will not appear on the mac.
