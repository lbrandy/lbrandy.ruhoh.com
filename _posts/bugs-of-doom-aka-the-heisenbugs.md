---
title: "Bugs of Doom (aka the Heisenbugs)"
date: '2009-02-16'
description:
categories:
tags: []

layout: post

---
I think anyone who has programmed for any length of time has some stories to tell about the most ridiculous and convoluted bugs that they've ever encountered. Here's my little hall of fame. Pretty much all of the most convoluted bugs have something in common: they are incredibly difficult to reproduce. In low level languages, this typically involves one of three issues: memory management, concurrency, or rarely a bug in something you should be trusting (your compiler, your OS, etc.). In higher level languages, the most convoluted bugs tend to happen when the auto-magic of your language hits some corner case and goes haywire.

The absolute worst of the worst are the <a href="http://en.wikipedia.org/wiki/Heisenbug#Heisenbug">heisenbugs</a>. That is, the bugs that only happen when you aren't looking for them. The harder you try to find them, the less reproducible they become.** The very act of trying to debug them, makes them disappear.**
<h3>Concurrency troubles</h3>
**What happened:** We created a live demonstration of our face detection and face tracking. We decided to stress test it and leave it running for awhile. It would dead lock after running for about 2 days.

**How we attacked it:** It was relatively simple to determine that a thread was crashing. The problem was altering the code in any meaningful way ended up making the bug irreproducible. You can imagine the pain in testing this, however, because it takes a good 4 to 5 days to decide the bug isn't going to happen, <a href="http://en.wikipedia.org/wiki/Halting_problem">and even then you aren't sure</a>.

**What caused it:** It ended up, no surprise, being a subtle race condition. We set up a thread-safe queue to have the mother process dump all the work to be done onto, and then had the worker threads reading off that queue. In our implementation, the queue could be connected to by worker threads, it would give them things to do, and be disconnected from once the worker thread was done. It would also clean itself up once all the connections died and there was nothing left on the queue.

Well, that last little bit is the root of the problem: the program crashed in the pathological condition when one of the threads was blocked in such a way that the other threads were all able to connect to the queue, process all of the data, and then disconnect. The queue would clean itself up, then, and the final thread would awake and try to connect to the now vanished queue. Crash.

**The fallout:** It probably took us an off-and-on three weeks to figure this one out. Most of that time was spent reproducing the original crash before we started looking seriously. Threading is no joke. Even simple implementations are wrought with potential problems. From that point on, we made some (obvious) rules regarding our threading constructions. First, we have a "prove this is too slow, first" approach to extra complexity (is there an off the shelf solution? Does an extremely simple solution work, first?). Next, if you really need a customized synchronization method for performance reasons, you make it generic (so it can be reused) and you test it  with extreme predjudice. We've built up a nice library of extremely well-tested thread-safe data structures for our use cases. We rarely have to write new ones, these days.
<h3>Memory, memory, memory</h3>
**What happened:** Again we decide to stress test an application and it seg-faulted after a few days.

**How we attacked it**: We turned off threading, and it ran for 2 weeks, no problems. We removed the assembly code (replacing it with our non-assembly versions) and it ran for 2 weeks, no problems. Sigh. Okay, now what? Was the assembly code bugged and trouncing out of bounds overwriting important information? Another race condition? Or some memory issues that only showed up in certain circumstances? It was the last one.

**What caused it:** I did. In order to maximize speed for SIMD assembly, you want your data structures to be aligned to cache-line boundaries. This typically means you want all of your primary data structures to start on addresses mod 16 = 0. In order to do this, I had created an aligned allocator. The assembly code was using the aligned allocator, while the non-assembly code defaulted to the normal allocator. As it turns out, you really shouldn't use <a href="http://linux.die.net/man/3/valloc">valloc()</a> to get this kind of alignment. That was just boneheaded.

valloc() gives not just 16-byte alignment but (on our machines) 4096 byte alignment. That's like 4080 bytes better! It also has the horrible side effect of potentially fragmenting memory into pieces. This is exactly what was happening in our case. Switching to a more sane <a href="http://linux.die.net/man/3/valloc">memalign()</a> caused the problem to go away (or, at least, cause the half-life of the problem to be pushed beyond our acceptance horizon).

**The fallout: **This bug actually took close to two months to finally track down. The reason it took so long was because of the other experiments we had to run for a week each to convince ourselves it wasn't going to crash in the same way. And then the experiments seemed to point in the wrong direction (an assembly or threading bug). Anyway, we decided to add some real memory recovery code to our application. More importantly, we learned the danger of memory fragmentation first hand.
<h3>Memory, again, maybe</h3>
**What happened: **I was improving one of our internal programs that operated on huge amounts of data in batch. You couldn't fit all of the uncompressed data in memory at once, so you had to uncompress a chunk, do your work, free the uncompressed chunk, and start on the next chunk. Very occasionally, the free() call appeared to fail. It appeared that that chunk just stayed in memory, and it would go to expand the next chunk, causing the system to start swapping and crawling to a halt. It appeared to be some kind of memory leak.

**How we attacked it: **This was the ultimate heisenbug. Every single time I tried to probe the executable, the bizarre behavior would vanish. Run it through valgrind, it vanished. Change the compile flags, it vanished. Use a malloc() debug replacement, it vanished. Write a custom version of malloc() to track simple issues, it vanished. Put a print statement in the offending code, it vanished. Attach gdb, of course, it vanished.

**What caused it: **Well, uhm, that's a funny story. After about two weeks of trying everything under the sun, it stopped happening. I don't know what I changed. I tried reverting my changes bit by bit. I tried a fresh check out. I did everything I could to reproduce this bug, and I couldn't. And I can't fix a bug I can't reproduce.

**The fallout:** Maybe it was a bad object file getting into the build by accident. Maybe it was a pathological linux kernel issue. Maybe it was a pathological malloc issue. Maybe I am crazy. Maybe. Maybe there's a landmine sitting in that program waiting to explode at some later date.

How about you? Got any stories?