---
title: "The Hardest Test I Ever Gave (C++)"
date: '2008-11-24'
description:
categories:
tags: []

layout: post

---
So while attending the University of Florida, I was a TA for a variety of classes. One summer in particular I took on an extra job of teaching an intro to programming course for incoming engineering freshman. The course wasn't for credit so it let me be a little, shall we say, creative. Since the class was taught in a computer lab, the course was really me giving a tiny lesson and them then doing some assignment in class. I wanted them to have left the course having written many successful programs that solved simple problems.

But I also had to give a test. Ok, then. I sat down and made up a test. I had no intention of using the test in their "grades" (again, not for credit), so I wasn't worried too much about the difficulty. I should have been. It turned out way too hard. The test had the unintended side effect of causing the high-school-programmed kids to have a collective aneurysm (you see because 90% and above is an A, and so they were obviously failing, hard).

I was able to find the old course website. I've chosen some of the more entertaining questions so you can try it yourself...
<h3>Question #1 -- Syntax</h3>

<pre>
1. Which of the following will give a syntax/parse error? (circle all that apply)
(note, x is an integer)
*5 points*

1a) y = x++3;
1b) y = x+++3;
1c) cout &gt;&gt; "Hello";
1d) if (x+3) x=x+3;
1e) x = (x++ == 3 + x % (x=x=3));
</pre>

Not on the original test, but for bonus points, if x is 1 before 1e, what is x after that line?
<h3>Question #2 -- Evaluating Expressions</h3>

<pre>
2. What is the value of each of the following...
*5 points*

   2a.	11 % 3		_____
   2b.	2 - 6 * 2	_____
   2c.	3 / 1 + 1	_____
   2d.	5//3		_____
   2e.	(34 &gt; 19)	_____
</pre>

This should be straightforward. Except for 2d. That is just plain mean.
<h3>Question #5 -- Why? Seriously, why?</h3>

<pre>
5. What is the output of the following code?
*2 points*

int x = 0;
int y = 1;
int z = 2;

x = x + 1;
z = z + 1;
y = y + y - x;

if (x != z)
  {
  if (y = z)
     cout &lt;&lt; "This is the answer.";
  else if (y != z)
     cout &lt;&lt; "This is not the answer.";
  }

Output: ___________________________________________
</pre>

This problem screams "trick-question" but to no avail. Every single one of them got this wrong. Every. Single. One. That is quite frankly amazing considering it's essentially a 50-50 guess and I had about 30 students. I'll go ahead and put this challenge out. Try to come up with a 50-50 question that every single student in your class gets wrong.
<h3>Bonus Question #1 -- Words do not describe...</h3>

<pre>
B1) What is the _EXACT_ output of the following code:
*2 points*

void main(int)
{
int counter1, counter2, j, k;

j = k = counter1 = counter2 = 0;

while (counter1++ != 10)
   while (counter2++ &lt; 10)
	j = counter1 + (k = k + counter2);

cout &lt;&lt; 'j' &lt;&lt; 'k';
}

Output: ______________
</pre>

I failed.