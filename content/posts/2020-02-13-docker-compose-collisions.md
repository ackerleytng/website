---
slug: docker-compose-collisions
date: "2020-02-13:00:00Z"
description: docker-compose collisions
tags:
- docker
- collisions
- containers
- docker-compose
title: docker-compose collisions
---

Here's a description of collisions between groups of services described in similar docker-compose files, in different directories, when they are brought up on the same host with `docker-compose up`

I think of them as "collisions" because when using different `docker-compose.yml` files in different directories, I tend to think of them as different instances, even if they are of the same groups of services.

`docker-compose` actually identifies services using a combination of service name (declared in the file) and the [project name](https://docs.docker.com/compose/reference/envvars/#compose_project_name), which defaults to the directory containing `docker-compose.yml`.

Consider a simple service described in a `docker-compose.yml` file, in `service-instance-a/`: (let this be the first instance that later scenarios refer to)

```
$ cat service-instance-a/docker-compose.yml
version: "3"
services:
  nginx:
    image: nginx:stable-alpine
$
```

Start that, and it should start as expected.

Now if you copy that entire directory `cp -r service-instance-a/ service-instance-b/`, and `docker-compose up` from `service-instance-b/`, the same service starts as expected, and both instances can be stopped independently. (Keep this instance running, it should not be affected by the scenarios below)

Now once the containing directory is the same, docker-compose starts to treat them as the same project.

Suppose you have

```
$ cat same-instance-a/service-instance-a/docker-compose.yml
version: "3"
services:
  nginx:
    image: nginx:stable-alpine
$
```

And now you `cd same-instance-a/service-instance-a/` and do `docker-compose up`, you'll see that it starts fine, but it's actually a related instance to the first one (`service-instance-a/docker-compose.yml`). If you start both, send `Ctrl-C` on either one, and the other will go down as well.

If you try and fix that problem by changing the container name, that's actually worse - docker-compose thinks you have changed a configuration of the previous instance, and promptly shuts down the first instance.

```
$ cat different-container-name/service-instance-a/docker-compose.yml
version: "3"
services:
  nginx:
    image: nginx:stable-alpine
    container_name: different-nginx
$
```

This also applies if you change any other configuration, like if you decided to try and fix the problem by trying to connect the second instance to another network - docker-compose also shuts down the first instance.

```
$ cat different-network/service-instance-a/docker-compose.yml
version: "3"
services:
  nginx:
    image: nginx:stable-alpine
    networks:
      - foobar

networks:
  foobar:
$
```

Finally, if you try and rename the service, docker-compose still thinks it's part of the same project!

```
$ cat different-service-name/service-instance-a/docker-compose.yml
version: "3"
services:
  nginx-renamed:
    image: nginx:stable-alpine
$
```

Now if you start this one, you get

```
$ docker-compose up
WARNING: Found orphan containers (service-instance-a_nginx_1) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Creating service-instance-a_nginx-renamed_1 ... done
Attaching to service-instance-a_nginx-renamed_1
```

docker-compose thinks you renamed a container in the same project as the other running one, and recommends that you clean up the orphans. On the bright side, the other container is still up and running.

Here's a repo with all the scenarios in case you want to try it out: https://github.com/ackerleytng/docker-compose-collisions

> I ran into this issue while assuming that making a copy of `docker-compose.yml` in another directory with the same name would allow me to run two instances of the same service, allowing me to keep one service running while trying out another configuration - except I ended up bringing both services down :(
