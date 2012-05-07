---
title: "Using genetic algorithms to find Starcraft 2 build orders"
date: '2010-11-01'
description:
categories:
tags: []

layout: post

---
<em>UPDATE: Just to make this explicitly clear: I did not write this program. The fourth sentence makes this fairly clear, but some comments indicate that some people are a bit lazy :). I also added a video of the rush to the bottom.</em>

I've been on a bit of starcraft kick recently (see my replay aggregator: <a href="http://replayspider.com/">replayspider</a>). I also work in computer vision, and general AI has always been an interest (see this post on <a href="http://lbrandy.com/blog/2009/04/genetic-algorithms-evolving-human-faces/">"evolving" faces</a>). Sometimes strange interests collide. Over on a forum called <a href="http://www.teamliquid.net/">teamliquid</a>, a user by the name of Lomilar <a href="http://www.teamliquid.net/forum/viewmessage.php?topic_id=160231">posted a fairly long thread</a> about a program he had written that optimized build orders for the zerg race in starcraft. He eventually cleaned up his code and <a href="http://code.google.com/p/evolutionchamber/">posted the code to googlecode</a>. The program is called EvolutionChamber (a clever name, as it's the name of one of the buildings in the game), and it uses genetic algorithms to find build orders.

This I had to see.
<h3>A quick Starcraft 2 primer: setting up the rules</h3>
Since this is primarily a programming blog, I'm going to assume you know a fair bit about video games. Feel free to skip this section if  you know anything about starcraft 2, in particular. Essentially, SC2 is a real-time strategy game that starts you with a simple base, some workers, and some resources, and asks you to put those workers to work collecting resources that you can use to build things (including other workers), eventually building up an army and killing your opponent. A build order refers to the exact opening steps you take early in the game that best supports the strategy you are trying to conduct. These early games are all about balancing spending money on your economic foundation (making more workers), making units (rush!), or building new buildings or getting new upgrades (tech!).

Build orders generally only cover the very early game because once you've scouted the enemy, you have to begin to react to what he's doing and modifying it as you go. In other words, and a perfect aphorism, no battle plan survives first contact with the enemy. In this way, build orders in real-time strategy are very much akin to openings in chess. They set up the soul of the entire game about to be played, and some players prefer to force certain types of games, depending on what kind of opening they choose to do.

One of the reasons build-order optimization is so important is that you can discover openings that "hard-counter" other openings. If I can get an army of N size into your base when you do opening X, you will always lose.

Enough with the abstract, here's what you need to know:
<ol>
	<li>The program in question optimizes Zerg build orders (which is one race in starcraft), this is a rather significant choice because the mechanics of the zerg race are arguably the most difficult to manage (esp. for build order optimization).</li>
	<li>Of most interest are "rush" build orders. This means "how quickly can I get N of this type of unit?".</li>
	<li>There are two primary resources that workers collect in starcraft: gas and minerals.</li>
	<li>Zerg also have a third de factor resource: larva. Larva are used to create ALL zerg units, including workers.  So long as you have less than three,  they regenerate at a fixed rate (note: this means any time spent at three larva delays all future larva production -- very bad).</li>
	<li>Most units require some building to be constructed in order to be "unlocked" (and many of these buildings require others as prerequisites -- this is the so-called tech tree)</li>
	<li>Creating a building causes you to lose the worker who creates it (so the longer you can wait, the more resources that worker can collect before building the building)</li>
</ol>
These "rules" provide for an extremely complicated search space to find optimal build orders. Essentially, you want to make the exact number of workers you need as quickly as possible (and then no more). Losing a worker when you make a building, and delaying all future larva when at three larva make the dynamics extremely complicated.
<h3>How EvolutionChamber works</h3>
At its core, the program is a <a href="http://en.wikipedia.org/wiki/Genetic_algorithm">genetic algorithm</a>. For those of you who don't know, a genetic algorithm is a type of optimization algorithm that tries to find optimal solutions using a method analogous to biologic evolution (to be specific: descent with modification &amp; natural selection). Put simply, you take a "population" of initial build orders, evaluate them for fitness, and modify the population according to each element's fitness. In other words, have the most successful reproduce.

The program's input is simply the desired game state. In practice, this means "make N units" to determine some rush build order (but it also allows for other types of builds, like make N workers with some defensive structures and a small army). Here are some of the highlights:
<ol>
	<li>It's written in Java using <a href="http://jgap.sourceforge.net/">JGAP</a>.</li>
	<li>A 'chromosome', in this case, is an array of 'actions' that can be done in game. (e.g, 1) Build a drone. 2) Build a drone. 3) Build a spawning pool. 4) Build an overlord. And so on.)</li>
	<li>Invalid actions (ie, trying to build a unit you cannot build because you do not have the tech necessary) are ignored (this allows for "junk dna").</li>
	<li>An action that can't be done YET (not enough minerals!) causes the simulation to wait until it can be done.</li>
	<li>It uses some fairly standard mutation types (deletion, insertion, and one strange one called "overlording" -- heh)</li>
	<li>It uses the "many villages" approach where there are several separate populations evolving independently.</li>
	<li>Populations that are deemed to be stagnant are annihilated and replaced by a variant of the most successful.</li>
	<li>The fitness function is really a measure of distance from the "desired" state and the current state (this is measured by the difference in resources required to get there), taking into account the time required (less time is always better).</li>
</ol>
<h3>The 7-roach rush</h3>
For the starcraft nerds among you, here's one of the very first builds constructed by the program:
<pre>10 extractor-trick to 11
11 overlord
11 spawning pool
15 extractor
16 queen (stop drones here)
18 overlord
18 roach warren
17 overlord (yes, two)
spawn-larva on queen when she pops
roach x7</pre>
This is a fairly fascinating build order in a number of respects.

First, from a starcraft perspective: it is incredibly strong. To be clear, I am certain virtually anyone who practiced this build and went onto the ladder and used it in every game would very easily rise to diamond level (currently the highest league). The seven roaches at that time in the game will destroy all but the most well-executed counter-builds. It caused an <a href="http://us.battle.net/sc2/en/forum/topic/902030865">almost immediete stir on the starcraft forums</a>, and had one player proclaiming that an all-in variant ("all-in" coming from poker and to mean that you win or lose right now, in this case it means attacking with all your workers as well as your army) was <a href="http://us.battle.net/sc2/en/forum/topic/902031213">completely unstoppable in a certain matchup</a>.

Second, as far as I know, this build was "discovered" by the program (or at least, it's never been well known). There is a similar build that's been well known called the 5-roach-rush (the 5-roach-rush comes later, and is a bit more economical). When comparing the two, the 5RR has certain situational advantages, but the 7RR build, above, has two staggeringly obvious advantages: 1) you get two more roaches, 2) you get them almost 45 seconds sooner. I'm not 100% certain this build was "discovered" by the program, but I do know it's not been extremely popular or considered standard play so my guess is that it's not been studied in too much detail.

The most interesting part of this build, however, is how counter-intuitive it is. <strong>It violates several well-known (and well-adhered-to) heuristics used by Starcraft players when creating builds. </strong>Some of this may be lost on you non-starcraft players, but I'll do my best to explain.

**Extractor trick.**

The extractor trick is using a drone to build an extractor (remember this removes the drone), then build a replacement drone, then cancel the extractor, giving you the original drone back -- this allows you to build one more worker than your supply would allow. The extractor trick, as used above, has been tested and seen to be economically inferior to a more standard play of buying an overlord on 9 supply. The extractor trick + very early spawning pool do some economic damage and induce a small larva delay, so they are almost never seen. In this case, however, the extractor trick + early pool end up speeding up the entire tech path (this is the primary reason why the 7RR produces roaches much sooner than the 5RR).

**Double Overlord at 18/17.**

First, a quick discussion about supply. Each unit you create costs supply. So long as you have supply, you can make units. Most RTS games have a similar concept. Overlords, for the zerg, are the unit that provides this supply. So for zerg, you have to spend 100 minerals to unlock additional supply. In general, it  is considered "optimal" for you to have just enough supply to not be supply-blocked. It's generally considered wasteful to buy supply when you don't need it (since you could spend that money, instead, on units or workers now, and buy the supply later, when you need it).

In almost all cases, it would be extremely wasteful to purchase supply twice in a row. I'm not sure any starcraft player would look at such a build and consider that a good idea. In this case though, it ends up  working out so perfectly that you'd actually have to try it any other way to understand how and why. Because your desired goal is 7 roaches, you will need to construct 2 more overlords at some point, but doing them both so early is certainly surprising. During that particular period of the build (around 18 supply), you end up waiting for your roach warren to finish so you can begin creating roaches.  This causes you to max out on larva, stopping regeneration. By moving the second overlord so far up into the build, this larva ends up being "free" -- you'd lose it anyway because the regeneration would stop. So the only penalty to making the second overlord early is minerals, and during this portion of the build, you are not mineral-bound. The net result is that moving that overlord so far up into the build costs nothing and frees up larva regeneration to produce quicker roaches.

This is the type of non-obvious optimization that genetic algorithms excel at.

As for the 7-roach-rush, I'm certain if you are playing starcraft2, you'll see this build quite a bit. As for whatever hidden and game-breaking builds remain undiscovered, that remains to be seen.

<strong>UPDATE:</strong>

Here's a video of someone doing the 'all-in' variant of this build against a real player:

<object width="640" height="385"><param name="movie" value="http://www.youtube.com/v/KH1ucvJomlY?fs=1&amp;hl=en_US"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/KH1ucvJomlY?fs=1&amp;hl=en_US" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="640" height="385"></embed></object>

Thanks to <a href="http://www.rockpapershotgun.com/2010/11/02/genetic-algorithms-find-build-order-from-hell/">rockpapershotgun.com</a> for the writeup and pointing me to this video.