---
title: "Genetic Algorithms: Evolving Human Faces"
date: '2009-04-20'
description:
categories:
tags: []

layout: post

---
<em>updated: I've been kindly informed that the algorithm described below is not technically a genetic algorithm because there is no crossover (e.g. sexual reproduction). Maybe I'll do a second version once I figure out a way to make two faces mate.</em>

I work for a company called <a href="www.pittpatt.com">Pittsburgh Pattern Recognition</a>. We do face detection, tracking, and recognition. This becomes important momentarily.

Not too long ago genetic algorithms were all the rage on the <a href="http://www.reddit.com/r/programming/comments/7i22c/genetic_programming_evolution_of_mona_lisa/">internets</a> (see original here: <a href="http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/">genetic programming: evolution of mona lisa</a>). I was keenly aware of genetic algorithms since I first learned of them in grad school and have always had the urge to code one up. Given the company I work for, and recent popularity of genetic algorithms, this gave me an idea. Let's evolve a human face.
<h3>What is a genetic algorithm?</h3>
A genetic algorithm is an algorithm that tries to find solutions to a problem through a biologically inspired method. Specifically, you create a "population" of solutions, score them to see which are most fit, kill off the weak ones, and have the most successful ones reproduce to form the next generation. You repeat this process until a solution emerges. You can find out more about the details on <a href="http://en.wikipedia.org/wiki/Genetic_algorithm">the wikipedia</a>.
<h3>How do I do it with faces?</h3>
We write face detection and face recognition software. Face recognition is about comparing two faces to see if they come from the same person. Face detection, on the other hand, is the process of locating faces inside images.

Every face detector, somewhere, deep in the heart of the code, has a function that essentially takes a square set of pixels and returns a number representing the likelihood that set of pixels is a face. In other words, every face detector has a built-in fitness function for a genetic algorithm.

So, I set out to write a face-evolving genetic algorithm using a slightly modified version of our face detector as the fitness function.
<h3>My Algorithm</h3>
Turns out it was insanely easy. The very first thing I tried resulted in reasonable faces. I only made minor adjustments to make the output look a bit better. Here's the details:
<ul>
	<li>Initial population (500) are random grey-scale images (they look like static)</li>
	<li>The best 15 reproduce twice, the worst 15 die</li>
	<li>I did asexual reproduction, depending only on mutation</li>
	<li>Mutation: each pixel had a 1% chance of being mutated to a random value</li>
	<li>The output images are moving averages that have been low-pass-filtered and normalized (in other words, I've done a bit of image processing to remove noise from the output)</li>
</ul>
This is not a sophisticated algorithm. In fact, there are a hundred ways you could improve this algorithm. But I didn't need to.
<h3>Results</h3>
Please note, <strong>our detector is a low-resolution detector.</strong> It means our detector is capable of finding faces that are quite small. That is an awesome feature for a face-detector but not such a good one for a face evolver. The evolved faces, consequently, must also be at low resolution.

<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="425" height="344" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0"><param name="allowFullScreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="src" value="http://www.youtube.com/v/qS5HWBNvf9U&amp;hl=en&amp;fs=1" /><embed type="application/x-shockwave-flash" width="425" height="344" src="http://www.youtube.com/v/qS5HWBNvf9U&amp;hl=en&amp;fs=1" allowscriptaccess="always" allowfullscreen="true"></embed></object>

<strong>The effect is more striking if you see it from a bit further away (stand back a few feet).</strong>