---
slug: non-negative-less-than
date: "2020-06-07T08:42:00+08:00"
description: Investigating nonNegativeLessThan's implementation in Functional Programming in Scala
tags:
- random-number-generation
- scala
title: Why the condition in the nonNegativeLessThan implementation works
---

In Chapter 6 of Functional Programming in Scala, when we're trying to implement
`nonNegativeLessThan`, the condition to accept the generated random number
didn't make sense to me, so I dug into it a bit more.

```scala
def nonNegativeLessThan(n: Int): Rand[Int] = {
  nonNegativeInt.flatMap { i =>
    val mod = i % n
    if (i + (n - 1) - mod >= 0)
      State.unit(mod)
    else
      nonNegativeLessThan(i)
  }
```

Suppose instead of the regular `Int`, we used a 4-bit integer instead, which overflows after 15.

> We assume that the randomly generated numbers provided to `flatMap` will be
> between 0 and 15 (inclusive)

In this example, lets use `n = 6`. For the randomly generated numbers to be
evenly distributed between 0 and 5 (inclusive), we need to retry if the
randomly generated number is between 12 and 15 inclusive:

```
mod 0  1  2  3  4  5
    -----------------
    0  1  2  3  4  5
    6  7  8  9  10 11
    12 13 14 15 __ __  <== __ means it would have overflowed
```

We need to retry when the randomly generated number falls in the last row, so
that generated numbers from `nonNegativeLessThan` will be evenly distributed
between 0 and 5 (inclusive).

The condition `i + ((n - 1) - mod)` works because the number in the outer
parentheses `((n + 1) - mod)` is the number needed to increase any `i` to the
last number in a row.

Examples:

+ 6 + (6 - 1) - 0 = 11
+ 9 + (6 - 1) - 3 = 11
+ 13 + (6 - 1) - 1 = 17 (would have overflowed)
+ 14 + (6 - 1) - 2 = 17 (would have overflowed)

If `i % n = mod` where `i` is the dividend and `n` is the divisor, `i + n -
mod` will definitely round `i` up to the next multiple of `n`, so `i + n -
mod - 1` will round `i` up to just less than the next multiple of `n`.

Hence, if `i`, rounded up to just less than the next multiple of `n`, is still
positive (no overflow happened), the original number `i` must not be higher
than the largest multiple of `n` that fits in an `Int`.

Suppose now we use `n = 4` instead:

```
mod 0  1  2  3
    ----------
    0  1  2  3
    4  5  6  7
    8  9  10 11
    12 13 14 15
```

Examples:

+ 8 + (4 - 1) - 0 = 11 (no overflow, no need to retry)
+ 10 + (4 - 1) - 2 = 11 (no overflow, no need to retry)
+ 12 + (4 - 1) - 0 = 15 (no overflow, no need to retry)

If our condition had excluded the `- 1` part, as in if the condition had been
`i + n - mod` instead, then we would have retried for numbers `12 <= i <= 15`,
which would still result in a uniform distribution, but at a slight additional
computation cost, since it wasn't necessary to retry for numbers `12 <= i <=
15`.
