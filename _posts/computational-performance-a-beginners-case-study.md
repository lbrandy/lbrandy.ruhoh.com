---
title: "Computational performance -- a beginner's case study"
date: '2009-07-06'
description:
categories:
tags: []

layout: post

---
So, not too long ago, I wrote <a href="http://lbrandy.com/blog/2009/03/more-cache-craziness/">this post</a>. In it, I asked the question which bit of code was faster:
<pre>/* going vertical */
for (x=0;x&lt;width;x++)
  for (y=0;y&lt;height;y++)
     a[y*width+x] = b[y*width+x] + c[y*width+x]</pre>
<pre>/* going horizontal */
for (y=0;y&lt;height;y++)
  for (x=0;x&lt;width;x++)
     a[y*width+x] = b[y*width+x] + c[y*width+x]</pre>
I made the unfortunate comment, at the time, that every programmer should know which is faster. It turns out that I spoke too soon and maybe was a bit shortsighted. I found <a href="http://stackoverflow.com/questions/997212/fastest-way-to-loop-through-a-2d-array">this post on stack overflow</a>. In it the questioner re-asks the question: which is faster, and why?

Sadly, the answer he is given, and the answer he chose as the "best", is almost completely wrong (UPDATE: the "community" eventually overturned the accepted answer and chose a better one). Since I was the cause of all this confusion, I figured I'd go ahead and give a detailed explanation of which is faster and why.

The 2d matrices are mapped in row-order, meaning you put each row into memory one after the other. (Contrasted with column order where each column is put into memory, one after the other.). It's really important you understand that fact before we proceed because the entire post hinges on that. If you were to store your matrices in column order, the entire logic of this post flips.
<h3>Science</h3>
Let them never say we programmers are not scientists. This is the scientific method at work. Let's test these hypotheses with some real experiments. <a href="https://github.com/lbrandy/blog_examples">I've uploaded the code I've used to github and you can find it here</a>.

For most of my experiments, I added two matrices of size 4096x4096 and stored the result into a third one. This is large enough to wash out any "cache memory" from our experiments. If your matrices are sufficiently small, you can fit the entire thing into large L2 caches, ruining the experiment. These matrices are about 67 MB which ensures that by the time you iterate through one, the beginnings of that matrix will have already been ejected from cache.

Let's start easy -- which is faster, traversing horizontally or vertically?

The answer is: horizontal, by a landslide. I've compiled two versions of the program, one with optimizations (-O3 -funroll-loops) and one without optimizations, and run both.
<pre>louis@noisy:~/simple-optimization-test$ ./slow
horiz: 1.123245
vert: 14.359954
louis@noisy:~/simple-optimization-test$ ./fast
horiz: 0.525076
vert: 15.049684</pre>
It's not even close, really. Without any compiler optimizations, the horizontal method is about 15x as fast while with optimizations, it's closer to 30x. It's also clear (and possibly bewildering) that the compiler optimizations do help the horizontal but do not help the vertical.

So now that we know which is faster, the question moves to why.
<h3>Hypothesis 1: <a href="http://stackoverflow.com/questions/997212/fastest-way-to-loop-through-a-2d-array/997273#997273">The stack-overflow hypothesis.</a> Are we CPU bound?</h3>
Let me quote the "chosen" stack overflow answer:
<blockquote>So if you're scanning vertically, the next index is calculated as:
<pre class="prettyprint"><code><span class="pln">index </span><span class="pun">=</span><span class="pln"> row </span><span class="pun">*</span><span class="pln"> numColumns </span><span class="pun">+</span><span class="pln"> col</span><span class="pun">;</span><span class="pln">
</span></code></pre>
however, if you're scanning horizontally then the next index is just as follows:
<pre class="prettyprint"><code><span class="pln">index </span><span class="pun">=</span><span class="pln"> index</span><span class="pun">++;</span><span class="pln">
</span></code></pre>
<strong>A single addition is going to be fewer op codes for the CPU then a multiplication AND addition</strong>, and thus horizontal scanning is faster because of the architecture of computer memory.</blockquote>
Now, let's remember that the horizontal version is between 15 and 30 times faster depending on our compiler optimization settings. Immediately, you should be highly skeptical of this answer. How could a single instruction, or two, make such a staggering difference? This is a fairly easy to test hypothesis, as well. If we look at the inner loop assembly of the unoptimized version of the code, we see the follow code snippets.
<table border="0">
<tbody>
<tr>
<th> Vertical_Add (unopt.)</th>
<th> Horiz_Add (unopt.)</th>
</tr>
<tr>
<td>
<pre>        movl    -4(%ebp), %eax
        sall    $12, %eax
        addl    -8(%ebp), %eax
        movl    %eax, -12(%ebp)
        movl    -12(%ebp), %eax
        sall    $2, %eax
        movl    %eax, %edx
        addl    16(%ebp), %edx
        movl    -12(%ebp), %eax
        sall    $2, %eax
        addl    8(%ebp), %eax
        flds    (%eax)
        movl    -12(%ebp), %eax
        sall    $2, %eax
        addl    12(%ebp), %eax
        flds    (%eax)
        faddp   %st, %st(1)
        fstps   (%edx)
        addl    $1, -8(%ebp)</pre>
</td>
<td>
<pre>        movl    -4(%ebp), %eax
        sall    $12, %eax
        addl    -8(%ebp), %eax
        movl    %eax, -12(%ebp)
        movl    -12(%ebp), %eax
        sall    $2, %eax
        movl    %eax, %edx
        addl    16(%ebp), %edx
        movl    -12(%ebp), %eax
        sall    $2, %eax
        addl    8(%ebp), %eax
        flds    (%eax)
        movl    -12(%ebp), %eax
        sall    $2, %eax
        addl    12(%ebp), %eax
        flds    (%eax)
        faddp   %st, %st(1)
        fstps   (%edx)
        addl    $1, -4(%ebp)</pre>
</td>
</tr>
</tbody>
</table>

You do not need to be an assembly expert (or even a novice) to realize that <strong>these two inner loops are absolutely 100% identical.</strong> The only difference occurs outside the computational portion of the loop where the loop variables are incremented, and in which order.

So while it is true that a perfectly optimized horizontal add will have less instructions than a vertical add, that is most certainly not the end of the story.
<h3>Hypothesis #2: My hypothesis. Are we cache bound?</h3>
(note: other stack overflow respondents share my hypothesis, and they deserve credit, as well). Horizontal adds are better because they make better use of cache. Specifically, they make accesses to memory in sequential order. A horizontal add accesses memory in order from start to finish. A vertical add accesses memory in a strided fashion incrementing by large chunks through memory. This is not a cache-friendly behavior.
<h4>A quick cache primer</h4>
When you access a memory address, the computer loads it into cache, along with its neighbors. This is called a <em>cache line</em>. On my CPU, the cache line size is 64 bytes, or 16 floating point numbers. That means when you load up a particular address, 15 of his neighbors are coming along for the ride. Since we store our matrix in row order, that means when I ask for a particular element, the CPU will cache 15 neighboring elements to his left and right. These cache lines are 64-byte aligned, which means if you ask for 0x07, you are going to get 0x00 through 0x3F (these numbers are multiples of 64).

(note: My example has a few contrived elements to minimize complexity. I used valloc() in my test program, and I made sure my width was a multiple of 64. The net effect of these assumptions is that the beginning of each row is always the beginning of a cache line, and each row is always a clean multiple of the cache line size.)
<h4>A cache-eyed view of our algorithms</h4>
**Horizontal**. You will load up the first element and you get the 15 following elements (the cache line) "for free". You then proceed to use those 15 in order, after the first. At this point, you request the next element (the 17th), and get the next cache line, which you then compute on, and so on. This fits quite nicely.

**Vertical.** You will load up the first element, like before, and get the 15 elements to his right "for free". You promptly ignore those 15 elements, and proceed to jump down to the next row (say, 4096 elements away, if that is the width of the row). You will then load up the second element of the first column, including his cache line (the 15 elements to his right), compute only him, and proceed to the third element. And so on.

In the horizontal case, you load up all 16 elements and use them. In the vertical case, you are loading up 16 elements to compute only one of them.  On average, each element is loaded ONCE in the horizontal case, and each element is loaded 16 times in the vertical case (computed once, ignored 15x). T<strong>his means you are doing 16x as many memory to cache loads in the vertical case.</strong>

This hypothesis is immediately appealing because 16x is on the same order of magnitude of the timing differences we've seen.<strong> It also explains why compiler optimizations don't help the vertical.</strong> If we are entirely cache bound, removing unnecessary instructions isn't going to help.

Can we test this more fully? Well. Yes. Let's <strong>use</strong> those extra guys we've loaded. Let's try this bit of code:

<pre>
void vert_add2(float *in1, float *in2, float *out)
{
  int i,j;
  for (j=0;j&lt;WIDTH/16;j++)
    for (i=0;i&lt;HEIGHT;i++)
      {
        int index = i * WIDTH + j*16;
        out[index]=in1[index]+in2[index];
        out[index+1]=in1[index+1]+in2[index+1];
        out[index+2]=in1[index+2]+in2[index+2];
        out[index+3]=in1[index+3]+in2[index+3];
        out[index+4]=in1[index+4]+in2[index+4];
        out[index+5]=in1[index+5]+in2[index+5];
        out[index+6]=in1[index+6]+in2[index+6];
        out[index+7]=in1[index+7]+in2[index+7];
        out[index+8]=in1[index+8]+in2[index+8];
        out[index+9]=in1[index+9]+in2[index+9];
        out[index+10]=in1[index+10]+in2[index+10];
        out[index+11]=in1[index+11]+in2[index+11];
        out[index+12]=in1[index+12]+in2[index+12];
        out[index+13]=in1[index+13]+in2[index+13];
        out[index+14]=in1[index+14]+in2[index+14];
        out[index+15]=in1[index+15]+in2[index+15];
      }
}
</pre>

In this case, I am still traveling "vertically", but by cache lines, not elements. I load up the first cache line of the first row, compute it. I then load up the first cache line of the second row, compute it. And so on. If this hypothesis is true, this should be much faster than the normal vertical addition.

<pre>
louis@noisy:~/simple-optimization-test$ ./fast
horiz: 0.581028
vert1: 15.797579
vert_add2: 1.531041
</pre>

With this simple change, we've made the vertical code 10x faster. This is strong evidence that our code is cache, not CPU bound.
<h3>Follow-up #1: Can the vertical code be as fast as the horizontal?</h3>
Probably not. As the stack overflow patron rightly pointed out, in the end, vertical code will need a marginal amount of extra code. I suspect the effect of these extra instructions will turn out to be extremely trivial in reality.

The real reason it's difficult to ever make the vertical code as fast as the horizontal code is because CPUs have built-in hardware prefetchers. The behavior of modern hardware prefetchers is fairly complicated and their behavior, alone, could fill many posts of this size. The short version is that a CPU that loads one cache line after the next, in order, is very likely to have some hardware mechanism built-in that begins prefetching cache lines to minimize the wait time. Accessing one line after the next is an extremely common operation. For example, <a href="http://www.techarp.com/showfreebog.aspx?lang=0&amp;bogno=282">adjacent-line prefetching</a> is a fairly common strategy.

It would be fairly difficult to make the CPU prefetch cache lines optimally in the vertical case. Likewise, the CPU is almost certainly prefetching optimally in the horizontal case, without any help at all.
<h3>Follow-up #2: Can't this horizontal code be made even faster?</h3>
Many, many, many people (including people on stack overflow) will see my code:

<pre>
void horiz_add(float *in1, float *in2, float *out)
{
 int i,j;
  for (i=0;i&lt;HEIGHT;i++)
    for (j=0;j&lt;WIDTH;j++)
      {
        int index = i * WIDTH + j;
        out[index]=in1[index]+in2[index];
      }
}
</pre>

... and feel the uncontrollable urge to "optimize" this...

<pre>
void fast(float *in1, float *in2, float*out)
{
  int i;
  for (i=0;i&lt;HEIGHT*WIDTH;i++)
    out[i]=in1[i]+in2[i];
}
</pre>

This is obviously faster. Right? Certainly, without compiler optimizations, it will be. But is the compiler smart enough to do away with the unnecessary calculations and do what is "right"?

<pre>
louis@noisy:~/optomization$ ./slow
horiz: 1.669533
fast: 1.273352
louis@noisy:~/optomization$ ./fast
horiz: 0.530805
fast: 0.531471
</pre>

Laugh. I ran this about 10 times and the "fast" version won sometimes and lost others. On average and unscientifically, I'd say it might be a little faster. At best, this is an extremely marginal improvement.

In the grand scheme of things, this optimization is completely and totally unnecessary. It provides, at best, a barely measurable improvement. And if this bit of code turns out to be a bottleneck...
<h3>Follow-up #3: No seriously, can this be made even faster?</h3>
<a href="http://en.wikipedia.org/wiki/Streaming_SIMD_Extensions">Yes, it can.</a> That is left, however, as an exercise for the reader.<a href="http://en.wikipedia.org/wiki/Streaming_SIMD_Extensions">
</a>