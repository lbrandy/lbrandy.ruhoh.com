---
title: "Some tips for getting started on Project Euler"
date: '2009-03-23'
description:
categories:
tags: []

layout: post

---
So the other day at work my boss casually mentioned that he had messed around with <a href="http://projecteuler.net/">Project Euler</a>. He knew I was a bit of a geek for <a href="http://lbrandy.com/blog/2008/09/what-code-golf-taught-me-about-python/">online programming fun and games</a>. Project Euler is a very large set of programming puzzles (237, to date) that tests your ability to solve largely mathematical (and often algorithmic) challenges. Brute force will in principle work, but in practice it tends to take a bit too long (sometimes longer than the age of the universe). Generally, the difficulty is in solving the problems efficiently so you can get an answer within a few seconds.

I knew of Project Euler but I had never really joined in the fun. He casually mentioned that he had reached <a href="http://projecteuler.net/index.php?section=scores">level 1</a>. Congratulations were clearly in order. This weekend I decided to give it a try. <a href="http://projecteuler.net/index.php?section=profile&amp;profile=lbrandy">I stopped after gaining level 2.</a> We thrive on one-upmanship. Ball's in your court, Mike.
<h3>Project Euler, a weekend vanished</h3>
So I ended up solving a good 60 or so of these problems (starting from the easiest) over a few hours a day this weekend. The vast majority of the first 25 problems are fairly trivial to brute-force if you have decent tools. With a decent high-level language many of these problems become fairly trivial.

The "second level" problems (25-50) start to require a bit more programming and a bit more thought, but you can still pretty much brute force your way through them without too much optimization.

Getting started is fairly easy, but if I could make a suggestion, choose your language wisely. Here are the basic functionality you'll need (either built-in or to build yourself):
<ol>
	<li>You need multi-precision support. If you don't have it, you'll spend alot of time inventing it. (if you want to use C/C++, <a href="http://en.wikipedia.org/wiki/GNU_Multi-Precision_Library">go here</a>)</li>
	<li>You need good type-conversion tools</li>
	<li>You need good containers</li>
	<li>Good functional programming support will help alot</li>
	<li> If you have a prime-number library, use it. You'll be building one up, if you don't.</li>
	<li>Same goes for permutations and combinations.</li>
</ol>
My language of choice, Python, had pretty much everything you'd need.
<h3>A quick example</h3>
Project Euler is constantly asking you treat numbers in non-standard ways. They'll want you to manipulate numbers like strings, like arrays of digits, and as normal numbers. This can be rough in languages that don't really support this. Here's an example:


> If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.
> 
> Not all numbers produce palindromes so quickly. For example,
> 349 + 943 = 1292,
> 1292 + 2921 = 4213
> 4213 + 3124 = 7337
>
> That is, 349 took three iterations to arrive at a palindrome.
> 
> Although no one has proved it yet, it is thought that some numbers, like 196, never produce a palindrome. A number that never forms a palindrome through the reverse and add process is called a Lychrel number. Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that a number is Lychrel until proven otherwise. In addition you are given that for every number below ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome. In fact, 10677 is the first number to be shown to require over fifty iterations before producing a palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).
> 
> Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is 4994.
> 
> How many Lychrel numbers are there below ten-thousand?

<p style="text-align: right;"><a href="http://projecteuler.net/index.php?section=problems&amp;id=55">Problem 55</a></p>
<p style="text-align: right;"></p>
<p style="text-align: left;">When I saw this problem, my inner C programmer cried out in pain. You need to reverse the digits of number. Ugh. You need to determine if a number is a palindrome. Double ugh. And don't forget that you'll need multi-precision integer math to actually compute this stuff.</p>
<p style="text-align: left;">It's just so much cleaner (and clearer) like this:</p>

<pre>
#SPOILER#

def is_palin(n):
    return str(n)==str(n)[::-1]

def rev(n):
    return int(str(n)[::-1])

def lychrel(n, iter):
    if iter &gt; 50: return True
    next = n + rev(n)
    if is_palin(next): return False
    return lychrel(next, iter+1)

def l(n):
    return lychrel(n,0)

print len(filter(l,range(1,10001)))
</pre>