---
title: "Unplanned planning"
date: '2009-12-07'
description:
categories:
tags: []

layout: post

---
Here are some rectangles:
<pre>
struct irect {int   top; int   bot; int   left; int   right;};
struct frect {float top; float bot; float left; float right;};
</pre>

Now, given those rectangles, you are asked to write a conversion from <code>irect</code> to <code>frect</code>.

<pre>
struct frect convert (struct irect i) {
   struct ans = {(float) i.top, (float) i.bot, (float) i.left, (float) i.right)};
   return ans;
}
</pre>

This might at first seem like a reasonable answer but... it's almost certainly not.
<h3>The problem</h3>
What is the area of a rectangle with corners (0.0,0.0) and (10.0,10.0)?

Now, how many pixels are in an image with bounds (0,0) to (10,10)?

Hopefully, your answers disagreed (or at least you can see how they could disagree). In our field, we deal with images. Lots and lots of images. One of the most fundamental data structures you can possibly imagine when dealing with images is the lowly rectangle. For us, a rectangle is a region of an image. And it’s this role, as a region, that creates all kinds of pain and heartache.

We can more clearly isolate the problem by asking what is the lower-right hand corner of the above integer rectangle? Well, it depends on exactly what we mean by the lower-right hand corner. If you want to know where to look in memory for the lower-right hand corner pixel information, the answer is (x=10,y=10). If you wanted to know the Cartesian coordinate of the true lower right-hand corner, the answer would be (x=11, y=11).
<h3>The solution?</h3>
The difficulty here is the conflation of two separate ideas into the same form. First we have the integerized “point” on the cartesian plane, and then we have the 1x1 region known as a “pixel” and specified by its index. How should pixel indices convert to the cartesian plane? Put another way, should an integer rectangle (0,0)x(10x10) have an area of 100 or 121? This is, to some extent, a question of convention. If you pick one, and are consistent, everything will work out fine. However, almost certainly, for your application, one convention will result in cleaner code.

**So the answer to the original question becomes a fairly complicated ordeal.** This one problem only scratches the surface of the painstaking care that must be taken when dealing with integer and floating point regions of pixels. You would need to figure out exactly how and why you use rectangles and what index convention you want to use. For every function that you write operating on rectangles, you need to carefully consider the implications of your chosen convention. And depending on the convention you use, the rest of your code is going to look very different.

Writing a rectangle class <em>seems</em> straightforward. Yet, all planning in the world won't prepare you because it’s almost impossible to anticipate this design issue. It's the simple act of trying to use one of your converted rectangles that makes the problem obvious. Almost paradoxically, this problem, once realized, can only really be solved by meticulous and careful planning. The devil is always in the details.