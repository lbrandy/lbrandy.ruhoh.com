---
title: "My New Year's Resolution"
date: '2010-01-04'
description:
categories:
tags: []

layout: post

---
I am a bit of a procrastinator.

Yes, yes, that doesn't exactly make me special, but I'm talking specifics here. I'm a programmer, and a procrastinator. And that can mean troubles.

For the next year (and/or the first three weeks of January, whichever comes first), I'm going to automate/refactor/abstract any operation I do for the third time. I've noticed far too many insignificant hiccups in my workflow that go ignored. It's just that the marginal cost of putting up with the annoyance is so much less painful than sitting down and writing the script (or a special commands, or option, or what have you). Maybe I'll do it next week. And next week becomes next month. And now I've started to realize niggling annoyances that have gone on for years. Yes, years.

Let me give you two examples...
<h3>Oprofile</h3>
I use oprofile constantly.
<pre>sudo opcontrol --reset
sudo opcontrol --start
./run_my_code
sudo opcontrol --shutdown
opreport -lt1</pre>
I've typed that out, in full, for probably close to 3 years now. Why? Other people have noticed. I've noticed. I'm pretty sure no less than two of my co-workers would have edited my aliases for me, if I had let them. Well, I finally sat down and wrote the 10 line python script that will do this (and a handful of other useful oprofile functions) for me. It took about 10 minutes. Sigh.
<h3>Emacs vs vi</h3>
I've always been an emacs fan. I probably always be. However, there is one part of vi that has always made me jealous. The name. <code>vi</code> is just such an amazingly easy name to type instead of the incredibly laborious <code>emacs</code>. As a young kid, I decided to fix this and I added an alias for my customized emacs launch as "<code>em</code>". Yes, I aliased emacs to <code>em</code>. I've been using it for years. And it's extremely stupid. Extremely, extremely stupid. <a href="http://en.wikipedia.org/wiki/Rm_(Unix)">It doesn't take much thought to figure out why "<code>em important_file.cpp</code>" can become a disaster.</a> (extra stupid note: compare the locations of the typo keys).

I know it's stupid, and yet it continues. Every time I move my environment over to a new machine, I copy the alias over. Why? Because it's always been there, and it's on all my machines. Because I can't fix it <i>right now</i>. I'll fix it next time. Gah. It ends now. I will never type <code>em</code> again.