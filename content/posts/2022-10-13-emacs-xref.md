---
slug: emacs-xref
date: "2022-10-13T22:00:00-07:00"
description: "Understanding emacs' xref mode and exploring supporting multiple backends"
tags:
- emacs
- xref
title: "Understanding emacs' xref mode and exploring supporting multiple backends"
---

`xref` is a pluggable emacs subsystem to quickly find where identifiers are defined and referenced, and for quick renaming, etc.

Every module that plugs into `xref` must provide a constructor function that returns a backend value and a set of methods:

+ `xref-backend-identifier-at-point`
+ `xref-backend-identifier-completion-table`
+ `xref-backend-definitions`
+ `xref-backend-references`
+ `xref-backend-apropos`

## `xref-backend-identifier-at-point`

This method should return a string, which will later be passed to other functions like `xref-backend-definitions`, `xref-backend-references` or `xref-backend-apropos` which will use this string to find definitions, references, etc.

This allows different backends to determine what constitutes an "identifier" independently. For example, if the cursor is on `foo-bar`, a lisp backend might pick up `"foo-bar"` as an identifier, while a C backend might just pick up `"foo"`, since the `-` would be another symbol in C.

Because `xref-backend-identifier-at-point` needs to will be called with the backend's corresponding search function, like `xref-backend-definitions`, the backend can choose to encode anything into the string.

[`gxref`](https://github.com/dedi/gxref/) uses a relatively straightforward implementation. Its [`xref-backend-identifier-at-point`](https://github.com/dedi/gxref/blob/380b02c3c3c2586c828456716eef6a6392bb043b/gxref.el#L377) delegates the task of finding a symbol to emacs' `symbol-at-point` and returns the symbol. This works well with its `xref-backend-definitions` method, which takes that string and sends it off to `gtags` for the actual search.

[`eglot`](https://github.com/joaotavora/eglot) takes the result of `symbol-at-point` as a pattern and makes a `:workspace/symbol` request to the language server to get the symbols for that pattern.

The backend can also return nil to indicate no identifier found.

## `xref-backend-identifier-completion-table`

This method should return either a list of strings, or an associative array like `'((<human-readable string>, <actual value>))`. Examples can be found here: http://www.howardism.org/Technical/Emacs/alt-completing-read.html

This method will be called when `xref-backend-identifier-at-point` returns `nil`, in which case this function will be invoked to provide a list of options for the user to pick an identifier.

One use case I can think of is when the backend can find more than one possible identifier when `xref-backend-definitions` is invoked. The backend can then return `nil` for `xref-backend-identifier-at-point` and return a completion table for the user to choose an identifier from the list.

## `xref-backend-identifier-completion-ignore-case`

This method should return `t` if case is significant in identifier completion and `nil` otherwise.

## `xref-backend-definitions`

This method will be called with the identifier from `xref-backend-identifier-at-point`, and should return

+ one xref object if the unique definition can be determined, otherwise
+ a list of xref objects for possible definitions,
+ and `nil` if no definitions can be found.

## `xref-backend-references`

This method will be called with the identifier from `xref-backend-identifier-at-point`, and should return

+ a list of xref objects, one for each reference,
+ and `nil` if no references can be found.

## `xref-backend-apropos`

This method will be called with the pattern from `xref-backend-identifier-at-point`, and should return

+ a list of xref objects, one for each location that could be meaningful given a pattern,
+ and `nil` if no definitions can be found.

`apropos` is a fuzzy way of returning anything meaningful. In `gxref` for example, `xref-backend-apropos` delegates to the `-g` flag of gtags, which does a grep-like search over the indexed symbols.

# Exploring lettng xref use multiple backends

## Common case

I expect that most users will have just a few backends, perhaps `eglot`, then `gtags`, `cscope`, and a fallback option like `grep`. This should limit the number of external calls emacs has to make.

## Constraints

1. The identifier provided by the backend must be provided to the same backend as per API contract. This will allow encoding of search parameters in the identifier.
2. We want to minimize the number of user prompts in the happy case where the identifier can be identified.

## Finding definitions/references

1. Poll each of the backends for an identifier, add (backend, identifier) to an associative list.
2. If none of the backends returned an identifier, prompt the user for an identifier based on the highest-priority backend.
    a. Usually, when all the backends returned any identifiers, it means the user probably intended to request the backend for a list of relevant symbols (invoke `xref-backend-identifier-completion-table`) of a certain backend. Asking the user to choose a backend at this stage would probably be too many prompts.
    b. We expect that the user prefers to get the identifier completion table from the highest-priority backend and so we just query the identifier from that one backend and proceed.
    c. If the user prefers to use another backend in this situation, the user can re-order `xref-backend-functions` to set up the preference correctly.
3. For each pair in the associative list, call `xref-backend-definitions` or `xref-backend-references`.
4. Return results. For each result, add the backend name for presentation to the user.

There may be duplicate results (by location), but we expect `xref-show-definitions-function` or `xref-show-xrefs-function` to handle deduplication.
This allows the display function to use that additional frequency information, perhaps to sort the results by frequency when displaying results.

## New behavior

Previously, all of these would have used a single backend. Here's the new behavior:

| Functionality                                                                                                                    | New Behavior                      |
|----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| `xref-find-definitions`/`xref-find-definitions-other-frame`/`xref-find-definitions-other-window`                                 | Uses more than one backend        |
| C-u `xref-find-definitions`/`xref-find-definitions-other-frame`/`xref-find-definitions-other-window`                             | Uses the highest priority backend |
| `xref-find-definitions`/`xref-find-definitions-other-frame`/`xref-find-definitions-other-window` when no identifier can be found | Uses the highest priority backend |
| `xref-find-references`                                                                                                           | Uses more than one backend        |
| C-u `xref-find-references`                                                                                                       | Uses the highest priority backend |
| `xref-find-references` when no identifier can be found                                                                           | Uses the highest priority backend |
| `xref-find-apropos`                                                                                                              | Uses the highest priority backend |
| `xref-find-definitions-at-mouse`                                                                                                 | Uses more than one backend        |
| `xref-find-references-at-mouse`                                                                                                  | Uses more than one backend        |

# Other required fixes

## Suppressing etags' prompt for TAGS file

Since etags is the default backend for xref, it would be really annoying, once we enable multiple backends, if etags prompts for a TAGS file when we want to just skip the use of etags.

This should be a customizable option: skip the use of etags if a TAGS file is not set. (To set the tags file, we would just manually invoke `visit-tags-table` before using `xref`.

To skip etags as a completion, we have 2 options.

1. Let `xref-backend-identifier-at-point` return `nil`
2. Let `xref-backend-definitions` return `nil`

I'm going with 2 since it feels more "correct" - identifiers can be extracted even if a TAGS file isn't available, but definitions can't be found if a TAGS file isn't available.
