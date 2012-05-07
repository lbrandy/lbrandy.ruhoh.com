---
title: "Parallel programming is hard. Right?"
date: '2010-02-24'
description:
categories:
tags: []

layout: post

---
It's a fairly oft-repeated mantra of programmers. Parallel programming is hard. Right? Right! Almost everyone will tell you so! I was at a job fair not too long ago and even one of the students told me so. Everyone knows parallel programming is hard.

Sadly, though, I disagree with the vast majority on why. The most common answer, by far, will involve some combination of the following words: <a href="http://en.wikipedia.org/wiki/Deadlock">deadlock</a>, <a href="http://en.wikipedia.org/wiki/Deadlock#Livelock">livelock</a>, <a href="http://en.wikipedia.org/wiki/Parallel_programming#Race_conditions.2C_mutual_exclusion.2C_synchronization.2C_and_parallel_slowdown">synchronization</a>, <a href="http://en.wikipedia.org/wiki/Shared_memory">shared memory</a>, <a href="http://en.wikipedia.org/wiki/Race_conditions">race condition</a>, <a href="http://en.wikipedia.org/wiki/Thread_safety">thread safety</a> and so on. You can find umpteen blog posts explaining how difficult it is to avoid race conditions, and how <a href="http://lbrandy.com/blog/2009/02/bugs-of-doom-aka-the-heisenbugs/">some of the most pernicious bugs come from synchronization issues</a>. Yes, indeed.

(note: this post is mostly about data-parallel programming, or other parallel optimizations for computational performance purposes. There are other reasons to use concurrency, but I'm not sure my argument will hold in most of those cases.)
<h3>Avoiding race conditions is hard, but it's not that hard.</h3>
There, I said it. I think most people, especially those who've only learned about parallel programming in a classroom setting, believe that race conditions, synchronization, and dead-locks are the crux of the parallel programming problem. There are a whole bunch of really solid reasons for me to say they are wrong:
<ol>
	<li> You can almost always use a simple locked data-structure for synchronization fairly painlessly (and with a bit of practice, you can usually write one fairly painlessly, too).</li>
	<li>You can almost always abstract away the synchronization primitives and unit-test them really well.</li>
	<li>There are tons of good off-the-shelf and well-tested synchronization libraries for most platforms, and most languages.</li>
	<li>The <a href="http://www.mysql.com/">truly difficult synchronization problems</a> have many, many smart people working on them, and these are things you should not be reinventing.</li>
	<li>**And last but not least, and most importantly, no matter how difficult your synchronization issues are, I can assure you that bigger problems are lurking.**</li>
</ol>
<h3>Why parallel programming is actually hard</h3>
There is probably no one correct answer to this question, but most will probably involve words like: granularity, throughput, response-time, cache size, memory bottleneck, and so on.

Let's start with the core of the problem: <a href="http://en.wikipedia.org/wiki/Granularity">granularity</a>. When parallelizing some computation, you must decide "at what level" to parallelize the problem. Choosing the correct granularity is almost never immediately obvious and, almost always, there is more than one correct answer.  Trade-offs abound.

I'll invoke a problem from my daily work that will help explain this nicely. A video file is nothing but a sequence of images. If you want to perform face detection on a video stream, you can parallelize in several ways. A coarse grain approach might be to give each worker its own image, and collect the results at the end. A finer grained approach might throw all of the threads at a single image hoping you can process that image n-times faster.

**Here are some general (yet frequently broken) rules of thumb:**

1. **Finer grained algorithms will thread less efficiently than coarse grained.** Usually, it's because any natural parallelism in your problem tends to improve as you become more coarse grained (do 20 images in each thread, instead of one). Furthermore, coarse grained algorithms do less communication and synchronization per unit of work. This means coarse grain approaches will tend to have better throughput (work done per unit of time) and less administrative overhead. There is an important caveat here, if you are too coarse grained, or if your jobs vary in size too much, you run smack into <a href="http://en.wikipedia.org/wiki/List_of_NP-complete_problems#Sequencing_and_scheduling">scheduling problems</a> that will certainly leave some workers with nothing to do.

2.** Finer grained algorithms will have better response times.** In this case, response time means from submission of a work unit, until the result is ready. Since a fine grained algorithm is more frequently synchronizing the state, you have more opportunities to prioritize things that need to get done, and then declare them done.

3. **Finer grained algorithms will tend to use less cache/memory.** This is because, in general, less data being worked on.

4. **Finer grained problems tend to be more painful to maintain**. You will assume parallelism along some dimension that really needs to be serialized for some new feature.

Let's go back to my real-world example. Sometimes throughput is king, like when you are processing a movie file. In this scenario, sending a frame to each worker thread and collecting the results later is fairly easy to implement, and threads extremely well. Other times, response time is king. For example, when tracking a face with a pan-tilt-zoom camera. Sending each frame to a different worker is completely inappropriate for this use-case because this doesn't improve response time at all (each thread only has one worker, still). As soon as a frame is submitted, you need an answer as quickly as possible to have stable control. In this case, it is far better to throw all of the worker threads at a single frame (thread at the sub-frame level), and hope to improve the computation of a single frame.

So what do you do when the frame-level approach threads more efficiently than the sub-frame level treading? Well, you've run into a situation where one approach is better for throughput, and the other for response time. If you want to support both use-cases, you need both approaches (and some good documentation!). I think this demonstrates my original point that bigger problems than synchronization are lurking. No matter how difficult your synchronization problems are, I just doubled them.
<h3>Trade-offs in every direction</h3>
So lets say you can sort your way through that nest of trade-offs to find a place that gives you the right balance of response-time and throughput, stays within your memory requirements, and threads at an acceptable efficiency, you are home free! Right? Wrong. Now add in the fact that you cannot predict the future, and you don't know what features will be needed (and what will then need to be serialized), how your response-time vs throughput needs might change, or how you will ever maintain this mess.

If you've survived this far, just remember the computer has one last trump card to play on you. All of these threads run on all real machines, with real memory bandwidths, real caches, connected over networks with fixed bandwidth. Each of these constraints has the ability to trip up your beautifully parallel problem and make it painfully serial. Let's not even mention the idea that it might need to run on different machines with different capabilities.

In truth, all of these difficulties come from the same source. Mapping a non-trivial problem onto a parallel machine optimally borders on the impossible when you fully consider all of the different requirements along all of the different dimensions.

And so here we are. When I think of parallel programming, synchronization is difficult, but managable. It is not, however, what makes parallel programming hard.