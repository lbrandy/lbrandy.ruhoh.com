---
title: "How We Made Our Face Recognizer 25x Faster"
date: '2008-10-27'
description:
categories:
tags: []

layout: post

---
This is a war story from my real day job. I work at a start-up company in Pittsburgh that does face detection, tracking, and recognition software. This particular problem involved optimization of the face recognizer.

I'm going to try to simplify our face recognition algorithm as much as possible to get to the point I'm trying to make. If you are reading this to try to learn our algorithmic secrets, you'll be sorely disappointed. What you'll see here is in the first few chapters of a pattern recognition textbook.

Recently, we came out with a brand new version of our face recognizer. As is usually the case, once they are happy with the accuracy they hand it off to me to see if I can speed it up.
<h3>The Problem</h3>
Comparing faces tends to grow quadratically with the number of input faces. When you imagine comparing 1000 faces to another 1000, that equals a million comparisons. Here's the pseudo-code of that operation:
<pre>for i in range(face_list1):
   for j in range(face_list2):
      answer[i,j] = compare(face_list1[i], face_list2[j])</pre>
When you look at this code, notice how threadable this problem is. These comparison operations are completely independent, numerous, and sizable amounts of computation. This is a concurrent programmer's <strong>DREAM</strong> problem. So when it came time to parallelize this algorithm, I wasn't worried. This is what one might refer to as an <a href="http://en.wikipedia.org/wiki/Embarrassingly_parallel">embarrassingly parallel</a> problem. Our speed-up should be identical to the number of CPU cores.

So I sat down, as I've done many times, whipped up a little thread pool, instantiated my thread-safe queue with a mama-process for feeding the workers. We generate a to-do list, dump them all on the queue, and have the worker threads go to town on the other end of that queue. This is a pretty standard solution. Before lunch I was ready to fire it up and I saw the most beautiful thing a concurrent programmer can ever see:
<pre>  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
32603 louis     16   0  246m  24m 4620 S  800  4.8   0:09.12 recognize</pre>
Just in case you aren't familiar with the output of top, this is showing my program using all 8 CPU cores (dual quad-core). Problem solved. I went to lunch.
<h3>Not So Fast</h3>
A funny thing happened over lunch. My test finished running and the results weren't what I expected. Having an embarrassingly parallel problem and a CPU pegged at 800%, you'd expect an 8x speed-up. That's not at all what happened. We ended up with about 3x improvement. Since our CPU is pegged at 800%, it's not a synchronization problem. Having been down this road a time or two, I was fairly certain of the culprit but took a moment to prove it. It wasn't due to file I/O or anything like that (since none of that stuff was present). With a little use of <a href="http://oprofile.sourceforge.net/news/">oprofile</a> (which deserves its own post, one day), I could tell the time was spent in user space, and not the kernel, which removes things like page zeroing or page faulting. Cache misses, on the other hand, are "assigned" to the user process.

Our code was cache bound.
<h3>The Inner Loop</h3>
I'm going to strip out all of the layers and show you the entire algorithm, simplified. Take my word for it, however, that in our ordinary code base, these loops were separated by numerous layers of abstraction, function calls, and a gigantic mass of book-keeping. It should be fairly trivial to understand <strong>what</strong> the algorithm is doing. How and why it works, though, are topics for a pattern recognition class.
<pre>for face1 in face_list_a:                                    # on the order of 1000
   for face2 in face_list_b:                                 # on the order of 1000
     for feature in features:                           
         feature_list[feature] = extract_feature(feature, face1, face2)                                
     answer[face1][face2] = classify(classifier, feature_list)</pre>
This may require some explanation for people without any pattern recognition background. First, every face is made up of a set of features. Think of a feature as some measurement (like eye color). How are features chosen, or generated? Go take that pattern rec class. We extract all of the features from our faces and dump them into our classifier which is able to determine a likelihood of a match.
<h3>The Solution - Becoming cache-friendly</h3>
The reason this is thrashing cache was pretty straight forward for me. The inner loop is iterating over features. Since each feature computation is relatively expensive, "iterating" over features is awful for cache performance. The solution is a very simple reordering of the loops:
<pre>for feature in feature_list:   
   for face1 in face_list_a:                                    # on the order of 1000
      for face2 in face_list_b:                                 # on the order of 1000                            
         feature_lists[face1][face2][feature] = extract_feature(feature, face1, face2)                                
for face1 in face_list_a:
   for face2 in face_list_b:
      answer[face1][face2] = classify(classifier, feature_lists[face1][face2])</pre>
This means we use the same feature for every input first and once we are done with it, we move on to the next one. This allows each successive comparison between faces to take advantage of the caching done in previous comparisons.

Not surprisingly, the above algorithm improved the performance of the single threaded recognizer by a factor of 6. It also removed the cache bottleneck. With the algorithm no longer cache bound, our speed-up factor equaled our core count. Once we combined all of the optimizations, we ended up with a 25x speed-up of our 8-threaded version on our octo-core machine.
<h3>Dead Abstractions</h3>
When I put the three loops next to each other, it appears like a textbook case of loop reordering. Sometimes, however, reordering loops isn't as easy as you'd like to believe. In this case, these loops were scattered over multiple levels of abstractions.

Do you see which abstraction died? The compare(face1, face2) function.

The loop reordering requires a set of input faces to work properly so that a single compare() function goes back to the slower, cache-inefficient algorithm. It would be natural for a programmer to decide that you need a compare(face1, face2) function. Unfortunately, however, implementing multiple comparisons by making multiple calls to a single compare() function leads to the misuse of cache.

Writing cache-friendly algorithms isn't necessarily easy. Usually, it involves breaking some nice abstractions. This cache-friendliness problem is exacerbated, greatly, in the multi-core generation where cache performance can act as a hidden serializing force. You are doubly punished for misusing cache in this new world. Added to this is the fact that writing cache friendly, highly scalable, concurrent algorithms is a black, black art. For any embarassingly parallel problem, like mine, the solution might be bit messy but it'll work. For more difficult problems, good luck.