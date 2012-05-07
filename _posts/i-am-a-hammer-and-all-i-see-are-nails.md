---
title: "I am a hammer and all I see are nails"
date: '2009-08-24'
description:
categories:
tags: []

layout: post

---
So a few weeks back I decided to write up my story about <a href="http://lbrandy.com/blog/2009/08/an-almost-perfect-hack/">my adventuers with the Allegheny County tax man and the court system</a>. The executive summary of that story goes like this: I got a letter summoning me to a hearing because the school district wanted to raise my property taxes. I wrote a web scraper to search the county website and walked into the hearing with tons of comparables. Turns out they didn't want to raise my taxes at all, and withdrew their appeal. I took the draw and walked out never showing anyone my comparables.

Here's one comment, from reddit, that caught me by surprise.
<blockquote>I'm a lawyer with computer nerd tendencies, so I'm always divided between two worlds. I love how, throughout the entire story, the author never just calls the tax authorities and tries to have a discussion, raising his points and seeing if it could get resolved without court. They probably knew well in advance that they would be dropping the appeal and all this hassle could have been avoided. From a strictly 'hacking' perspective, though, it is very interesting.
<p style="text-align: right;"><a href="http://www.reddit.com/r/programming/comments/974iy/an_almost_perfect_realworld_hack/c0bnw4l">downfell, reddit.com</a></p>
</blockquote>
I read that comment dumbfounded. Yes, they did probably know in advance.  And no, the thought absolutely positively never crossed my mind

It seemed to me that if you go to all the effort to write someone a letter and take them to local hearing, you mean business. This isn't something you do without meaning it. There's no way you set up a hearing, write a letter, and so on, and when the opposition calls you up and goes "C'mon bro... you aren't serious, are you?" you say "Ha ha. Just kidding. We'll drop the appeal".

Here's a follow-up question: if they knew they were going to drop the appeal, why didn't they do it? Why did they make me show up? Why didn't <em>they</em> call <em>me</em>?
<h3>Lessons learned</h3>
I've learned my lesson, dear downfell of reddit. I got such good feedback from various local sources about my little sojourn through the Allegheny property tax assessment scene that I decided to take my experience (and my scripts) one step further. I'm going to make a better, searchable database so other people can easily find comparables.  This is actually an incredibly simple problem. It's why relational databases were invented. All I need is data...

Instead of polishing up my webscraper, I just... asked. Dear county, can you provide me with your entire database. As it turns out, answer just might be yes. I have to submit an official request in writing, which I'm going to do, and we'll see how that goes. To be perfectly honest, I don't think I'd have even bothered with this step if it wasn't for that one comment on reddit.

The worst case scenario: mechanize+python will get me what I want.