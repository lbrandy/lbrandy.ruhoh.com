---
title: "Code that works the very first time"
date: '2009-09-14'
description:
categories:
tags: []

layout: post

---
It happens from time to time. You write some non-trivial code that is difficult to decompose into bite sized problems. And when it finally comes time to run it, it works. Perfectly. This is almost immediately accompanied by two feelings: 1) elation and 2) panic that something must be wrong. Do we trust this code? What do we do next?

Now, there's probably some subset of readers already gnashing their teeth: the test driven developers. If you are writing all your tests first, and watching them go from failure to passing, certainly this problem won't happen. But it will. I assure you. There are bits of code that are quite complicated and extremely difficult to test until large amounts of it are in place. When you see many difficult tests go from fail to pass on the first try, the same panic strikes (although it's usually more of the "did I write good tests?" variety).

Here's some of my examples from recent memory:

1. **An experimental memory allocator **-- We had a hypothesis that a certain type of highly customized memory management strategy would result in speed improvements to our codebase. I wrote up a quick draft memory allocator that employed the strategy to gain the speed-ups at the cost of memory usage. This allocator used memory like a pig but it resulted in the proper strategy to clean up the inefficiencies we were encountering. It was mildly sophisticated, had several custom data structures, was thread-safe, and so on. It worked perfectly the very first time I got it to compile. I don't believe a single line of code in it changed from that moment. The prototype allocator, by the way, let us run our speed tests. The speed-up wasn't that great. The idea (and the code) was tossed in the bin.

2. **A job manager** -- When you have a tasking to-do list, you can usually get away with something like a thread-safe queue feeding the tasks work to be done. In our case, a queue was simply insufficient. In truth, what we needed, was a two dimensional thread-safe priority queue with a handful of customized functionality for moving priorities around. It was messy problem and it was (almost) impossible to figure out how to even fully test it. In the end, I settled on a handful of good tests, and let the real code poke and prod all the inputs in all the various ways necessary. It, again, worked straight out of the box.

3. **A web scraper** -- I took a few examples of a web site onto an airplane with me and worked on the parsing engine while on the plane. About half way through the flight, I had the scraper parsing all of my test data to perfection. I spent the rest of the flight working basically blind. I had to build the mama-process that scheduled all the work and played watchdog. I was certain it would encounter errors on the real data because my test set was incomplete. I wrote in tons of error checking and other good features (like bypassing bad links and adding them to a "FIX-ME" list). Once I got home, the scraper worked brilliantly out of the box. The fixme file was empty. Not a single change was needed.
<h3>As the elation fades</h3>
Before it has passed, I go tell someone. You know you'd want to too. Just to brag for a minute before sitting down. Just remember, 75% of the time you'll find some boneheaded reason to announce that you lied not 5 minutes ago and it's actually horribly, horribly broken. Once the elation has passed, it becomes time to convince myself that it's actually working.

1. **Unit testing **-- If I haven't written baseline sandbox tests for the code, it's time to do it now. In fact, most of the time, I knew ahead of time the code would be difficult to write in small pieces and would have a "let's compile it all and pray" moment. In those instances, it makes sense to switch to a full-fledged test-driven-development methodology.

2. **Regression testing **-- Plug the module in, bring the system up to scale, and make sure nothing breaks at the highest level. These types of testing "from the top" are usually a pain to setup but they will catch some really nasty and subtle bugs.

3. **Step through it** -- When all else fails to convince me that my code is truly working, stepping through the code and watching it work at the crucial moments tends to finish the job. This can sometimes work equally well with a few well placed printfs().