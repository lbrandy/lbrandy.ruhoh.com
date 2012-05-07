---
title: "The Day I Got Git (with some help from github)"
date: '2009-01-05'
description:
categories:
tags: []

layout: post

---
Unlike other programmer holy wars, <a href="http://en.wikipedia.org/wiki/Distributed_revision_control#Vs_Centralised">distributed version control versus centralized version control</a> actually has interesting underlying issues. Distributed version control systems are all the rage these days and git seems to be leading the charge. I use both svn and git so I'll use them as my examples of the two paradigms.

When you first learn about distributed version control, it takes awhile to figure out why you'd ever use something like it. I understand why the Linux kernel people need it (or other very distributed development teams). But why would I need it? Seems like overkill. It's not until that first use-case hits you and all of the sudden the world explodes.<strong> </strong>What I'm presenting here is a particular use-case in which git shines and where subversion seems quite lacking.

This is not to say, however, that git is superior to subversion (that tired argument can be found elsewhere). There are most certainly situations where subversion is clearly the correct choice. Even at our office, our main code base is in subversion because we have a work-flow that matches so well to subversion.
<h3>Frame-accurate seeking</h3>
Awhile back we decided that since we work on face recognition, we really need a good solution for video input. Our requirements were a little different than most, though. We don't care much about audio, or time information because we aren't doing playback. We have more of a "video processing" need. That meant we needed a video input solution that was:
<ol>
	<li>cross platform</li>
	<li>supported a wide range of codecs and formats</li>
	<li>supported frame accurate seeking</li>
</ol>
The only video i/o solution that comes close (you pretty much lose everything else at "cross platform") is ffmpeg.

You wouldn't think this was a big list of requirements. I didn't. And boy was I wrong. As it turns out (that's code for "there's alot more to this painful painful story, but the wounds are still too fresh to talk about"), it's quite difficult to do frame accurate seeking in a format or codec agnostic fashion. And by "difficult" of course I mean "essentially impossible". It struck me as amazing, at first, that simple questions like "how many frames does this video have?" aren't exactly easy to get (the only foolproof way to do that is to decode them and count them, and even that doesn't always work). Even worse, trying to seek to a particular frame of a particular video (let's say frame 192) turns out to be even more impossible. However, the utter painfulness of modern digital video is a topic for a different day.

So we sat down and decided to write a little wrapper library that was reasonably capable of doing what we needed. We did a pretty good job in the end, but I'm certain there are still a few bugs. If you ever need frame accurate seeking, I urge you to give it a try.
<h3>Throwing our project "over the wall"</h3>
The point of this whole story is simple: this is a perfect project to open source. So I sat my bosses down and made the easiest pitch ever. It's not our core competency (we do face recognition), we have a vested interest in it working as well as possible, and we don't devote the time and effort to make it perfect (it would be a Herculean effort). Let's open source it and if just one person fixes one bug, it'll be better for us in the end. They agreed, I was happy, so let's do it. I went ahead and made a Sourceforge page for my<a href="http://sourceforge.net/projects/ffmpeg-fas"> Frame Accurate Seeking Extension to ffmpeg</a> <a href="http://sourceforge.net/projects/ffmpeg-fas"></a>page and uploaded the code.

The project wasn't really a success. Only a handful of people used it, but that was alright. It was useful. Early on, I enjoyed reading emails and answering questions from the few people who were using it. Over time, though, I moved back to working on what it is I normally do, and the video stuff became a bit of a burden. The problem was, though, I was the "owner" of this project on Sourceforge, it didn't have any sort of critical mass, and I had no interest in all the administrative nonsense that went along with such a position. I didn't really want to answer people's emails, or test people's patches, etc. I wanted to "let it go". The problem was, when using centralized version control through Sourceforge, "letting go" of such a small project is essentially equivalent to killing it.

I wanted to take this corporate project and toss it over the proverbial wall.
<h3 style="text-align: left;">Enter git (with the help of github)</h3>
There is a very obvious parallel between git/svn and the whole web 2.0 craze. Subversion is Slashdot. Git is Digg/Reddit. Does that make sense? There is no centralized governor in git. In general, git repositories end up with very obvious centralized branches that form the backbone of the project but this is arrived at organically. Git, in this sense, is a much more "social" tool where it's very easy for anyone to contribute and the make-up of the full project is the sum of all these individuals. Because git is so much more "social" than subversion, it makes sense that a "<a href="http://github.com">social coding" sites like github</a> would spring up.

The beauty of distributed version control is that there is no owner. There is no red-tape or permissions or any of that stuff. It's the perfect place for a single person to work on whatever it is they want but within public view. That way, if someone else is interested, they can come along, with no permission from the first, and add whatever it is they want. This is incredibly desirable for situations just as mine.

Git and github work together to form some bizarre <strong>social distributed version control system</strong>. The way it works is simply that you host your git projects on github, such that anyone can fork it, and all of the branches are tracked through a nice online and visible interface. You can then go back at some later date, see all the forks and all the patches in those forks, and incorporate whatever you want back into your project. It's a very slick solution to both hosting and tracking forks.

It's hard to explain to someone who has hasn't "seen the light" how perfect this synergy is. The best way I can describe it is that git and github make open sourcing and collaborating easier than it has ever been. It greases the wheels between individuals to such a degree that you can (almost) remove all of the organizational overhead in your average open source project. It lowers the bar of "life" for a project so low that they cannot really "die" as they will just sit there waiting for someone to fork the project and improve it.
<h3>Letting go with git + github</h3>
So since I realized I didn't really want to actively manage my little project, I wanted to leave it in a state that anyone could easily take over, if they wanted. Git and github provided a substantially better mechanism for this than subversion and sourceforge. <a href="http://github.com/lbrandy/ffmpeg-fas/tree/master">So, I moved the project over to github</a>. It may die a quiet death there (which will be alright) but at least this way I've provided it for anyone who might find it useful and I've removed all the painful red tape of anyone else creating, modifying, and building on what I started.

We all have those projects that would otherwise die on our hard drive. They aren't worth uploading to some "heavyweight" hosting site. This is where github kicks in to perfection. Just throw them up there. Chances are really good that no one will ever look at it. But what's the alternative? Let it die when you next wipe the hard drive? Let's say you share it and 6 months later someone wants to change it, all they have to do is fork it and change it. They don't need to email you to talk about it and send you a patch that you need to test (can you trust their code?) etc, etc. And if you don't care anymore, don't care. Ignore it, if you want. If 6 months later, you come back to the problem, you can see the work they did when you are ready, and pull in any changes you want.

By lowering the friction coefficients due to administration and collabaration, git + github have created this entire new class of open source projects that are "healthy" despite their smallness (whether in audience or even usefulness). This is a place where people can upload the smallest of their personal work and together with a few other people, seperated by a great deal of time, cobble together small but useful things. Connection and collaboration at this level was just too onerous to be useful, in the past.