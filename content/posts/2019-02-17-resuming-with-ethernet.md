---
slug: resuming-with-ethernet
date: "2019-02-17T00:00:00Z"
description: Resuming with Ethernet
tags:
- arch
- ethernet
- suspend
- resume
title: Resuming with Ethernet
---

I had this strange issue on Arch where I would not have internet connection after waking from suspend.

I was suspending the desktop through i3, with

```
bindsym $mod+bracketright exec --no-startup-id $lock_command && systemctl suspend
```

in `~/.config/i3/config`

When the computer resumes from suspend, it would not be able to connect to the Internet for a while.

`tcpdump` on my home router (also my DNS/DHCP server) would show no DHCP requests.

`dig www.google.com` on the computer would just not respond for about 40 seconds, and after 40 seconds, the connection would magically revive itself again.

I looked at `systemd-networkd` and `systemd-resolved` but logs and configuration of both of those seemed correct.

I took a while to realize that there was some issue with some component of the network interface on the physical layer, because `ip link` would show `NO-CARRIER`.

```
enp2s0: <NO-CARRIER,BROADCAST,MULTICAST,UP>
```

There was definitely no wiring issues, since all I did was to suspend and resume the computer.

After following some guides on forums, it appears that a possible workaround would be to stop the interface before suspending and then start it on resume, so here are the systemd service files to make that work:

```
$ cat /etc/systemd/system/root-suspend.service
[Unit]
Description=Stop network interface before sleep
Before=sleep.target

[Service]
User=root
Type=oneshot
ExecStart=/usr/bin/ip link set enp0s31f6 down
TimeoutSec=0
StandardOutput=syslog

[Install]
WantedBy=sleep.target
```

```
$ cat /etc/systemd/system/root-resume.service
[Unit]
Description=Stop network interface before sleep
After=suspend.target

[Service]
User=root
Type=oneshot
ExecStart=/usr/bin/ip link set enp0s31f6 up
TimeoutSec=0
StandardOutput=syslog

[Install]
WantedBy=suspend.target
```

And we need to enable those two

```
sudo systemctl enable root-suspend.service
sudo systemctl enable root-resume.service
```
