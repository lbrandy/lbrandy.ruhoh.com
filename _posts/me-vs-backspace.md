---
title: "Me vs Backspace: my war against a rogue character"
date: '2010-07-22'
description:
categories:
tags: []

layout: post

---
Amazingly, this is my second story about me and a <a href="http://lbrandy.com/blog/2009/11/the-8-hour-journey-to-a-single-character/">single character</a>.

A while ago, I began receiving reports from various people in IRC that I was prepending a garbage ascii character to some of my messages. I found this very odd. The complaints didn't stop. It became a running joke. Eventually, playful mockery. It is a bit demeaning to hang out in programmer corners and not have any idea how, what, or why your computer is misbehaving.

After a bit of digging, I discovered that the rogue in question was the character for <a href="http://www.fileformat.info/info/unicode/char/0008/index.htm">backspace</a>. Now, this is an odd character to be inserted into text because most often this character doesn't actually go anywhere, it informs the program that you want to, you know, backspace. This story gets a bit tricky here because not only does this character rarely make it into text, but most programs won't render it. Only certain programs, on certain platforms, will actually render the backspace character as anything (usually a box with a little 0x0008, or as ^H). So while other people were telling me about rogue characters, I never saw them.

My first suspicion was that the IRC program I was using, <a href="http://colloquy.info/">Colloquy</a>, was bugged (spoiler alert: it's not). I spent a long time asking colloquy/irc people, searching the googles, and otherwise trying to figure out how this rogue character was getting printed. I continued to fail. I continued to be mocked.
<h3>The plot thickens...</h3>
One day I recieved an instant message from my brother: "What is that weird character at the beginning of your messages?". Wait? What? My instant messages have the same character? Surely <a href="http://adium.im/">Adium</a> isn't suffering from the same bug, is it? How have I not heard of this before?

It turns out that most instant messaging programs don't render the backspace character. <a href="http://www.pidgin.im/">Pidgin</a>, however, does. And that day my brother was using Pidgin, and he saw the character of doom. I eventually noticed that I was apparently inserting rogue character using Safari, and later Firefox, all on my work computer (a Mac). It's important to note that none of my Mac programs -- Chrome, Safari, Firefox, Adium, or Colloquy -- would render the character, but they were all inserting it at the beginning of lines into random things. (You could see the character if you viewed my text using Firefox on windows or linux, for example).

I decided to wipe my Mac, reinstall the OS, and see if that fixed it. It didn't. I began to suspect this was a hardware problem having to do with my Mac. I spent a long time asking mac people, searching the googles, and otherwise trying to figure out how this rogue character was getting printed. I continued to fail. I continued to be mocked.
<h3>Luckily, my Mac was breaking anyway...</h3>
After this went on for close to a year, my Mac began having all kinds of problems including its charging circuitry, so I decided to replace my mac (or rather, lobby to have my work replace my mac). I bought a bright shiny new macbook pro and was good to go. I was pretty sure this would solve the problem.

Very soon thereafter, before I setup my new computer, I went to my <a href="http://news.ycombinator.com/">Hacker News</a> profile and saw this message: <a href="http://news.ycombinator.com/item?id=1531448">http://news.ycombinator.com/item?id=1531448</a> A user by the name of 'davidw' informed me that the stupid character appeared in a comment I wrote. There's only one problem: **I wrote that message using my wife's mac**. (<a href="http://www.youtube.com/watch?v=RSn0A7Kw5oI">if my life was a tv show, this is where the screen would go black -- end of episode</a>).

So I get my new computer setup, and ask the people in IRC if the character was still happening. It was! Gahh!!! This was good news, and bad news. It finally meant that I've reproduced this problem on three different macbooks in a variety of programs. It had to be something I was doing that was causing this.

I spent the next half-hour in IRC, talking to myself, trying to reproduce the problem. I finally figured it out.
<h3>TLDR: It's a Mac bug (I think)</h3>
**You can see the nasty character, live, in this comment**: <a href="http://news.ycombinator.com/item?id=1530832">http://news.ycombinator.com/item?id=1530832</a>. For many of you, however, this comment will look completely normal. That is because the program you are using doesn't render it. If you, for example, use firefox in linux, you will see the rogue character. I've got a screenshot for you:

<img src="http://imgur.com/QZ4rk.png" alt="" />

**Here's how to reproduce the problem, exactly**: On a mac laptop (and maybe others), you need to hold down LEFT SHIFT and an arrow key (LEFT ARROW works great). While holding those two buttons, press backspace (or, to be precise, DELETE). The tricky part, however, is verifying that you've actually sent a rogue character, since none of the standard mac programs (that I know of) will render the character. The way that I verified the problem was to use Colloquy to send IRC messages to myself, reading those messages using emacs-irc. There are other ways, I am sure.

**Why I kept doing it**:  I often use the shift-&lt;arrow&gt; shortcut to highlight various bits of text. Most often I tend to do shift-UP to highlight an entire line and then hit DELETE to remove it. Obviously, if I do this incorrectly, it ends up replacing the entire line with the backspace character. As I type in the new line, it comes out as a perpended backspace character on my final submission.

**The million dollar question**: is this a bug, or is there some feature I'm inadvertantly using? Anyone got any bright ideas on how I could fix this (other than unlearning my shift-UP habits)?