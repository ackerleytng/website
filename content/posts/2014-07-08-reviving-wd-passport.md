---
slug: reviving-wd-passport
date: "2014-07-08T00:00:00Z"
description: Reviving the WD Passport
tags:
- Western Digital
- WD
- external hard disk
- guides
title: Reviving the WD Passport
---
So. I'm not sure if this is just luck, but I managed to revive a connection to my WD Passport (Essential SE). There are so many forum threads on the Internet that discuss this topic, but most are just cliffhangers that don't provide real solutions.

It was neither being recognized on a Mac nor PC, even after:

- Trying different cables
- Using the USB ports at the back of the computer instead of those in the front

Here are some other suggestions that you might want to try if you have the resources or patience. I personally think that this is not an issue with power supply to the WD Passport, but you can still try:

- Using a Y-cable, which is something like [this](http://en.wikipedia.org/wiki/File:Y-shaped_USB_3.0_cable.jpg)
- Returning it to Western Digital for a new unit
- Disconnecting all unnecessary USB devices so that all the power goes to the WD Passport

### Revival Procedure ###

I used a desktop PC running 64-bit Windows 7, eventually, to connect to the WD Passport. The WD Passport was never used with this desktop before, hence we know that the drivers for the WD Passport was never installed from the web.

1. Connect the WD Passport to the USB ports at the *back* of a *desktop* PC. Windows will probably attempt to install the WD Passport, but will not find the right drivers, because it is unable to identify the device.
2. Go to Device Manager. You should see a USB device that has a yellow triangle next to it, indicating that the drivers for the WD Passport were not installed properly.
3. Download and install the appropriate WD Passport drivers from [here](http://wdc.custhelp.com/app/answers/detail/a_id/1708/related/1/session/L2F2LzEvdGltZS8xNDA0ODUwMTc4L3NpZC8zd0ExaE9ZbA%3D%3D)
4. Go back to Device Manager. Right-click on the Unknown Device, then select "Update Driver Software".
5. Choose to browse your computer for driver software.
6. Pick from a list of device drivers on your computer.
7. From the list, choose Western Digital, then select WD SES Device. Complete that installation procedure and the WD Passport should now be recognized as a "WD SES Device". The drive, however, is probably still not working.
8. Unplug the WD Passport. (I unplugged the USB cable on the side of the WD Passport (as opposed to the side plugged into the computer)
9. Plug it back in, and it should auto-detect and install, and work this time.
10. You should probably grab everything you can from the drive and not use it again.

### Update the Firmware ###

Update the firmware on the newly-revived Passport following instructions [here](http://www.wdc.com/wdproducts/wdsmartwareupdate/firmware.asp?id=wdfMyPassport&os=WIN).
