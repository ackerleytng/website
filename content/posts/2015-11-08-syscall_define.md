---
slug: syscall_define
date: "2015-11-08T00:00:00Z"
description: SYSCALL_DEFINE
tags:
- linux
- kernel
title: SYSCALL_DEFINE
---
I think macros are pretty interesting... Really wanted to take some time to understand what this particular one means!

For this post, I'll use Linux 4.3, the latest stable version at the point of writing.

To put things in context, let's get a concrete example of a syscall -- read.

```
SYSCALL_DEFINE3(read, unsigned int, fd, char __user *, buf, size_t, count)
{
        struct fd f = fdget_pos(fd);
        ssize_t ret = -EBADF;

        if (f.file) {
                loff_t pos = file_pos_read(f.file);
                ret = vfs_read(f.file, buf, count, &pos);
                if (ret >= 0)
                        file_pos_write(f.file, pos);
                fdput_pos(f);
        }
        return ret;
}
```

The macro SYSCALL_DEFINE3 is defined in `include/linux/syscalls.h`.

```
#define SYSCALL_DEFINE1(name, ...) SYSCALL_DEFINEx(1, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE2(name, ...) SYSCALL_DEFINEx(2, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE3(name, ...) SYSCALL_DEFINEx(3, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE4(name, ...) SYSCALL_DEFINEx(4, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE5(name, ...) SYSCALL_DEFINEx(5, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE6(name, ...) SYSCALL_DEFINEx(6, _##name, __VA_ARGS__)
```

Applying that macro, we have

```
SYSCALL_DEFINEx(3, _read, unsigned int, fd, char __user *, buf, size_t, count)
{
        struct file *file;
        ...
```

`SYSCALL_DEFINEx` is defined as

```
#define SYSCALL_DEFINEx(x, sname, ...)                          \
        SYSCALL_METADATA(sname, x, __VA_ARGS__)                 \
        __SYSCALL_DEFINEx(x, sname, __VA_ARGS__)
```

I'll deal with `__SYSCALL_DEFINEx` first.


```
#define __SYSCALL_DEFINEx(x, name, ...)                                 \
        asmlinkage long sys##name(__MAP(x,__SC_DECL,__VA_ARGS__))       \
                __attribute__((alias(__stringify(SyS##name))));         \
        static inline long SYSC##name(__MAP(x,__SC_DECL,__VA_ARGS__));  \
        asmlinkage long SyS##name(__MAP(x,__SC_LONG,__VA_ARGS__));      \
        asmlinkage long SyS##name(__MAP(x,__SC_LONG,__VA_ARGS__))       \
        {                                                               \
                long ret = SYSC##name(__MAP(x,__SC_CAST,__VA_ARGS__));  \
                __MAP(x,__SC_TEST,__VA_ARGS__);                         \
                __PROTECT(x, ret,__MAP(x,__SC_ARGS,__VA_ARGS__));       \
                return ret;                                             \
        }                                                               \
        static inline long SYSC##name(__MAP(x,__SC_DECL,__VA_ARGS__))
```

`asmlinkage` is a macro too!

```
#define asmlinkage CPP_ASMLINKAGE __attribute__((regparm(0)))
```

This is an instruction to gcc to expect to get all the arguments for this function from the stack.

`__MAP` is an amazing macro, and the following comment in the code is quite descriptive:

```
/*
 * __MAP - apply a macro to syscall arguments
 * __MAP(n, m, t1, a1, t2, a2, ..., tn, an) will expand to
 *    m(t1, a1), m(t2, a2), ..., m(tn, an)
 * The first argument must be equal to the amount of type/name
 * pairs given.  Note that this list of pairs (i.e. the arguments
 * of __MAP starting at the third one) is in the same format as
 * for SYSCALL_DEFINE<n>/COMPAT_SYSCALL_DEFINE<n>
 */
#define __MAP0(m,...)
#define __MAP1(m,t,a) m(t,a)
#define __MAP2(m,t,a,...) m(t,a), __MAP1(m,__VA_ARGS__)
#define __MAP3(m,t,a,...) m(t,a), __MAP2(m,__VA_ARGS__)
#define __MAP4(m,t,a,...) m(t,a), __MAP3(m,__VA_ARGS__)
#define __MAP5(m,t,a,...) m(t,a), __MAP4(m,__VA_ARGS__)
#define __MAP6(m,t,a,...) m(t,a), __MAP5(m,__VA_ARGS__)
#define __MAP(n,...) __MAP##n(__VA_ARGS__)
```

`__SC_DECL` is also a macro!

```
#define __SC_DECL(t, a) t a
```

The kernel code uses this `__SC_DECL` to declare parameters in the function.

So, in the first line after `SYSCALL_DEFINEx`, we have

```
__MAP(x,__SC_DECL,__VA_ARGS__)
```

More concretely, we have 

```
__MAP(3,__SC_DECL, unsigned int, fd, char __user *, buf, size_t, count)
```

```
__MAP3(__SC_DECL, unsigned int, fd, char __user *, buf, size_t, count)
```

```
__SC_DECL(unsigned int, fd), __MAP2(__SC_DECL, char __user *, buf, size_t, count)
```

```
__SC_DECL(unsigned int, fd), __SC_DECL(char __user *, buf), __MAP1(__SC_DECL, size_t, count)
```

```
__SC_DECL(unsigned int, fd), __SC_DECL(char __user *, buf), __SC_DECL(size_t, count)
```

And then `__SC_DECL` is also a macro,

```
#define __SC_DECL(t, a) t a
```

So we have

```
unsigned int fd, char __user * buf, size_t count
```

Hence, the first line of `__SYSCALL_DEFINEx` expands to

```
asmlinkage long sys_read(unsigned int fd, char __user * buf, size_t count) __attribute__((alias("SyS_read")))
```

Now what is an `alias`? It's a gcc [attribute](https://gcc.gnu.org/onlinedocs/gcc/Common-Function-Attributes.html#Common-Function-Attributes). From the [gcc site](https://gcc.gnu.org/onlinedocs/gcc/Common-Function-Attributes.html#Common-Function-Attributes), "The alias attribute causes the declaration to be emitted as an alias for another symbol, which must be specified."

So as I understand it, `sys_read` is now the same thing as `SyS_read`. The following line declares the function,

```
asmlinkage long SyS##name(__MAP(x,__SC_LONG,__VA_ARGS__)); 
```

And these lines define it:

```
asmlinkage long SyS##name(__MAP(x,__SC_LONG,__VA_ARGS__))       \
{                                                               \
        long ret = SYSC##name(__MAP(x,__SC_CAST,__VA_ARGS__));  \
        __MAP(x,__SC_TEST,__VA_ARGS__);                         \
        __PROTECT(x, ret,__MAP(x,__SC_ARGS,__VA_ARGS__));       \
        return ret;                                             \
}                                                               \
```

Notice that the same `__MAP` macro is used to apply `__SC_LONG` in the declaration and definition of `SyS_read`.

```
#define __TYPE_IS_L(t)  (__same_type((t)0, 0L))
#define __TYPE_IS_UL(t) (__same_type((t)0, 0UL))
#define __TYPE_IS_LL(t) (__same_type((t)0, 0LL) || __same_type((t)0, 0ULL))
#define __SC_LONG(t, a) __typeof(__builtin_choose_expr(__TYPE_IS_LL(t), 0LL, 0L)) a
```

I believe `__SC_LONG` checks the type of `t` and generates `long long a` or `long a` based on whether `t` was originally of type `long long`. Isn't it interesting that the preprocessor can generate code based on macro arguments?

The result of `__MAP`ing `__SC_LONG` is

```
asmlinkage long SyS_read(long fd, long buf, long count)
```

In the next line, we have

```
long ret = SYSC##name(__MAP(x,__SC_CAST,__VA_ARGS__));
```

`__SC_CAST` is relatively simple, it just basically casts the input arguments to the types suitable for `SYSC_read`.

```
#define __SC_CAST(t, a) (t) a
```

So `SyS_read` calls `SYSC_read`, then saves the result in `ret`. In the next line, we have

```
__MAP(x,__SC_TEST,__VA_ARGS__);
```

Following that macro in the code, we have

```
#define __SC_TEST(t, a) (void)BUILD_BUG_ON_ZERO(!__TYPE_IS_LL(t) && sizeof(t) > sizeof(long))
```

`BUILD_BUG_ON_ZERO` is pretty interesting. This [stackoverflow question](http://stackoverflow.com/questions/9229601/what-is-in-c-code) has a really good explanation of what this does.

`BUILD_BUG_ON_ZERO` is, I [quote](http://stackoverflow.com/questions/9229601/what-is-in-c-code), "a way to check whether the expression e can be evaluated to be 0, and if not, to fail the build."

So the line

```
__MAP(x,__SC_TEST,__VA_ARGS__);
```

tests the type of each argument. After applying de Morgan's theorem (because of `ON_ZERO` in `BUILD_BUG_ON_ZERO`), each argument must either be of type `long long`, or have a bitwidth less than or equal to that of `long`.

Moving on to the next line, `__SC_ARGS` basically extracts the argument and drops the type:

```
#define __SC_ARGS(t, a) a
```

`__PROTECT` is a macro, defined as

```
#define __PROTECT(...) asmlinkage_protect(__VA_ARGS__)
```

Its function is well-explained in the comment:

```
/*
 * Make sure the compiler doesn't do anything stupid with the
 * arguments on the stack - they are owned by the *caller*, not
 * the callee. This just fools gcc into not spilling into them,
 * and keeps it from doing tailcall recursion and/or using the
 * stack slots for temporaries, since they are live and "used"
 * all the way to the end of the function.
 *
 * NOTE! On x86-64, all the arguments are in registers, so this
 * only matters on a 32-bit kernel.
 */
#define asmlinkage_protect(n, ret, args...) \
        __asmlinkage_protect##n(ret, ##args)
#define __asmlinkage_protect_n(ret, args...) \
        __asm__ __volatile__ ("" : "=r" (ret) : "" (ret), ##args)
#define __asmlinkage_protect0(ret) \
        __asmlinkage_protect_n(ret)
#define __asmlinkage_protect1(ret, arg1) \
        __asmlinkage_protect_n(ret, "m" (arg1))
#define __asmlinkage_protect2(ret, arg1, arg2) \
        __asmlinkage_protect_n(ret, "m" (arg1), "m" (arg2))
#define __asmlinkage_protect3(ret, arg1, arg2, arg3) \
        __asmlinkage_protect_n(ret, "m" (arg1), "m" (arg2), "m" (arg3))
#define __asmlinkage_protect4(ret, arg1, arg2, arg3, arg4) \
        __asmlinkage_protect_n(ret, "m" (arg1), "m" (arg2), "m" (arg3), \
                              "m" (arg4))
#define __asmlinkage_protect5(ret, arg1, arg2, arg3, arg4, arg5) \
        __asmlinkage_protect_n(ret, "m" (arg1), "m" (arg2), "m" (arg3), \
                              "m" (arg4), "m" (arg5))
#define __asmlinkage_protect6(ret, arg1, arg2, arg3, arg4, arg5, arg6) \
        __asmlinkage_protect_n(ret, "m" (arg1), "m" (arg2), "m" (arg3), \
                              "m" (arg4), "m" (arg5), "m" (arg6))
```

So the `SyS_read` function essentially just calls `SYSC_read`, applies some compile-time checks, and returns the result.

Finally! We're at the definition of the actual syscall.

```
static inline long SYSC##name(__MAP(x,__SC_DECL,__VA_ARGS__))
```

A quick look at `SYSCALL_METADATA` shows that the macro expands to stuff used for tracing syscalls `#ifdef CONFIG_FTRACE_SYSCALLS`. 

So after all the expansion, 

```
SYSCALL_DEFINE3(read, unsigned int, fd, char __user *, buf, size_t, count)
{
        struct fd f = fdget_pos(fd);
        ...
```

becomes

```
... syscall metadata stuff ...
asmlinkage long sys_read(unsigned int fd, char __user * buf, size_t count) __attribute__((alias("SyS_read")))
static inline long SYSC_read(unsigned int fd, char __user * buf, size_t count);
asmlinkage long SyS_read(long fd, long buf, long count);
asmlinkage long SyS_read(long fd, long buf, long count)
{
    long ret = SYSC_read((unsigned int) fd, (char __user *) buf, (size_t) count);
    ... compile-time tests for each argument ...
    ... assembly stuff to prevent clobbering of arguments on stack ...
    return ret;
}
static inline long SYSC_read(unsigned int fd, char __user * buf, size_t count)
{
        struct fd f = fdget_pos(fd);
        ...
        
```
