---
slug: profession-hobby
title: "Coding: profession/hobby"
icon: "fas fa-user-tie"
---

Coding is my profession (and it's also a hobby).

### College

I've always liked tinkering with computers. I then studied Electrical and Computer Engineering at Cornell, where professors managed to sell me Computer Architecture as a career. In those college years Computer Architecture was totally my thing; I could see myself optimizing chip design, doing pipelining, moving hot code paths into hardware and letting things just *fly* at an order of magnitude faster than it did in software.

{{< figure src="/photos/beebe-lake.jpg" title="Beebe Lake. From just behind Noyes Lodge, Cornell, Fall 2011" >}}

### Cybersecurity

Then school ended and I found myself able to apply my understanding of the hardware-software interface at work in cybersecurity. My team audited software and also built custom security solutions for our servers.

Auditing the Linux kernel source code and understanding vulnerabilities brought back the good old times from college when we had to step through functions - prolog, body, and epilogs, mentally emulating the stack and heap...

In school, going past the end of allocated memory meant re-writing your program to fix that. In the cybersecurity world, it means continuing to execute in a whole new world. It was fun seeing how people could creatively re/abuse code in other techniques too, such as in return-oriented programming.

{{< figure src="/photos/just-over-the-edge.jpg" title="A Whole New World, Just Over The Edge. La Cueva del Indio, Puerto Rico, Spring 2013" >}}

Work in security gave me a much deeper understanding of operating systems because all those malicious code would just throw system calls out the window and abuse protocols in their own ways to disable protections, get a grip on (address space layout/secret) randomization. They could even execute [allocated code at its physical address](https://cs.brown.edu/~vpk/papers/ret2dir.sec14.pdf)!

While on the defence, it was great to also see the offensive angle and think through their approaches.

### Out of work / programming languages: Clojure, Scala, OCaml / seeking the lisp enlightenment

Cornell CS had this (in)famous OCaml class (CS3110) that I *didn't* get to take because I didn't have the time in school. Then I did a compilers class, where my groupmate educated me on how our projects would have been so much simpler if we had been familiar with Scala. All these created this functional programming hole in me that I needed to fill.

So I did online classes:

+ [Functional Programming Principles in Scala](https://www.coursera.org/learn/progfun1) by Martin Odersky himself, and
+ [Introduction to Functional Programming in OCaml](https://www.fun-mooc.fr/courses/parisdiderot/56002S02/session02/about) by Université Paris Diderot

The paradigm shift from procedural languages was no doubt challenging, but it was a great learning experience, and the r/programming gurus were right - it truly shapes the way one codes. Functional programming forces you to think in components and functions instead of a long series of steps. You're also forced to write small, meaningful functions or lose yourself in your own code. All these are applicable even back in the procedural world. It was totally worth learning.

{{< figure src="/photos/seeing-differently.jpg" title="Seeing Differently. Infinity Mirrored Room, Yayoi Kusama, Crystal Bridges Museum of American Art, Fall 2019" >}}

While doing these courses I found that I really do have an interest in learning languages - and so I figured I'd work upwards to the source - lisp. (And of course I've been drinking from the hackernews and r/programming fountain of kool aid.)

So I dabbled in Common Lisp and Racket, but I felt some sort of disconnect from those. Common Lisp was kind of hard to get started in, and Racket just felt most aligned with DrRacket, but I wanted to stick with Emacs. I still want to learn/use those someday, I just haven't gotten to it yet

I then stumbled into the welcoming world of Clojure and felt that it just speaks to me! Repl-driven development is such a game changer. It took a while to get out of the mode of having a save-compile-run cycle, but once I got it, I began to feel the power it provides. Now that I look around, this workflow is actually taking different forms in different languages. For example, data scientists would be familiar with jupyter, which is basically a python repl that provides mechanisms for iterative exploration of data.

Also, I found [clojurians slack](https://clojurians.slack.com/) to be a very helpful and welcoming community where, as a beginner, I was able to find help easily. It also helped that there is a cozy but growing community of clojurians in Singapore that I hang out with, and I've also given talks at our [Clojurians Meetup](https://www.meetup.com/Singapore-Clojure-Meetup/)! I also like it that clojure allows us to ride on the tall shoulders of the Java giant so that we can be productive very quickly using Java libraries.

I've used clojure for a while but I still feel like I'm along the path to the lisp enlightenment. I look forward to understanding and utilizing the full power of macros in lisp.

{{< figure src="/photos/iceland-road.jpg" title="A Long Road. Iceland, Winter 2011" >}}

There are still many other languages I want to learn: Rust, Smalltalk, Erlang, Elixir, Elm, ReasonML, Prolog, Haskell..., and these, properly: golang, Racket, Common Lisp, OCaml, Scala.

It's pretty easy to pick up a language, but it takes way longer to learn the idioms, optimizations and standards.

p.s. This course was really brilliant - Grossman sets functional programming and object-oriented programming side-by-side, so you get to see how it's really two sides of a coin

+ [Programming Languages](https://www.coursera.org/learn/programming-languages) by Dan Grossman

### Management

I was appointed Engineering Group Lead, in the team that builds security software.

In this role, I served as Engineering Manager, Tech Lead and Product Manager.

As product manager, I enjoyed helping users find out what they really need, and then designing good solutions for those problems. In this triple role, I had the benefit of being able to also guard scope fiercely so that delivered solutions would be timely and by still reliably tested.

It was difficult drawing a line between engineering manager and tech lead; in the role, I managed resources like tooling and hardware, as well as training for all officers. I also mentored newer teammates in coding and software development, and I was big on learning, both individually and as a team.

I believe in learning. Sending staff for courses is but an introduction to the topic. Nothing replaces the day-to-day investment of time to understand any subject thoroughly, running into problems to recognize the edge cases where one's solution wouldn't be sufficient, or just stepping through frameworks to understand how the designers had intended it to be used. In this role, I sought to allocate projects to maximise learning for my teammates.

I believe in learning from others and collective improvement. I had the good fortune of having great teammates that I could bounce ideas off, discuss problems and learn from. I wanted this for my teammates, so as a manager, I stood up for having teams of people work on a single problem instead of distributing people over many projects.

{{< figure src="/photos/growing-group.jpg" title="Growing Together. Korea, Spring 2016" >}}

I pushed for the use of our internal testing framework to remove the tedium of testing while improving reproducablity, and emphasized documentation to retain knowledge for future selves and other teammates.

### Moving up the tech stack

I then felt that I wanted to move up the tech stack, perhaps a little further from the kernel, libc and bash scripting into software engineering for data, using higher level languages, so I transferred into a software engineering role in our of our data analytics teams.

{{< figure src="/photos/moving-up-lassen.jpg" title="Climbing Up. Cinder Cone, Lassen Volcanic National Park, Summer 2013" >}}

In this role, I found that interestingly, code auditing and cybersecurity never leaves you. While building apps, the possible vulnerabilities stood out to me - docker containers with daemons running as root, possible data validation/corruption or misconfiguration issues, ways to spoof credentials/identities/passing the hash...

Developing applications at this higher level of abstraction allows greater flexibility in leveraging technologies and tooling that others have built. It is nice seeing concepts in programming like abstraction and modularity repeat themselves again at a system level in (micro)service oriented architectures. Unix's philosophy of making each program do one thing well replays itself at the level of services, except instead of text streams, we have json.

Before making this transition, I also did a bunch of online courses to get foundational knowledge in data science and machine learning, to better understand how software should be built to support analytics:

+ [Machine Learning](https://www.coursera.org/learn/machine-learning) by Andrew Ng, in python instead of Octave! (https://github.com/dibgerge/ml-coursera-python-assignments)
+ [mlcourse.ai](https://mlcourse.ai): A machine learning course with a good mix of theory and practice
+ [cs231n](http://cs231n.stanford.edu/): Convolutional Neural Networks for Visual Recognition
