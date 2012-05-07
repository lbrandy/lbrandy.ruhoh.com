---
title: "Mistakes we made when naming our computers"
date: '2009-09-21'
description:
categories:
tags: []

layout: post

---
<h4>Sequential Numbers</h4>
When our company bought a bunch of rack mounted computers for heavy computation load, we had to choose names. We numbered them, sequentially. They were skinny and generated a far bit of heat, so we called them toasters. Toaster1, toaster2, and so on. The first, and maybe most important, problem with this naming convention is that machines get no identity. They have no soul. It's difficult to distinguish them in your mind and you end up mixing them up constantly.

We were aware of this problem, but didn't care. These weren't going to be people's personal machines. They didn't need much of an identity. They all had NFS mounted drives and some local storage. The idea was these were computational workhorses and so a nice identity-less sequential numbering scheme would fit.

Here we are, a few years later, nearing our 20th rack mounted workhorse and this strategy has hit a second fault. When a computer dies, what do you do? Do you replace that number with a new computer, and thus break the "higher is newer and better" scheme, or do you leave that number permanently retired leaving gaps in the numbers? There's really no good solution to this. We decided to retire their jersey number. Over time the sequential numbering ends up being a big mess.
<h4>Too Descriptive</h4>
When you get a new machine, sometimes it is tempting to describe what makes that machine special. We named our very first quad-core machine "quad". We named our first octo-core "octo". Very original, I know. This works great at first because that machine is special. But what happens when you get a second quad core? I named it cuatro. We had another machine that was the definition of squirrely. The BIOS did a crappy job of identifying the CPU cores, and we struggled to get the computer to benchmark at the level it should have been at. We named this machine "broken". After replacing some of the hardware, broken works like a charm. It's still named "broken". When new people come and have to use "broken" for something, it doesn't exactly inspire confidence.

I think we've learned this lesson.
<h4>Bad themes</h4>
By far the most common scheme for naming is choosing a theme. This is probably the best strategy, as well. Each machine has an identity, and you don't suffer from "holes" (as you can safely "retire" names, as well). A good naming theme has a virtually inexhaustible list of easy-to-type (important) names. You can waste <a href="http://lbrandy.com/blog/2008/08/developer-timesink-name-paralysis/">a tremendous amount of time</a> finding one.

The big problem with themes is that you will eventually run out of good names. Early on we bought a bunch of very small form factor Shuttles for various purposes. We used them for their portability so you could hook up a camera to our software and have a computer doing the visual processing but remain relatively hidden. We needed a naming theme for our shuttles so we decided on Greek Gods. We'd never run out of Greek Gods. There was Zeus, Apollo, Hermes, and Aphrodite. This was, in retrospect, an awful naming scheme. Zeus, the king of the Gods, was some single core CPU with a gig of ram. He was almost useless. And who wants to type out Hephaestus?

In college, the computers at our lab were named after Simpson's characters. That's a great theme. The main server was named.... wait for it... Moe. Genius.
<h4>Our current solution: the themeless theme</h4>
We ended up abandoning most of our themes and have now settled into a good pattern. We name all our of machines with a really interesting word. That's the only rule. We have spike, blizzard, sparky, and windex, and so on. This, I believe, is the best scheme of all. First, and most importantly, ever other machine we've already named fits into this scheme perfectly. It's also fairly trivial to find new names and avoid paralysis. Every machine gets a unique identity, and finally we are certain we will never run out.