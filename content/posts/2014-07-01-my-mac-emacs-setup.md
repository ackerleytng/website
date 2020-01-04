---
slug: my-mac-emacs-setup
date: "2014-07-01T00:00:00Z"
tags:
- emacs
- mac
- setup
title: My Mac-Emacs Setup
---
## 1. Emacs distribution

There are a few distributions of Emacs, and I was looking for the cleanest, most vanilla Emacs, without sacrificing convenience. I went with emacs-app from Macports.

The version I got was 24.3.1.

{{< highlight bash >}}

sudo port install emacs-app

{{< / highlight >}}

## 2. Running Emacs as a Daemon

Advantage of running Emacs as a Daemon: all Emacs instances initialized from the Terminal will use the same Emacs process, allowing all of them to share the same buffers, command history etc.

The idea here is to get OSX to start the daemon, aka Emacs server, when the system starts up, and then subsequently, emacsclient is used to connect to that server.

There are some ways of starting the Emacs daemon automatically on system startup. I chose to use launchd because it felt like the cleanest method.

### Writing plist file

OSX can be configured to read plist files on startup and start the Emacs daemon. Find out more about writing the plist file from [Apple](https://developer.apple.com/library/mac/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html).

{{< highlight xml >}}

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>gnu.emacs.daemon.plist</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Applications/MacPorts/Emacs.app/Contents/MacOS/Emacs</string>
    <string>--daemon</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>ServiceDescription</key>
  <string>Gnu Emacs Daemon</string>
  <key>UserName</key>
  <string>[Your Username]</string>
</dict>
</plist>

{{< / highlight >}}

The above plist file was named gnu.emacs.daemon.plist and was placed in the ~/Library/LaunchAgents/ directory.

I chose the user's LaunchAgents Directory as opposed to the system one to make this start only with my account.

### Checking to see that the daemon starts

At this point, restart OSX.

After restarting, to check that the daemon is running, open a Terminal window and do

{{< highlight bash >}}

ps aux | grep Emacs

{{< / highlight >}}

If it is running, you should see a process with this name

{{< highlight bash >}}

/Applications/MacPorts/Emacs.app/Contents/MacOS/Emacs --daemon

{{< / highlight >}}

### Configuring Terminal to work with the daemon

To do this simply, I set up two aliases in ~/.bash_profile

{{< highlight bash >}}

alias oe="/Applications/MacPorts/Emacs.app/Contents/MacOS/bin/emacsclient -c -n"
alias oie="/Applications/MacPorts/Emacs.app/Contents/MacOS/bin/emacsclient -n"
alias ed="/Applications/MacPorts/Emacs.app/Contents/MacOS/Emacs --daemon"

{{< / highlight >}}

oe is the command I use to open files, such as

{{< highlight bash >}}

oe foobar.txt

{{< / highlight >}}

and ed is used to start the daemon again in case the daemon was shut down.

Using -c uses a graphical frame, otherwise if there is no existing graphical frame, nothing appears to happen in the terminal.

oie allows me to open a file in an existing frame, if I choose to.

Using -n allows you to continue using the same terminal window even after Emacs is opened.

Using the above brings focus to the newly-opened Emacs window and away from the Terminal window.

### Closing the daemon

If there's a need to close the daemon for whatever reason, just press Cmd+Q (on an open Emacs frame - it doesn't work if you do that without an open Emacs frame) as you would for any other OSX program.

## 3. Important emacs config

This section contains emacs configuration files that I love to use

### Setting default window size

{{< highlight lisp >}}

(add-to-list 'default-frame-alist '(height . 58))
(add-to-list 'default-frame-alist '(width . 144))

{{< / highlight >}}

### Moving all backups to Trash

To remove clutter:

{{< highlight lisp >}}

(setq backup-directory-alist '(("." . "~/.Trash")))

{{< / highlight >}}

### [Multiple Cursors](https://github.com/emacsmirror/multiple-cursors)!

Installation instructions are available [here](https://github.com/emacsmirror/multiple-cursors), and you can explore the power of multiple cursors from this [YouTube Video](http://emacsrocks.com/e13.html).

## 4. Finally

The above combines information from various different sites.

Drop me a note if you've been here and found this useful (or not useful), or if you have questions! It's my first contribution to the Internet, which has been helping me so much. Hope this will help many other people :).
