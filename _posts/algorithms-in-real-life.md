---
title: "Algorithms In Real Life "
date: '2008-10-20'
description:
categories:
tags: []

layout: post

---
Sometimes I notice computer science or other assorted math nerdery in real life. These are their stories.
<h3>Alphabetizing Papers</h3>
Have you ever seen a teacher alphabetizing a couple dozen papers? This is basically a sorting problem, right? And you are a computer scientist, so sorting problems should be interesting to you. Have you ever analyzed how people alphabetize papers? How does she (for the sake of brevity I've made the sexist assumption that this teacher is female) do it? Almost always, she puts all the 'A' names in this pile, 'B' names in that one, and so on. The group ranges my vary (maybe A through C in this pile, etc.), but the algorithm is almost always the same. Once she's done with that, what does she do? She tends to go letter by letter and use some other algorithm on each group. In my experience, she uses an <a href="http://en.wikipedia.org/wiki/Insertion_sort">insertion sort</a>.

Did it ever strike you as odd that human beings used such an algorithm? Did you ever, as a young, naive, computer programmer, snicker to yourself thinking that she was using an inferior algorithm? I did. Everyone knows that <a href="http://en.wikipedia.org/wiki/Quicksort">quicksort</a> is the best and fastest way to sort, right? Why don't teachers use quicksort? My original answer to this question was that unlike computers, the human brain doesn't do all comparisons equally. It's just "easier" for our brains this way. Splitting into letter groups makes each smaller problem more manageable.  I was certain, in those times, there might exist some faster algorithm that teachers could use based on a quicksort. I was wrong.

Back to the computer science part: do you know the name of the sorting algorithm that these teachers use? It's called a <a href="http://en.wikipedia.org/wiki/Bucket_sort">bucket sort</a>. A bucket sort followed by individual insertion sorts (exactly what teachers tend to do) is a linear time sorting algorithm. Yes, linear time. Did you know there are linear time sorting algorithms? But you thought n*log(n) was the best possible sorting algorithm? That's only the bound for comparison based sorting. When you have some notion of the distribution of the items to be sorted, you can break through that boundary and do linear time sorting. The catch with linear time sorting is that the input must follow some known distribution. This, by the way, is why teachers instinctively break the piles into various types of groupings. If there are alot of papers, you need finer group ranges. Furthermore, the ideal bucket setup would distribute the papers roughly evenly. The letter S might need its own bucket, but you can put all the letters up through F in their own bucket. Teachers have alot of experience with both the general problem and their specific problem (for example, the peculiarities of a particular class' name distribution) and so they are optimizing the algorithm given the known distribution. They are setting up the parameters of the linear time sort (number of buckets, bucket ranges, etc.) exactly as they should to optimize the sort time.

The main downside to these linear sort algorithms is that they require alot of extra space (versus comparison-based sorting). You tend need to need an auxiliary bookkeeping array on the order of the original problem to do them. This isn't a problem in real life! She just needs a larger table. In a very real sense, this supposedly "naive" algorithm that teachers use is among the very best possible. And woe to any computer science student who thinks to himself that she's doing it wrong.
<h3>The Coffee Problem</h3>
So I woke up the other day, took my shower, got dressed and got on the elevator. My apartment complex has complimentary coffee in the lobby area (that's why the rent is so high). This particular morning, when I got there, I noticed all of the little tags that tell me which dispenser was which were missing. So there I stood, with five identical coffee dispensers, virtually certain at least one of them was decaf. I don't want decaf. What do I do?

If I was <a href="http://www.youtube.com/watch?v=_sarYH0z948">David Carruso</a> or that dude from CSI: Las Vegas, I could have smelled the coffee, detected the bean's nation of origin and deduced which was decaf based on the trade distribution of that country's beans throughout the continental United States. Or maybe I could have used some nearby chemical MacGuyver style to determine which was caffeine. I'm just a dude needing caffeine, so I thought for a second, and then went for the middle one. How did they likely set these up? It seemed logical to me that since there were five, no more than two would be decaf. That seems like a good assumption. Furthermore, my "opponent", being a rational person, likely put the decafs together, and on one end. That means the middle one is probably caffenieted.

(Another good answer I received from someone else is just to mix them all up. At worst you get 60% caffeine.)