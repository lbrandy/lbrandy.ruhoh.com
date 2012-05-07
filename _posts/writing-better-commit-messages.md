---
title: "Writing better commit messages"
date: '2009-03-30'
description:
categories:
tags: []

layout: post

---
If you and your team are in the habit of writing good commit messages, it can save everyone a tremendous amount of time and effort. Other developers can very quickly see what you've done. It'll also save tons of time tracking down commits from the past when you need to find them. A good commit message serves exactly two purposes: it gives other developers an explanation of the commit, and it gives some documentation for future searching.
<h3>You aren't special</h3>
Everyone thinks they write great messages. Most of the time you probably do. But everyone, including you, phones it in from time to time. It's true, admit it. I know you think you write awesome commits but if we looked at your last 100, how many would we truly classify as awesome? Just for fun, try it. I just did. It wasn't pretty.
<h3>Make "atomic" commits</h3>
This isn't really about the message, per se, but it's too important to not mention. A commit should be one (and just one) logical unit. It should be something that someone might want to patch or revert in its entirety, and never piecewise. If it could be useful in pieces, make separate commits. This will result in short, clear, and concise commit messages. Non-atomic commits make for awful run-on commit messages.

<em>A run-on commit:</em>
<blockquote>Fixed a few bugs in the interface. Added an ID field. Removed a couple unnecessary functions. Refactored the context check.</blockquote>
<p style="text-align: right;"></p>

<h3>Be specific. Make it search friendly.</h3>
<em>The worst message of all:
</em>
<blockquote>Fixed some bugs.<em>
</em></blockquote>
Hey wow, thanks for that.

Usually, this commit follows some previous larger commit that had a bunch of bugs. If so, say so! The lack of search-friendliness in the commit log can come back to haunt you. Be more descriptive. When you are skimming a commit log, or searching for a particular commit, these catch-all messages will be basically useless.

At the very least, name the important subsection/module of the code. "Fixed bad allocations in image processing routines" goes a long a way.
<h3>Communicate caveats</h3>
<em>Bad:</em>
<blockquote>Added super-widget 2.0</blockquote>
<em>Better:</em>
<blockquote>Very rough draft of super-widget 2.0. Compiles but is completely untested.<em></em></blockquote>
<blockquote>Tested + working super-widget 2.0... but the XYZ function() should be alot smarter to re-use previous computation</blockquote>
While your commit should never break anyone else's build, it's generally acceptable to commit things that aren't "patched in" and aren't necessarily fully working. Just state the important caveats in the commit. This is especially true if you have major line items to do.  The third example above states missing functionality for others to see (and possibly implement), and it provides fantastic information when looking at the log for a particular file or module.
<h3>Blame someone else</h3>
If you looked in our code base, you might see commit messages like this, from me:
<blockquote>Fixed a huge memory leak in Mike's code (which was cleverly hidden in the code I comitted yesterday... he is very crafty)</blockquote>
<h3>Place a bounty</h3>
Here's another example of a commit message I've made:
<blockquote>The most bizarre commit ever. It obviously changes the code. It also obviously makes the code faster in my tests. The problem is that it makes absolutely no sense, whatsoever. $5 to whomever convinces me that this works for some rational reason as opposed to my current theory: a combination of black magic and alien technology.</blockquote>
This has a happy ending as someone was able to come up with a plausible explanation for what was going on. Like almost all speed improvements, it was due to cache. You can find the <a href="http://lbrandy.com/blog/2009/03/more-cache-craziness/">nitty gritty details over here</a>.