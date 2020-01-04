---
slug: setting-up-nfs-server-in-lxd-container
date: "2016-09-06T00:00:00Z"
description: Instructions to set up NFS server in lxd container
tags:
- nfs-server
- container
- lxd
title: Setting up NFS server in lxd container
---
In the lxd host, suppose you have the following containers

```
$ lxc list
+------------+---------+-----------------------+------+------------+-----------+
|    NAME    |  STATE  |         IPV4          | IPV6 |    TYPE    | SNAPSHOTS |
+------------+---------+-----------------------+------+------------+-----------+
| base       | STOPPED |                       |      | PERSISTENT | 0         |
+------------+---------+-----------------------+------+------------+-----------+
| nfs-server | RUNNING | 192.168.31.135 (eth0) |      | PERSISTENT | 0         |
+------------+---------+-----------------------+------+------------+-----------+
```

Make nfs-server a privileged container

```
$ lxc config set nfs-server security.privileged true
```

and get apparmor to allow nfs-server stuff

```
$ lxc config set nfs-server raw.apparmor 'mount fstype=nfs*, mount fstype=rpc_pipefs,'
```

Then reboot.

In the lxd container,

```
apt-get install nfs-kernel-server
```

and use regular instructions to set up nfs.

Check that nfs-server is up using

```
$ sudo systemctl status nfs-server
[sudo] password for user: 
● nfs-server.service - NFS server and services
   Loaded: loaded (/lib/systemd/system/nfs-server.service; enabled; vendor preset: enabled)
   Active: active (exited) since Tue 2016-09-06 15:57:33 UTC; 37s ago
  Process: 339 ExecStart=/usr/sbin/rpc.nfsd $RPCNFSDARGS (code=exited, status=0/SUCCESS)
  Process: 338 ExecStartPre=/usr/sbin/exportfs -r (code=exited, status=0/SUCCESS)
 Main PID: 339 (code=exited, status=0/SUCCESS)
    Tasks: 0
   Memory: 0B
      CPU: 0
   CGroup: /system.slice/nfs-server.service
```
