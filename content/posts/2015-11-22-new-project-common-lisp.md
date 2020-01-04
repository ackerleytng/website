---
slug: new-project-common-lisp
date: "2015-11-22T00:00:00Z"
description: This post helps people to start a new project in Common Lisp. It also
  explains how to use slime together with asdf and packages.
tags:
- slime
- common lisp
- packages
title: Starting a new project in Common Lisp
---
Is it fair to say that there aren't that many up-to-date books for common lisp that would help a beginner who doesn't want to start with a prebuilt environment?

I want to try and set up as much of my own environment as possible because

- I don't want to download multiple environments for my computer
- I want to know how the environment was set up so that I will know how to replicate it

There are many good books but a lot of them use old syntax, or they don't explain how to work with quicklisp...

The Common Lisp world feels fragmented because there are so many ways to do things, and many guides (if the guides exist) assume a certain setup. This makes the guide difficult to follow if you don't want to start at the beginning. I think this is probably a side effect of the power of lisp - people can build entire environments on their own, and they become so used to it that they forget what it is like for a beginner. These people are the ones who write books, so that makes it really difficult to understand for a beginner.

Anyway.

# Setup

So quicklisp is like a package manager for existing lisp projects. It's something like gems for ruby and pip for python. You need it. [Install it from here.](https://www.quicklisp.org/beta/) If you don't need the package vecto you can skip all the vecto stuff, but remember this `(ql:add-to-init-file)`. We want quicklisp to autostart with sbcl.

Then, we want to enable asdf in slime, in emacs. Go to your `.emacs` file, make sure you see `slime-asdf` in this list:

```
(setq slime-contribs '(slime-fancy slime-asdf))
```

This will enable `slime-load-system` later to load `.asd` files.

# How to start programming

Start sbcl, then first load quickproject with quicklisp, then use quickproject to make your project.

```
$ sbcl
This is SBCL 1.3.0, an implementation of ANSI Common Lisp.
More information about SBCL is available at <http://www.sbcl.org/>.

SBCL is free software, provided as is, with absolutely no warranty.
It is mostly in the public domain; some portions are provided under
BSD-style licenses.  See the CREDITS and COPYING files in the
distribution for more information.
* (ql:quickload :quickproject)
To load "quickproject":
  Load 1 ASDF system:
    quickproject
; Loading "quickproject"

(:QUICKPROJECT)
* (quickproject:make-project #p"~/src/test/" :depends-on '(cl-ppcre))

"myproject"
```

That creates a project in `~/src/test/` and makes it depend on `cl-ppcre`.

I think of `quickproject` as something like `rails new <project>`. It builds you a skeleton. This is the skeleton.

```
$ ls
README.txt   package.lisp test.asd     test.lisp
```

I think `package.lisp` is like a C header file, except that it is all headers in one.

`test.asd` is like a `Gemfile`, which defines the packages, the files, the dependencies.

`test.lisp` is where you want to be programming in.

Now open `test.asd` in emacs.

The repl should start on it's own, presenting you with a `CL-USER>` prompt. `CL-USER` is actually the package that you're currently working in.

I'll add something to `test.lisp` so we can test it.

```
(defun hello-world ()
  'hello-world)
```

Compile `test.asd`. With your cursor in `test.asd`'s frame, press `C-c C-k`. Then load the system using `M-x slime-load-system` and then pick `test` as the system to load. Now go over to the repl frame, and then you want to switch to the package that you're working on. Pick one of two ways:

+ type `(in-package :test)` at the repl
+ press `,` at the prompt to use slime shortcuts, then type either 
  + `!p`
  + `change-package`

Now in the repl frame,

```
TEST> (hello-world)
HELLO-WORLD
```

Now I want to start using `cl-ppcre`.

Go to `package.lisp`, modify the form to look like this

```
(defpackage #:test
  (:use #:cl #:cl-ppcre))
```

Then go to `test.lisp` and add the following

```
(defun my-scan ()
  (scan "(a)*b" "xaaabd"))
```


Now do `M-x slime-reload-system`.

In the repl, try `(my-scan)`.

That should not produce an error. :)


