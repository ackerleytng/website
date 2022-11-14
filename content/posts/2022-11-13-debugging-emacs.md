---
slug: debugging-emacs
date: 2022-11-13T21:02:45-08:00
description: Notes on debugging emacs
tags:
- debugging
- emacs
title: Notes on debugging emacs
---

## debug-on-error

```
(setq debug-on-error t)
```

When emacs hits an error, this will show a backtrace.

This is useful to get an idea of where the error is and how we got to the error.

## Profiler

Emacs code tends to use a lot of variables (like global variables, or customizable variables) that aren't passed through function parameters. Also, functions tend to have different stages where elisp statements might be used, so it helps to know which statements were evaluated before getting to the point of error.

After figuring out the source of the error, we can pick one of the functions near the source of the call chain, and activate the profiler on it.

### Manual activation

Doing an `M-x (profiler-start 'cpu)` and then `M-x (profiler-stop)` and then `M-x (profiler-report)` works, but it tends to introduce a lot of noise from the elisp triggered by `M-x`.

### Single-keystroke to start and stop the profiler

```
(global-set-key [f12] (lambda () (profiler-start 'cpu)))
(global-set-key [f11] (lambda () (profiler-stop)))
```

Set some keybindings and then use a single key to start and stop the profiler, to remove some noise.

### Editing code

Make a copy of the function you want to profile, and insert `(profiler-start 'cpu)` at the beginning and `(profiler-end)` at the end, then trigger the function, and then do `M-x (profiler-report)` to show what code was executed.

> Perhaps there's a better way, something like `(profile-function)` maybe?

## Instrumenting for debugging

Hitting `C-u C-M-x` while the cursor is in your function of interest puts the function in debug mode.

When the function is next executed, you'll be able to step through the function.

This is a good way to inspect all the local variables within the function as the function progresses.

In this mode, hit `e` to evaluate any elisp.

Hitting `d` will show a backtrace, which is useful to see where we are in the entire call chain.

Full documentation is at [Edebug mode](https://www.gnu.org/software/emacs/manual/html_node/elisp/Edebug.html)
