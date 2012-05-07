---
title: "You can't beat a good compiler... right?"
date: '2010-06-07'
description:
categories:
tags: []

layout: post

---
Right! Sort of.

It is extremely well worn conventional wisdom that for your "average" programmer, it's pretty much impossible to beat a good optimizing compiler at writing fast code. For those who skip the "understanding" part, and jump straight into the "application" part, this rule of thumb tends to be grossly misunderstood, and misused. For these people, compilers are so smart, and so good, that micro-optimization is basically impossible (uh, no), or too hard (no), or even that they make assembly knowledge unnecessary or obsolete (not even close). This tends to lead to a mentality that optimization can be left to the compiler and often results in people warning others to not bother with micro-optimizations at all. 
 
Optimization, today, is largely about writing some naive code, looking at the assembly output, figuring out what you want to improve on, and then getting (or, often, tricking) the compiler into doing what you want. After several iterations of this, you end up with the code you want, and you gain all the benefits of having a compiler in the loop (portability, future-proofing, and so on). This process, though, obviously involves a great deal of low-level knowledge: assembly, cpu architecture, micro-optimizations that are likely to work, etc.

As an aside, I have a question: how exactly does one go about learning how to go beyond standard C into hardcore optimization? For me, it's been a long road of trial &amp; error, and random discovery. It seems to me that there is probably good resources out there for getting started on optimizing code (let's say in gcc). Know any?

<em>All the code I used can be found here: <a href="https://github.com/lbrandy/blog_examples">http://github.com/lbrandy/simple-optimization-test (see signal_blur.c)</a>. I ran all of these tests on Linux using gcc 4.3.3 and -O3. UPDATED: I changed the code to use c99's <code>restrict</code> keyword, instead of gcc's <code>__restrict__</code></em>

<h3>Getting yourself into trouble</h3>
Here is a naive (and contrived) one dimensional filter routine.

<pre>
#define LENGTH 5000

// a bad impersonation of a gaussian filter
const float filter[] = {0.01f, 0.2f, 0.58f, 0.2f, 0.01f};

void naive(float* in, float* out)
{
  int i,j;
  for (i=0;i&lt;LENGTH-4;i++)
  {
    out[i]=0.0f;
    for (j = 0;j&lt;5;j++)
      out[i] += filter[j] * in[i+j];
  }
}
</pre>

This is an interesting example because it contains a fatal flaw that might not be obvious. Take a second to understand what this code is doing. It's fairly simple, but critical to the rest of the discussion. Let's look at the assembly output of this, built  using -O3.

<pre>
08048430 naive:
 8048430:       55                      push   %ebp
 8048431:       31 c0                   xor    %eax,%eax
 8048433:       89 e5                   mov    %esp,%ebp
 8048435:       8b 4d 08                mov    0x8(%ebp),%ecx
 8048438:       8b 55 0c                mov    0xc(%ebp),%edx
 804843b:       90                      nop    
 804843c:       8d 74 26 00             lea    0x0(%esi),%esi
 8048440:       d9 ee                   fldz   
 8048442:       d9 14 82                fsts   (%edx,%eax,4)
 8048445:       d9 05 10 89 04 08       flds   0x8048910
 804844b:       d9 04 81                flds   (%ecx,%eax,4)
 804844e:       d8 c9                   fmul   %st(1),%st
 8048450:       de c2                   faddp  %st,%st(2)
 8048452:       d9 c9                   fxch   %st(1)
 8048454:       d9 14 82                fsts   (%edx,%eax,4)
 8048457:       d9 05 14 89 04 08       flds   0x8048914
 804845d:       d9 44 81 04             flds   0x4(%ecx,%eax,4)
 8048461:       d8 c9                   fmul   %st(1),%st
 8048463:       de c2                   faddp  %st,%st(2)
 8048465:       d9 c9                   fxch   %st(1)
 8048467:       d9 14 82                fsts   (%edx,%eax,4)
 804846a:       d9 05 18 89 04 08       flds   0x8048918
 8048470:       d8 4c 81 08             fmuls  0x8(%ecx,%eax,4)
 8048474:       de c1                   faddp  %st,%st(1)
 8048476:       d9 14 82                fsts   (%edx,%eax,4)
 8048479:       d9 44 81 0c             flds   0xc(%ecx,%eax,4)
 804847d:       de ca                   fmulp  %st,%st(2)
 804847f:       de c1                   faddp  %st,%st(1)
 8048481:       d9 14 82                fsts   (%edx,%eax,4)
 8048484:       d9 c9                   fxch   %st(1)
 8048486:       d8 4c 81 10             fmuls  0x10(%ecx,%eax,4)
 804848a:       de c1                   faddp  %st,%st(1)
 804848c:       d9 1c 82                fstps  (%edx,%eax,4)
 804848f:       83 c0 01                add    $0x1,%eax
 8048492:       3d 84 13 00 00          cmp    $0x1384,%eax
 8048497:       75 a7                   jne    8048440 naive+0x10
 8048499:       5d                      pop    %ebp
 804849a:       c3                      ret    
 804849b:       90                      nop    
 804849c:       8d 74 26 00             lea    0x0(%esi),%esi
</pre>

From the assembly, we see that the compiler has done quite a bit (if you don't know assembly, don't worry, I'll do my best to explain). First we see all of the address calculation involved in loading the filter coefficients has vanished (it is loading each one directly, e.g. <code>flds 0x8048918</code>). Second, notice that the (fixed sized) inner loop has been completely unrolled, resulting in each of the 5 multiplications and additions per iteration. So far so good.

There is, however, a very alarming surprise is this code. That is the quantity of store instructions (also loads). After every iteration of our inner loop (each filter coefficient), the result is stored. You can see 5 different store instructions (<code>fstps</code>, <code>fsts</code>) per iteration of this loop. Why? Let's have a look at the code again:

<pre>
void naive(float* in, float* out)
{
  int i,j;
  for (i=0;i&lt;LENGTH-4;i++)
  {
    out[i]=0.0f;
    for (j = 0;j&lt;5;j++)
      out[i] += filter[j] * in[i+j];
  }
}
</pre>

To the inexperienced, it might be bewildering why the optimizing compiler would generate 5 store instructions for <code>out[i]=</code> in the inner loop. Why wouldn't it just accumulate the answer in a register, and then store only the final result? The answer is: aliasing. The problem here is that compiler cannot assume that the pointers <code>*in</code> and <code>*out</code> are disjoint. It must store the result into <code>out[i]</code> each iteration because <code>out[i]</code> may be <code>in[i+j]</code> in the next iteration of the inner loop. With a bit of thought, it becomes clear how this code requires these stores to be correct in cases like <code>*out</code> pointing one float ahead of <code>*in</code>.

Another hard-learned tidbit: wasteful store instructions are terrible because stores can be incredibly expensive (far worse than an extra add or multiply).

<h3>Fixing it with restricted pointers</h3>

There are several ways to fix this problem, but in the spirit of teaching the art of optimization, I'll go with the use of the <code>__restrict__</code> qualifier (this is a gcc directive, but most compilers have some support for restricted pointers). The only change I made is to add <code>__restrict__</code> to the function declaration: 

<pre>
void naive_restrict(float *__restrict__ in, float *__restrict__ out)
{
  int i,j;
  for (i=0;i&lt;LENGTH-4;i++)
  {
    out[i]=0.0f;
    for (j = 0;j&lt;5;j++)
      out[i] += filter[j] * in[i+j];
  }
}
</pre>

This directive tells the compiler that you, the programmer, promise that <code>*in</code> and <code>*out</code> are disjoint, and no aliasing will occur. If you break your promise, don't expect your code to be correct. Here is the assembly of that output:

<pre>
080484a0 naive_restrict:
 80484a0:       55                      push   %ebp
 80484a1:       31 c0                   xor    %eax,%eax
 80484a3:       89 e5                   mov    %esp,%ebp
 80484a5:       8b 55 08                mov    0x8(%ebp),%edx
 80484a8:       8b 4d 0c                mov    0xc(%ebp),%ecx
 80484ab:       90                      nop    
 80484ac:       8d 74 26 00             lea    0x0(%esi),%esi
 80484b0:       d9 05 10 89 04 08       flds   0x8048910
 80484b6:       d9 04 82                flds   (%edx,%eax,4)
 80484b9:       d8 c9                   fmul   %st(1),%st
 80484bb:       d8 05 0c 89 04 08       fadds  0x804890c
 80484c1:       d9 05 14 89 04 08       flds   0x8048914
 80484c7:       d9 44 82 04             flds   0x4(%edx,%eax,4)
 80484cb:       d8 c9                   fmul   %st(1),%st
 80484cd:       de c2                   faddp  %st,%st(2)
 80484cf:       d9 05 18 89 04 08       flds   0x8048918
 80484d5:       d8 4c 82 08             fmuls  0x8(%edx,%eax,4)
 80484d9:       de c2                   faddp  %st,%st(2)
 80484db:       d8 4c 82 0c             fmuls  0xc(%edx,%eax,4)
 80484df:       de c1                   faddp  %st,%st(1)
 80484e1:       d9 c9                   fxch   %st(1)
 80484e3:       d8 4c 82 10             fmuls  0x10(%edx,%eax,4)
 80484e7:       de c1                   faddp  %st,%st(1)
 80484e9:       d9 1c 81                fstps  (%ecx,%eax,4)
 80484ec:       83 c0 01                add    $0x1,%eax
 80484ef:       3d 84 13 00 00          cmp    $0x1384,%eax
 80484f4:       75 ba                   jne    80484b0 naive_restrict+0x10
 80484f6:       5d                      pop    %ebp
 80484f7:       c3                      ret    
 80484f8:       90                      nop    
 80484f9:       8d b4 26 00 00 00 00    lea    0x0(%esi),%esi
</pre>

Now, you do not have to be an assembly expert to see how much more streamlined this code is. It consists almost exclusively of loads, multiplies, and adds with a final store at the end. This does exactly what we'd originally hoped. It realizes it can keep a temporary running sum and only store once at the end. We should also note that if you violate the restricted pointer promise, this code will not be correct!

It shouldn't surprise you to see how much faster this version is, either:
<pre>  naive: 0.672957
  naive_restrict: 0.160432</pre>
It's almost 5 times faster than the non-restricted version.

<h3>Going Forward</h3>
Though I haven't actually done it, my overwhelming suspicion is that this code still has a ways to go in terms of speed. The next step would be the use of SSE instructions. Maybe next post.

The take-away from examples like this should be that optimization cannot be "left" to the optimizing compiler. You have to know what you are doing to get a compiler to make fast code. And if you really know what you are doing (which means knowing assembly and the underlying architecture quite well), you can usually get a modern optimizing compiler to do exactly what you want. You have to be in the loop. Truly optimized C code ends up looking nothing like C at all.

With careful hand holding, you can get a compiler to make fast code. In that case, it can become difficult to beat a compiler with hand-optimized code. But that is not because the compiler is so good, but because you are so good at getting the compiler to make the code you want.