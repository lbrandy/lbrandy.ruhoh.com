---
title: "Algorithms in Real Life: Gradient Descent (1/3)"
date: '2008-12-01'
description:
categories:
tags: []

layout: post

---
<em>I wrote a <strong>really long </strong>post that I decided to break up and flesh out into 3 full-sized posts.</em>

Do all computer scientists see algorithms everywhere they look or am I just insanely nerdy? I can't stop seeing examples of <a href="http://en.wikipedia.org/wiki/Gradient_descent">gradient descent</a> in real life.

Gradient descent is a very simple <a href="http://en.wikipedia.org/wiki/List_of_optimization_algorithms">optimization algorithm</a> and is used in many real life examples of optimization. If you are unfamiliar with the algorithm, it's actually quite simple: imagine standing on some hilly terrain, blindfolded, and being required to get as low as possible. (As a quick aside, typically in optimizations problems we are trying to get as low as possible because we tend to want to <em>reduce</em> things like risk or error. In cases where you want to get as high as possible, e.g. profit, it's known as gradient ascent. All subsequent discussion assumes down is "good" but the logic is identical in either direction.). It shouldn't strike you as a necessarily difficult problem. You'd probably just try to figure out which way is downhill and head that way. Just keep going down until you can't go down any more. That's gradient descent.

The algorithm is not exactly rocket science:
<ol>
	<li>Figure out which way is downhill</li>
	<li>Take a few steps</li>
	<li>Go to Step 1</li>
</ol>
The beauty of this algorithm is that given a few assumptions about your terrain, you are (virtually always) guaranteed to eventually reach a valley. The mathematically inclined can fret over what those assumptions are or under what pathological conditions you aren't guaranteed a valley. The rest of us, however, are moving on.
<h3>Lessons from Gradient Descent</h3>
Two very obvious lessons learned come to mind when talking about any gradient descent algorithm. The deeper beauty in this analogy is how the practical lessons of the gradient descent algorithm apply so frequently in the real life analogues.

The first important lesson involves the step size. For gradient descent to work correctly, you need to take small steps in between assessing the situation and potentially changing direction. The size of the steps you take need to be small relative to the speed with which the terrain is moving. Put another way: <strong>effective gradient descent should involve constantly checking the lay of the land</strong> and figuring out which way downhill is. If you aren't checking often enough, you will wander aimlessly. The lesson here is quite simple: frequent feedback is good. Any real-life procedure that involves iterating rapidly is often a form of gradient descent.

The second important feature of gradient descent is that <strong>where you choose to start matters</strong>. A lot. For all intents and purposes, where you start your travels in the hilly terrain is going to determine where you will end up. Since you are always traveling downhill, you are going to find the valley that's downhill from where you've started. There's no way of knowing that on the other side of that ridge, there's an even better (deeper) valley. Gradient descent provides a way of optimizing through small evolutionary changes. Many small steps. It has no built-in way of finding revolutionary paths that might be quite painful in the interim but ultimately result in being in a much better place. It is important, then, to choose the place you start with care. It doesn't need to be perfect, but putting it in the ballpark of good answers will help you find them.

To summarize:
<ol>
	<li>Choose your start spot wisely.</li>
	<li>Get feedback. Often.</li>
</ol>
What follows are four examples (over the next three posts) of gradient descent in the software world. I'll start with the two least controversial and build up to the two more interesting ones.
<h3>Obvious Example #1: Gradient Descent in Programming</h3>
Many programmers have heard the phrase that "<a href="http://en.wikipedia.org/wiki/Optimization_(computer_science)#When_to_optimize">premature optimization is the root of all evil</a>". The lesson is clear but often misused. Get it working first. Figure out all the details. Get all the necessary features. Once all of that is done, you can go back, identify the bottlenecks, and optimize them. Frequently, the program is fast enough. Other times things you believe are bottlenecks aren't, or won't be, or will change fundamentally because of other reasons (like you need to add some feature). Like all good programming idioms, this is a general rule of thumb that a good programmer has extracted from a lot of experience. That same good programmer, though, knows there is a time and a place to break it. Bad programmers, however, turn things like this into personal tenants of faith beyond reasonable questioning. The misuse of the idiom is known as the fallacy of premature optimization and has been <a href="http://www.acm.org/ubiquity/views/v7i24_fallacy.html">pointed out before</a>.

Optimization by this method is gradient descent. The starting point has been chosen by non-performance criteria. You started with code that was the easiest to develop, for example, and now you want to profile it, find the bottle neck, speed it up, and repeat. This is effectively gradient descent. You are assessing the environment to find the quickest way downhill and stepping in that direction. The problem, however, is that your starting spot has been chosen with no regard to performance. That means the valley you end up may not be even remotely optimal. Once you start thinking about your application in a more global sense you may realize that fundamental design changes you made very early have had a drastic impact on performance. The only way to make substantive progress is to start over. With a more performance-friendly architecture, you may end up at a very different starting spot, and consequently a far superior valley when you finally finish.

In the end, all I've really advocated is to take some time early on to plan out your likely performance goals and whether or not your intended architecture will meet those goals. This type of planning isn't "premature optimization" and it certainly isn't the root of all evil. I trust that this isn't terribly controversial.
<h3>Obvious Example #2: Gradient Descent in Software Engineering</h3>
There exists a method for developing software known as the <a href="http://en.wikipedia.org/wiki/Waterfall_model">waterfall model</a>. The waterfall approach requires that you sit down and decide what the software is going to do. First, you spec it out. Next, you develop it. Then, you test it for bugs. Finally, you deliver it. Oh, and then you get paid. Piece of cake. Well, as it turns out, it doesn't work.

Making good software is exactly like trying to find a valley. Because the software landscape is beyond complicated, it's literally impossible to plan out the perfect piece of software. Once we as an industry came to this realization, we realized that the only way to get our software into the valleys was to consult our environment (ie, our users) frequently, and keep heading downhill. The best way to traverse an incredibly complicated landscape is gradient descent. That meant we needed methodologies that behaved like gradient descent. They needed to iterate rapidly.

Software development methodologies like <a href="http://en.wikipedia.org/wiki/Agile_software_development">Agile</a> and <a href="http://en.wikipedia.org/wiki/Extreme_Programming">Extreme Programming </a>are based on rapid prototyping and rapid iteration. The basic idea is simple: build it quick, get it out there, get feedback, make changes, and repeat this process often. It's an organic process and it's gradient descent. As I said at the top, any process that involves rapid iteration is often a form of gradient descent. Your goal is to get your product near your user, and let him guide you toward the valley with his feedback. You also need to take small steps and constantly involve your user. By constantly checking your environment for feedback, it remains possible to continue to head "downhill".

The lesson here has been repeated so many times as to have become trite: you need feedback early and often.

Continued in the next post (probably tommorow)...