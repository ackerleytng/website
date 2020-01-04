---
slug: arduino-with-avrisp-mkii-crunchbang
date: "2014-07-17T00:00:00Z"
description: Setting up Arduino with CrunchBang Linux for pure C projects
tags:
- arduino
- arduino mega2560
- crunchbang
- linux
- C
- projects
- setup
title: Setting up Arduino with CrunchBang Linux for pure C projects
---
I'm powering the Arduino Mega 2560 board using USB. However, I'm going to program the Arduino using an AVRISP mkii programmer. [This site](http://allaboutee.com/2011/05/11/how-to-program-an-avr-microcontroller/) shows the pinout of the programmer, and upon comparison with the [Arduino schematic](http://arduino.cc/en/uploads/Main/arduino-mega2560_R3-sch.pdf), I've decided to use the programmer this way:

![Arduino Setup](/assets/images/arduino_setup.jpg)

Use apt-get to install packages

    sudo apt-get install gcc-avr binutils-avr gdb-avr avr-libc avrdude

To use avr-gcc to compile

	avr-gcc -DF_CPU=16000000UL -mmcu=atmega2560 -Os -o blink.out blink.c
	avr-objcopy -O ihex -R .eeprom blink.out blink.hex
	sudo avrdude -V -F -c avrisp2 -p m2560 -P usb -U flash:w:blink.hex
