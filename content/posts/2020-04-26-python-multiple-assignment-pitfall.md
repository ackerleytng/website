---
slug: python-multiple-assignment-pitfall
date: "2020-04-26T21:32:00+08:00"
description: python multiple-assignment pitfall
tags:
- python
- pitfall
title: python multiple-assignment pitfall
---

Fell into a pit while trying to reverse a linked list!

Here's the typical definition of a Node in a linked list

```
class Node:
    def __init__(self, val, next):
        self.val = val
        self.next = next

# To save typing:
N = Node
```

I set out to reverse a linked list with this template, because I wanted to
start off by making sure that the loop advances.

```
def reverse(head):
    rev = None
    p = head
    while p is not None:

        ...

        p = p.next
```

Continuing from there, I would then actually do the reversal using python's
multiple assignments

```
def reverse(head):
    rev = None
    p = head
    while p is not None:
        p, p.next, rev = p.next, rev, p

    return rev
```

I ran it on my little test case

```
def test_reverse():
    head = N(1, N(2, N(3, None)))
    rev = reverse(head)
    assert rev.val == 3
    assert rev.next.val == 2
    assert rev.next.next.val == 1
    assert rev.next.next.next is None
```

And promptly got a `AttributeError: 'NoneType' object has no attribute 'next'`!

It turns out that when using python's multiple assignments, the tuple on the
right of the assignment is evaluated completely, but there is still an order to
the assignments on the left, and the assignments go from left to right.

This means, on the third iteration of the loop above, `p` is assigned `None`,
then `p.next` is evaluated to try and assign `rev` to the `next` attribute of
`None`, which fails.

The fix is simply to swap the order around so that the assignment of `p.next`
to `p` goes last:

```
def reverse(head):
    rev = None
    p = head
    while p is not None:
        rev, p.next, p = p, rev, p.next

    return rev
```

Here are the details from Python's bytecode disassembly:

```
$ python
Python 3.8.2 (default, Feb 29 2020, 11:29:25)
[GCC 9.2.1 20200130] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dis
>>> dis.dis("rev, p.next, p = p, rev, p.next")
  1           0 LOAD_NAME                0 (p)
              2 LOAD_NAME                1 (rev)
              4 LOAD_NAME                0 (p)
              6 LOAD_ATTR                2 (next)
              8 ROT_THREE
             10 ROT_TWO
             12 STORE_NAME               1 (rev)
             14 LOAD_NAME                0 (p)
             16 STORE_ATTR               2 (next)
             18 STORE_NAME               0 (p)
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
>>>
```

> [Here's](https://stackoverflow.com/a/47529318/2108690) what the columns in that output mean

Here's a visualization of the progress

| after instruction offset | stack        | notes                  |
| ------------------------ | -----        | -----                  |
| 0                        | p            |                        |
| 2                        | p, rev       |                        |
| 6                        | p, rev, next |                        |
| 8                        | next, p, rev |                        |
| 10                       | next, rev, p |                        |
| 12                       | next, rev    | p stored into rev      |
| 16                       | next         | rev stored into p.next |
| 18                       |              | next stored into p     |
