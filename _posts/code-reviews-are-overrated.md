---
title: "Code reviews are overrated"
date: '2009-06-02'
description:
categories:
tags: []

layout: post

---
...but the notion that your code will be reviewed is most certainly not. I argue that the vast majority of the benefit of code reviews comes from the belief that many other programmers will look at this code and judge you for it. There is no doubt that this belief will produce better code. The ensuing review itself, though, adds quite a bit less value to the situation, especially given its cost. This distinction is important.

There are several types of code reviews ranging from desk checks (which taken to its natural extreme becomes pair programming) to full conference room thesis-defense-style interrogations. I am certain that these types of activities catch bugs, improve interoperability, and help programmers stay on the same page... but at what cost? Code reviews are terrifyingly expensive. Compulsory and frequent meetings (even impromptu ones at a desk) destroy the flow of a work day. It crushes the ability to get things done. It will slow down the best programmers for the possibility of improving the worst. I'm not a big fan.
<h3>Managers managing</h3>
A friend of mine works for a software development house who believes in code reviews. Their managers became convinced (undoubtedly at some management training seminar) that code reviews produce better code. Given that belief, it necessarily follows that more code reviews produce even better code. Managers constantly searching for ways to quantify and measure their employees developed a fun optimization: let's try to increase the number of eyeballs that looked at every piece of code. This rapidly became a classic case of non-technical management trying to invent ways to improve a process they do not understand. They found something they could measure that they believed correlated with code quality. Optimize it!

At first, there was formal code reviews. My suspicion says this produced a sizable increase in the quality of the code. This initial success and a touch of <a href="http://en.wikipedia.org/wiki/Confirmation_bias">confirmation bias</a> did the rest. Once a week meetings for code reviews probably isn't too disruptive. Next, they instituted desk checks before all commits. I suspect this added virtually no benefit. Now, though, throughout the day, someone might drop in in the middle of something you were working on and request your presence at their desk for a commit. If you want to finish what you are working on, they have to wait, if you go, you lose your train of thought. It's a lose-lose. And then, best of all, they decided that for each commit, each developer must send out an email containing the changes that were made, the files they are made to, and the diffs of the changes. All technical readers will note that this should be trivially automatic. It wasn't.

I'm certain that the programmers quickly automated the process anyway, but think, for a moment, about what these managers must be thinking. For every commit, you must have someone else come check your code, and then manually compose an email containing a whole bunch of information. The sheer amount of time used up in code reviews, reading emails, sending emails, dealing with distraction, and "re-immersion" for programmers must have been staggering. I'd doubt that anyone could get more than an hour honest work in per day. If they followed the concept in earnest, they would spend most of the time doing meta-work (work that lets you do actual work).
<h3>The real goal</h3>
If you are a manager and do not understand software, let me give you a piece of advice: interruptions are the devil. Instead of min/maxing whatever other variable you had in mind, try minimizing disruptions. If your developers know that their code will be extensively used, maintained, and extended, you already have most of the benefits of code review. The difference is it will be done organically and without the need for constant interruptions.

Our story has a happy ending. The programmers at said development shop, of course, adapted quickly. The emails were automated and the desk checks were ignored. The formal review was impetus enough for people to write better code. The only negative consequence turned out to be the revelation from manager to employee of the former's inadequacy.