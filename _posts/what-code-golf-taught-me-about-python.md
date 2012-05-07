---
title: "What Code Golf Taught Me About Python"
date: '2008-09-29'
description:
categories:
tags: []

layout: post

---
So I've become seriously addicted to <a href="http://codegolf.com/">code golf</a>. For those that don't know, code golf is a competition where you try to pass some programming test with a program consisting of the least number of characters. I chose to play code golf in Python because I wanted to learn more about the language. I'll probably eventually do the same for Ruby.

I know the title of this might be controversial. There's alot of people who have never tried it, know no one who has, but still have strong opinions on why golfing is a negative practice to undertake. These people are wrong. Golfing is just a programming puzzle. It doesn't remove your ability to recognize ugly code. Anyone who tries to "golf" outside of a golfing context has bigger problems.

What follows is a brief guide to the idioms that I learned through code golf <strong>that could be useful in real programming</strong>. It will also serve as a helpful set of tips for python golfers. I'll probably do a followup post with idioms that are useful but are completely worthless for any real programming.

I am by no means a code golf expert. I recently attained the 6th rank and have 5th well within striking distance, but my average per "hole" isn't staggering. So please keep in mind this is by no means a definitive list of techniques required to be successful. If anyone wants to email me some tips on the<a href="http://codegolf.com/dancing-queens"> Dancing Queens</a> puzzle, feel free. I've been beating my head against a wall on this one for a few weeks and haven't even gotten close to Mark Byer's 100. I don't know Mark, but I'd like to shake his hand.
<h3>White Space</h3>
Most people (wrongly) believe that white space is the reason Python is a poor language for golfing. In very few cases do the white space rules result in longer python programs. (The real reason that Python gets soundly beat by Ruby or Perl is a combination of the verbose nature of the standard python library and the strictness with types that requires additional keystrokes to overcome.)  Back to our war on white space...
<ol>
	<li>You can almost always turn single if/while/for loops into one-liners</li>
	<li>Nested control structures that require white space  aren't used as often as you think</li>
	<li>exec can save the day (not useful for real programming!)</li>
</ol>
The second point will be covered by some of the techniques below so let's deal with the first.

<pre>
if a:                 # before
  bob()
  jim()

if a: bob();jim()     # after
</pre>

Simple. Effective. One line if/while/for<em> </em>statements shouldn't be used in regular python very often but there are times when removing that white space can sometimes substantially clean up the code.
<h3>Functional Programming</h3>
Hopefully this is obvious but code golfers should be ready and willing to map() all kinds of things all over the place. Fall in love with map(). You generally won't use reduce() in golf because most often, after mapping, you'll tend to use either join() or sum() or something along those lines. Lambdas also get a fair bit of action in code golf. You'll become much more familiar with this section of the language.
<h3>Conditional Moves</h3>
Often times your if statements are nothing but glorified <a href="http://www.x86.org/secrets/opcodes/cmov.htm">conditional move instructions</a>. Those if statements can almost always be replaced by simpler statements:

<pre>
if a&lt;0:                        # beginner python
  b=2*a
else:
  b=3*a

b=2*a if a&lt;0 else 3*a          # proper python

b=a&lt;0 and 2*a or 3*a           # codegolf1
b=a*(3,2)[a&lt;0]                 # codegolf2
</pre>

Now, all of the above idioms have pros and cons as far both function and readability. Let's get the caveats out of the way. The first code golf technique above only works if your first expression doesn't evaluate to 0. The second code golf expression doesn't short circuit (so, for example, <code>(0,a/b)[b!=0]</code> does not prevent division by 0).

All three of these idioms (if/else, and/or, and the index into a tuple) are worth understanding and recognizing. They can all be very powerful in certain real world situations.
<h3>Operators</h3>
Code golfers become intimately familiar with the order of operations (removing those parentheses!). This is extremely useful information to know by heart, but you shouldn't be dropping those parentheses in your real code.  As a special note, the two string operators, * and %, are crucial. Most people are hopefully aware of these already. '%' is the string formatting operator. As a code golfer, you will master it and all its variants. Similarly, strings can be multiplied by integers to repeat them. If you want a hint of how powerful these can could potentially be for a code golfer, think about multiplying and string formatting mixed with the <a href="http://docs.python.org/ref/exec.html">exec command.</a>
<h3>Booleans as Values</h3>
Here is where alot of the magic begins to happen. When all else fails, Python will treat a Boolean True as an integer value 1, and a False as 0. This becomes extremely powerful when mixed with some of the techniques above.
<pre>print "Good Morning!" + (mailcount&gt;0)*" You have new mail!"
print "You have %d email message%s."%(mailcount, 's'*(mailcount != 1))</pre>
<h3>Miscellaneous</h3>
Here's a grab bag of other useful things. Hopefully this is self-explanatory.
<pre style="text-align: left;">a=b=0                    # I had no idea python let you do this
transpose=zip(*list)
rev = anything[::-1]     # reversed() that works on any sequence
print `x`+`y`            # convert to string (via repr)
print x,                 # ends print with a space (instead of a newline)</pre>