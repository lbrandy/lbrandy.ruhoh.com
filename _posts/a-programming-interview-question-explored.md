---
title: "A Programming Interview Question, Explored"
date: '2008-08-20'
description:
categories:
tags: []

layout: post

---
At my office recently, we've been brainstorming often about programming interview questions. I especially dislike giving interviewees puzzlers or <em>gotcha</em> type questions. I define a <em>gotcha</em> question to be one that doesn't have a good continuum of hints that you could provide. There is some trick that they either figure out or they don't. It's very black and white. There are a bunch of reasons that these questions are bad questions. The primary one is they don't really give you the information you are naively hoping they will. They won't tell you if someone is smart. But my interview ideology is something for a different day.

Let me give you some examples of <em>gotcha</em> style questions.<br id="vuff4" />
<ol>
	<li>Determine if there are any loops in a linked list?  Now do so without marking any of the nodes, or any other supplemental arrays or other forms of book-keeping.</li>
	<li>Given a room with three switches connected to three light bulbs in
another room. There is no way to see from one room to the other. You
start in the room with the switches and are allowed to switch them as
you see fit.  Once finished, you go to the room with the light bulbs.
Upon seeing the state of the bulbs, can you figure out which switches
controlled which light bulbs?</li>
</ol>
These questions, as posed, require lightning strike of cleverness that can't be expected in an interview. Furthermore, though, what represents the <strong>fatal flaw</strong> in these types of questions is that most often someone who answers correctly does so only because they've heard the question before.
<br id="vuff21" />Good technical interview questions are the type of questions that have obvious trivial (and sub-optimal) solutions that allow you to iterate from least clever to most clever with some careful prodding. This allows you, the interviewer, to give them progressive hints that allow them to show how big of a leap make on their own. Compare this to a gotcha question where you'd sit there in silence where the only hints you can give are far too big. They are going to look around confused and pretty soon the combination of silence and lack of progress is going to distract them from the problem at hand. After a sufficient amount of awkwardness you are going to just tell them the answer, and they're going to do their best acting job to make them seem as smart as possible upon discovering this incredibly insightful trick. In their own head, they'll think you are a dipshit.

There are alot of good questions of the iterative variety but I've chosen one that illustrates the iterative nature perfectly. That said, this particular question probably isn't suitable for an interview because a full discussion of it probably takes too long. The real reason I want to talk about this question is because the most often stated answer is, at best, flawed, but I prefer to think it's just plain <strong>wrong</strong>.<br id="vuff28" /><big><br id="vuff29" /><strong>A Knight and a Dragon</strong></big><br id="vuff30" /><br id="pn95" />I first read this problem here: <a href="http://www.ocf.berkeley.edu/%7Ewwu/riddles/easy.shtml">http://www.ocf.berkeley.edu/~wwu/riddles/easy.shtml</a>. Here is my variation...
<blockquote>A dragon and knight live on an island. This island has six poisoned wells, numbered 1 to 6. If you drink from a well, you can only save yourself by drinking from a higher numbered well. Well 6 is located at the top of a high mountain, so only the dragon can reach it. One day they decide that the island isn't big enough for the two of them, and they have a duel. Each of them brings a glass of water to the duel, they exchange glasses, and drink. Who dies and who lives? <br id="vuff36" /></blockquote>
Let me start by saying that the problem is not perfectly well defined. Some things are left to the listener to assume. I've taken the liberty of making some "reasonable" assumptions in my discussion (e.g., one doesn't feel sick when he is poisoned, and drinking same-level poison does nothing). A good interview would likely contain discussion of these assumptions.
<big>
</big><strong><big>The Trivial Answer</big>
<br id="vuff41" /></strong>Obviously, the dragon kills the knight by feeding him poison #6 which he cannot cure.  Similarly, the dragon can cure any poison that knight has given him by flying up to #6 after the duel. This answer should immediately seem "too obvious" and therefore give anyone pause as choosing it as correct.
<big>
</big><strong><big>Step 2: The "Official" Answer</big></strong>

Once the trivial answer is stated, we can continue by getting to the meat of the issue:
<blockquote>If I told you that the Knight was very clever and the actual result was that he lived, and the dragon died? Can you figure out how this could happen?</blockquote>
The knight knows the dragon will try to poison him with #6. He can use this to his advantage. If the knight pre-poisons himself (say, by drinking from the level 1 well) before coming to the duel, the dragon's offering of level 6 poison becomes a cure. Similarly, he can provide the dragon with fresh water at the duel.  The dragon will then, believing himself poisoned, fly to the top and poison himself with now incurable level 6 poison.<br id="vuff51" /><br id="vuff52" /><a href="http://answers.yahoo.com/question/?qid=20060629083522AA2p8OH">This answer is usually how the riddle is "solved"</a>. Note my scare quotes. This answer is incredibly unsatisfactory because it depends on an assumption of a (somewhat) stupid dragon. In some sense, it's just plain wrong. A dumb dragon wouldn't behave this way and neither should a smart dragon.<br id="imu6" /><br id="imu60" /><strong><big>Step 3: The Real Answer</big></strong>
<blockquote>What if we assume both are equally clever? What's the optimum strategy for both Knight and Dragon?</blockquote>
Would it surprise you if I told you that the Knight cannot kill the dragon? Want to stop and think about it? The dragon can only successfully cure himself with the level 6 poison if he is already poisoned. He cannot be sure he is poisoned after the duel. Is that enough of a hint? What if we go step by step? What does the dragon know before the duel. What about after? What happens if he knows he poisoned by levels 1-5 water? The answer should become increasingly obvious and I'm sure most of you figured it out relatively early in this paragraph.<br id="vuff61" /><br id="vuff62" />The simplest way to do this is for the dragon to go to the duel, drink the knight's water and then go to the level 1 well and drink. By drinking level 1 poison, the dragon has assured himself of being poisoned with at least level 1 water and at most level 5 water. This guarantees that level 6 water will cure him.<br id="vuff67" /><br id="vuff68" />How about the Knight? Surely the disadvantage of no access to the level 6 well dooms him, right? What if I told you that the Knight, also, should always survive? Want to figure it out?<br id="vuff72" /><br id="vuff73" />The logic follows almost identically from the dragon's situation. If the Knight gets poisoned by level 6 water, he dies. Therefore, he must come pre-poisoned in order to avoid getting level 6 poisoned. Therefore, after the duel, the Knight is either cured by some higher level poison, or has his original level of poison. Given that knowledge, the Knight can pre-poison himself with level 1 and go to the duel. After the duel, he is either level 1 poisoned or cured. By re-drinking level 1, he guarantees himself to be level 1 poisoned. He can now cure himself at any of the higher level wells.<br id="vuff79" />

<strong><big>So as it turns out...
</big></strong>

So, as it turns out, the dragon's advantage of having the level 6 well isn't really an advantage.  The game as posed turns out to be alot like tic-tac-toe.  Someone appears to have a huge advantage but only against sub-optimal play. Against optimal play, neither person can win.<br id="vuff83" /><br id="zaq6" />The real interesting question: what variations of this problem could make it more difficult or produce more interesting results?