---
slug: emacs-tramp-terminator-integration
date: "2014-08-23T00:00:00Z"
description: Emacs-Tramp-Terminator-Integration
tags:
- emacs
- terminator
- tramp
- iterm
title: Emacs-Tramp-Terminator-Integration
---
iTerm2 has a feature called [Triggers](http://iterm2.com/triggers.html) which doesn't seem to exist in any of the Linux terminal emulators.

Terminator has a plugin system, so I hacked together something that would parse emacs-formatted 'urls' and open those urls in Emacs over Tramp. The concept of tying triggers with the terminal emulator is borrowed from my ECE MEng advisor, Prof. (Christopher Batten)[http://www.csl.cornell.edu/~cbatten/].

## Concept

The idea is as follows. ssh into the research server to access source code there. Instead of customizing Emacs on every server you work with, customize only one - the one on the computer that you ssh from.

Generate a string containing information about the current user and server IP address, and the path to the file you want to edit.

I do this using a bash function added to .bashrc on the remote server:

    # Remote emacsclient trigger
    function oe() {
        user=$(whoami)
        file=$(echo "$1" | tr -d ' ')
        hostname=$(hostname -I | tr -d ' ')
        workingdir=$(pwd | tr -d ' ')
        echo "remote-emacsclient-trigger[[[/$user@${hostname}:${workingdir}/${file}]]]"
    }

So say I'm in /home/user/ on the remote server and I'm working on blah.

    oe blah

will cause the remote server to echo

    remote-emacsclient-trigger[[[/user@123.123.123.123:/home/user/blah]]]


In iTerm2, the trigger can pick up the string and in turn start a coprocess with the line `emacsclient -c -n <the content between [[[ and ]]]>`, using regex matches.

The following plugin, written for Terminator, will give you a similar effect, except you have to right click on the part between `[[[` and `]]]`, and click open link.

[Download](/downloads/activate_emacs.py)

Place that file in /usr/share/terminator/terminatorlib/plugins/activate_emacs.py and restart Terminator, then right click and click Preferences, go to the Plugins tab and check the ActivateEmacs plugin.

## The process

There's little documentation on plugin writing, so it took a while to look through the examples and other plugins to start. Fortunately Terminator's code could mostly be found in /usr/share/terminator/, but unfortunately it still takes time to scan through all the code.

There are lots of functions in terminator's code to do with matching, but I believe those are only activated on mouseovers rather than as they appear in the terminal.

The URLHandler plugin sounds like it could parse any text or string - it can, but only on mouseovers. The `callback()` function is something that is meant to transform the 'url' that matched to another url for a web browser to open; it does not perform actions on the matched string directly.

[Jocelyn's comment](http://www.tenshu.net/2010/04/writing-terminator-plugins.html?showComment=1350573521137#c3847139789739776267) was so super useful in writing this plugin!
