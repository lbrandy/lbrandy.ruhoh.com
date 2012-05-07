---
title: "OProfile: Profiling in Linux for Fun and Profit"
date: '2008-11-10'
description:
categories:
tags: []

layout: post

---
Profiling code to find performance bottlenecks is a relatively common operation. My goal here isn't to give you a detailed understanding of OProfile. I just want to convey to you that it's incredibly easy to use and extremely powerful.  If you don't know much about profiling, or use only gprof because it's the only profiler you know, please read on.

The one and only <a href="http://oprofile.sourceforge.net/news/">OProfile</a> is a system-profiler for the Linux platform that has been my absolute favorite tool for profiling code. I have no idea why it's not more popular or so unknown (maybe I just don't run in the right circles). OProfile does have somewhat onerous setup requirements but it has become standard fair for many distributions that now have excellent support for it. It's become substantially easier to get set up over the past few iterations of my favorite distributions (why am I lying? I only really use Ubuntu... but it's still true!). For many distributions, it's become trivial to setup and use. It should be a standard part of any Linux developer's toolkit. (Windows and Mac developers have similar tools that work on similar principles: V-Tune and Shark.)

The most commonly used profiler is gprof. Most programmers tend to know about gprof and can probably profile something given enough googling. In my opinion, given the choice, OProfile is a far superior tool. I'd like to first discuss the primary differences between profilers like gprof and profilers like OProfile. If you happen to be a gprof ninja and notice any mistakes, please let me know. Hopefully, though, I can convince you that OProfile is both technically superior and easier to use.
<h3>OProfile vs gprof</h3>
<h4>The Inner Workings</h4>
Both OProfile and gprof work based on a statistical sampling method. They periodically poke into your program(s), figure out what code is currently being called, and increment the counter for that symbol. If you let this run long enough, with a high enough sample rate, and you'll get a pretty accurate distribution of how the code works. The primary difference, however, between OProfile and gprof, is what triggers these samples.

Gprof uses a special system call that will periodically sample the currently running process only. This means gprof will only be aware of things that happen in "user time" for your process. You will not see bottlenecks that occur in external shared libraries (like libc) or the kernel. This can result in gprof's results being very skewed for certain types of bottlenecks (page faults, file i/o, memory fragmentation, etc.).

If you are using gprof and the 'time' command doesn't agree with gprof's cumulative total time, you've likely hit this limitation.

OProfile, on the other hand, is a system-wide profiler that triggers on hardware events and will record not only all of the current symbols being executed but also which process they belong to. This means OProfile sees all. If your code is causing a major bottleneck in the kernel or in libc, OProfile will see it and gprof will not. The downside of this kind of omniscience is that OProfile requires special permissions. Typically, this means the sudo password. If you are doing computational optimization, this is usually not a problem.
<h4>Call Graphs</h4>
Gprof requires code be built with the -pg flag. This instruments the actual code with information that will help build an accurate call graph. The upside here is you get your call graph and you also have cumulative timings (how much time did we spend inside this function, and all of its children functions). The downside is that you have to instrument your code and you also need to recompile it with special flags. There's two issues here that are worth noting. First, the -pg flag can interfere with other flags (like -fomit-frame-pointer). This can make certain bits of code no longer compile or work correctly (for example, inline assembly). Second, adding instrumentation to the code can cause fundamental changes. There is a Heisenberg effect that by trying to measure your code, you affect its true performance.

OProfile, on the other hand, requires no instrumentation of the code. This means OProfile does not need your code to be recompiled with any special flags (so long as the binary in question hasn't had the symbols <a href="http://unixhelp.ed.ac.uk/CGI/man-cgi?strip">stripped</a>). Since OProfile's only source of information is the hardware-based event sampling, it doesn't have any real information about call graphs. OProfile is able to build "statistical" call graphs where it can make guesses about which functions are calling which. This typically requires some interpretation on your part to fully decipher. If you need an accurate call graph, OProfile might not be the best tool.
<h4>Multithreaded Code</h4>
I have no idea if this issue is resolved in gprof yet but gprof does not (or, at least, did not) support multithreaded code. Oprofile does.
<h4>Summary</h4>
OProfile pros:
<ol>
	<li> Supports hardware based events (more than just CPU clock cycles: cache misses, etc.)</li>
	<li>Supports multi-threaded code.</li>
	<li>Sees all processes and will find bottlenecks in other places (like kernel and libc).</li>
	<li>Does not require any special compilation flags, or even recompiled code.</li>
</ol>
Cons:
<ol>
	<li> Requires root access</li>
	<li>Requires kernel support</li>
	<li>Does not provide (precise) call graphs nor cumulative timings</li>
	<li>Not portable (Linux only)</li>
</ol>
<h3>Setting Up OProfile</h3>
Most popular distributions have an OProfile package that can be easily installed. The only caveat is that some distribution flavors come with kernels that don't have OProfile support built in. This means you'll need a new kernel (they might offer an alternate in their package system, or else you will have to... compile it yourself... gah). I've found over the last few years many of the most popular distributions are shipping with kernels that support OProfile. Ubuntu, for example, has for awhile (while the server version, I believe, does not).

Installing the tool is usually fairly trivial (vanilla Ubuntu users need only: sudo apt-get install oprofile). Once installed the only setup required is:
<pre>sudo opcontrol --no-vmlinux</pre>
This tells OProfile that you do not have an uncompressed binary of your kernel (your vmlinux file). This means that OProfile will assign all kernel samples to a black-box called "no-vmlinux". If you see "no-vmlinux" high on the charts, you will know you are having bottlenecks inside the kernel. You can peer into the kernel by telling OProfile where your vmlinux for the kernel can be found. If you build your own kernel, you should already know what to do. By default, however, most distributions ship with only a compressed kernel (vmlinuz). Typically, there is a package that you can download that will also give you an uncompressed version of the kernel. For example, Ubuntu (Hardy Heron) calls it linux-image-debug-{version}. If you install that package, it will put a vmlinux file in /boot/. If you point oprofile to that file, you will be able to get a breakdown of what is happening inside your kernel.

Usually, by default, your system's prebuilt binaries are stripped of their symbols. This means that all of these applications and libraries will be black boxes to OProfile as well. If, for whatever reason, a particular program seems to be bottlenecked in libc for example, and you want the profiler to break down whats happening in libc, you will need to install the version of libc that contains symbols (look for the -dbg package). Furthermore, if you want to profile some pre-built binary, you will need a version without the symbols stripped out.
<h3>Using OProfile</h3>
It's really this simple:
<pre>sudo opcontrol --reset
sudo opcontrol --start
./run_my_code
sudo opcontrol --shutdown
opreport -lt1</pre>
Those are petty much all of the commands you need to know to use oprofile. You reset and start the profiler, run your code, and then shut it down. The final step is viewing the results. The opreport command in my example has taken two flags. The -l flag shows you inside each process (otherwise you will get just an overview of each process and its respective usage of the system resources). The -t1 flag sets a threshold at 1% so you don't see every symbol.
<h3>Advanced Beginner Usage</h3>
<h4>Cache Misses</h4>
On x86 machines, it's also fairly easy to track cache misses using OProfile. By default, OProfile tracks CPU_CLK_UNHALTED hardware events. This is really a measure of how long your code takes to run. You can change the hardware event (sudo opcontrol --list-events to see all the other options). In particular, you can switch to the L2_REQUESTS event with a mask that includes only 'INVALID' requests. This requires a bit of internet searching, or the Intel optimization manuals. I've gone ahead and looked it up for you, though:
<pre>sudo opcontrol --event=L2_RQSTS:1000:0xf1</pre>
Events are specified in this way with the first number being the count (how many of these events cause a sample to occur, lower is better but requires more overhead). The second number is the unit mask. In this case, the 0xF1 means across all CPUs, but only INVALID L2_RQSTS.
<h4>WTF moments</h4>
Have you ever built in some complicated new package and aren't getting results you think you should be? If you are anything like me your first thought is "Am I even running the new code?". Maybe you open your editor, dig down, and drop in a few printf()s to figure out if you are even calling the new super fantastic function. This obviously isn't the smartest way to do this. OProfile solves this problem trivially by letting you sample any compiled code. You can just fire up the profiler and actually look at all the symbols that were caught by the profiler. This is usually the fastest way to figure out if the code you wanted to be called is being called.