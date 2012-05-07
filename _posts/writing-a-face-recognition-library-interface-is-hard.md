---
title: "Writing a face recognition library interface is hard. Really hard."
date: '2009-06-08'
description:
categories:
tags: []

layout: post

---
This is a post I've wanted to write for awhile. This wasn't the post I had hoped it to be. The original working title was "Writing a library interface is hard. Really hard." The way the post was supposed to go was with me explaining a whole bunch of general problems with writing good programmatic interfaces for libraries and then giving some helpful advice.

Over time I realized that each library has such unique problems that general advice is almost entirely worthless. It involves balancing so many factor and in some cases the answers are obvious (a jpeg library really only has a handful of functions) or prior-art exists (GUI toolkits) that will help you. Other times, you are on your own and it becomes quite a struggle. So instead of my general advice that will save all of mankind, let me explain some of our struggles, and I'll let you figure out the lessons learned for your situation.

Oh, and as if the engineering challenges weren't enough, you needn't forget to add in these supplementary exercises that are among the most tedious in all of programming.

<h3>Crushed Souls</h3>
**Documentation**. It is not fun. We both know it. And yet, you absolutely must have it and if you've done it right, it'll be incredibly useful. The sad truth is that most people won't read it.

**Example Programs**. Virtually everyone who uses your library will skip straight by the docs and straight to the example programs. These cannot be bad. Try to make at least one short, simple, and hello-worldish. It should be easy to find.

**Error reporting.** Figure out a way to handle errors in a useful manner and report that information back to the developer. This is probably the second most soul crushing endeavor in all of programming.

**Meetings.** Did someone mentioning soul crushing? The only way to hammer out a good API is to get a bunch of people in a room and look at interfaces, functionality, paradigms, and conventions, and decide what is good and bad. As a word of warning, these meetings will not be short.

**Iterate.** You simply cannot get it right the first time. This shouldn't come as a surprise. Iterate early, and iterate often. Work out a prototype H file first and work from there. Get that into a room with other devs and walk through the use cases. That H file is your spec.

<h3>Usability vs Flexibility</h3>
This is where it gets difficult. Our SDK typically has been geared towards ease of use, not power. This meant that certain sophisticated things we do with our internal codebase aren't possible to replicate using our SDK. For example, we have a live camera-fed demo that devoted some threads to video processing (face detection &amp; tracking) and real-time display, and some other threads for psuedo-background recognition that updates the onscreen results as they come in. The complicated mix of threads and asynchronous nature of the recognition made this a non-trivial program to write. While possible, our old SDK was fundamentally ill-equipped to replicate it.

If you want to build an easy-to-use library, it's fairly straightforward. You pick a few use cases, do those right, and everyone else be damned. We decided, recently, to expose more functionality to make it capable of all the complicated and nuanced things you might want to do. This resulted in marathon meetings, lots of teeth gnashing, and at least one heated argument.

And you can take it too far. More than once, while at the whiteboard,  we'd finally convinced ourselves that this particular set of functionality lets everyone do everything. At that point it became clear, however, that it's all so complicated that you'll need five times the documentation and no particular user has any hope of actually getting it right on their own. So now you've traded feature request emails for "how do I get this to work?" emails. We went back to the literal drawing board.
<h3>High-level vs Low-level</h3>
Our original face recognition SDK basically had one function. Given two faces, you got a score. That was it -- pretty much the epitome of low level. From there, everything else follows. It turns out, of course, that everything else isn't so simple. Some people want to compare a probe face to a gallery of faces and find the best match. Other people want to take all the faces in some unorganized collections and organize it. In any use case, you'd need to build up a fair bit of infrastructure. You'd have to handle saving, caching, and re-using previous results. If you want to use a huge dataset, its up to you to figure out how to partition the data, and how best to thread it. There was quite a bit for you to get right. And more often than not, we found people getting it very, very wrong.

Eventually we realized that in any one use case, a developer using our SDK would have to create so many things and get so many of them right, that it simply wouldn't be feasible for him to get the system he wanted. At least not as well as we could.  We'd thought long and hard about some of these problems and could build solutions that were simply better.

Adding all of these functions while maintaining full flexibility resulted in a dozen functions (instead of our original one). Every function you add adds to the pain. It create complexity, documentation, and work. But we trimmed down to some minimal set that best balanced all these factors and pushed forward.
<h3>Elegance</h3>
When you find a non-trivial library that works spectacularly out of the box, you've found a piece of programming gold. It's a library that handles the easy and common cases trivially. It's a library whose abstractions snap together so well that you can almost do what you want without looking at the documentation. It's documentation that is easy to use and results in quick and accurate answers. And when one day you realize you need something a bit more sophisticated, the feature is there waiting for you. You shouldn't take it for granted. It's so incredibly hard to get right.

So in that spirit, <a href="http://doc.qtsoftware.com/4.5/index.html">I'd like to nominate </a><a href="http://doc.qtsoftware.com/4.5/index.html">Qt</a> as the most elegant and well-documented library I've ever used. Our SDK is not there, yet. All we need is about 100 iterations of progressive refinement.