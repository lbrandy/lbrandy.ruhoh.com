---
title: "Silence is not golden."
date: '2010-06-29'
description:
categories:
tags: []

layout: post

---
So <a href="http://www.rethinkdb.com/blog/2010/06/will-the-real-programmers-please-stand-up/">RethinkDB</a> wants to know where all the real programmers are. I do too. While I can commiserate with their post, there is one huge issue I have with it. That is the issue of silence.

Let me start by saying that the primary purpose of RethinkDB's post wasn't to discuss their interview philosophy (it was to generate good leads -- if you are looking for work, by all means, go apply). That means this post is probably slightly unfair to them in that I'm about to construct a gigantic strawman out of their post. However, I believe this template is so common that it still applies, in general.

As I've said here from time to time, I do quite a bit of the HR stuff for our small (startup -- when are we no longer a startup?) company. I've been doing technical interviews fairly frequently for a few years now. One of the biggest lessons I've learned as an interviewer is that <strong>silence</strong> is often times <em>my</em> fault, not theirs. If an interview is mostly silence, the interviewee was either woefully unqualified (ie, it should have never gotten this far), or the interviewer lost them.

Silence is not a sign of just ignorance, it is almost always a sign of ignorance mixed with confusion or panic. If you ask someone a direct question "do you know what X is?", they may think for a minute, but they will usually say "no". Silence, however, usually means "I do not 100% know what they want me to say, and I need to think of the answer that is least wrong".

Let's use one of their examples.
> How would you implement a read-write lock?
It doesn't surprise me such a question would result in silence. It's actually two questions.<em> Do you know what the term "read-write lock" means</em> and <em>how would you actually implement one</em>? For someone who was recently a student, or someone who hasn't done much concurrency recently, this sounds an awfully lot like an exam question.

On the inside it's a bunch of panic...

Well, <em>what -is- a read-write lock? Is that what you are asking me? Am I supposed to know what a read-write lock is? What class was that in? The one with the philosopher's dinner table? Yea, probably. It's some kind of concurrency thing, probably. It's probably related to reading and writing? Uhm, that's not a very good hint... Are they really asking me for the definition? Am I going to get marked down for not knowing the definition? </em>

On the outside, it's silence.
<h3>Say no to silence, interviewer and interviewee alike</h3>
> You don’t actually have to code it over the phone. Mentioning starvation issues is bonus points. For heaven’s sakes, just give us something.
>
> We try to ask about the difference between cooperative and preemptive multitasking. We try to ask about condition variables. 19 out of 20 times there is silence on the other end.

There's a good lesson for everyone here. Silence is pure poison in an interview. There should be all of five seconds of silence before you give up and answer their question with a question. If you are being interviewed, say something. "Let me make sure I understand what a read-write lock is, first. Is that when you can have many readers and no writers, or just one writer?" Even if you are wrong, you can at least get them to specify what they mean, and then you can try to answer the question that's been asked.

Even saying "I don't know what a read-write lock is." is almost certainly better than pure silence. Yes, it's a negative statement, but if I tell you, and then you proceed to discuss it flawlessly, I'll chalk it up to your textbook using a different term (or you just forgetting the vocabulary). No harm, no foul.

**And then there is the flipside of this conversation**: the cold, hard, reality that every interviewer faces from time to time. If an inordinate amount of interviewees are troublingly silent, it <i>might</i> be because your standard are really high. There is, however, another explanation.

If you are the interviewer, you have to realize that silence breeds silence. It's usually easy to break down questions into parts that make it much less likely to be ambiguous and promote that silent, confused, panicked state. First, ask them if they know what a read-write lock is. Then ask them what it is. And once you've both agreed on the definition, ask them how they'd implement one. This simple modification results in far more "yes" and "no", and far less confused silence.

