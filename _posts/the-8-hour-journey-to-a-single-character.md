---
title: "The 8 hour journey to a single character"
date: '2009-11-23'
description:
categories:
tags: []

layout: post

---
I came into work on day not too long and was met with an unfortunate piece of information. The test we ran the previous night reported a 4% drop in accuracy (we found 4% fewer faces). I frowned. <strong>I had clearly screwed something up.</strong>

You see, the day before, I found that our code was doing some really pathological and unnecessary color conversions on images. We were using our video i/o library (a very thin wrapper on <a href="http://ffmpeg.org/">ffmpeg</a>) to read in movies and allowing it to convert the frames into RGB. As soon as our code got ahold of these RGB frames, we immediately converted them to grayscale. The pathology of the situation is that the vast majority of all video formats are already in the <a href="http://en.wikipedia.org/wiki/YUV">YUV color space</a> (or <a href="http://en.wikipedia.org/wiki/YCbCr">YCbCr color space</a>. I will use the terms interchangably, but you should know they aren't quite the same thing). For those among you that aren't image processing nerds, the Y-channel of YUV is functionally equivalent to a gray channel. In other words, videos are almost always encoded with a gray channel and 2 color (chrominance) channels. That means converting these images to RGB just to convert them back to gray is beyond wasteful.

We had actually known about this problem for awhile but it's never been a terribly pressing issue. That changed recently when we were doing some really high speed processing and we noticed our color conversions were a non-trivial portion of the time. I dug into our video i/o library, removed the conversion to RGB, and piped the Y channel of the YUV frames into our software. Everything appeared to be working perfectly. Output looks good. No memory leaks. Commit. Go home. Watch House.
<h3>The next day...</h3>
So I walk in, bright and early, and hear the disappointing news. We lost 4% accuracy. Did my colorspace change cause this? I hope not. Within a half an hour, I realized that my colorspace conversion change clearly was not correct. The frames that I had tested on the previous day looked identical, but they weren't. I expected some minor round off error as a possibility, but the changes were more than I anticipated.

The error became extremely obvious when I ran the new decoding library on the opening of Star Trek. Conveniently, the opening of Star Trek is pitch black. My "new" library was not producing black! It was near-black, but very clearly NOT black. Uh oh. What's going on?
<h3>Let's look at the numbers</h3>
I dug into ffmpeg and very quickly reproduced the problem. The very first pixel of the very first frame of this episode of Star Trek had a Y value of 16. Not zero. When ffmpeg converted this value to RGB, the result came out to be (0,0,0). Black. Wait a minute, since when is Y=16 equal to black? What is going on?

I looked at the only other place in our codebase where we deal with this type of information: JPEG decoding. JPEG's also use YUV formatting. What would this particular frame look like in a JPEG's YUV? This is a quick test. Is it also 16? Nope, it's zero.

For an RGB value of (0,0,0), ffmpeg is telling me the Y value is 16, and the jpeg library is telling me the value is 0. Either there is an egregious bug in one of the two most well-tested libraries on the planet, or I clearly don't understand wtf is going on. I'm going to assume the latter. But that will have wait until after lunch.
<h3>Research time</h3>
When I got back from lunch, it was time to hit up the internet. If you search the internet for formulas to convert yuv to rgb you'll get all sorts of conflicting information. You'll even get very different formulas. If you read the YUV or YCbCr Wikipedia pages, you can easily miss the most important information (hint: it's not the equations). After spending a tremendous amount of time reading (and being confused about the different formulas), I made the critical discovery. <strong>There are different definitions of YUV.</strong>

I then had to dig into the details to find out just how deep this particular rabbit hole goes. In the end, it wasn't terribly complicated (but it was difficult to find good information). In essence, though, different standards define different dynamic ranges for the YUV color space when digitized into 8-bit per sample. Movie files (e.g, MPEG) will often use 16-235 for the Y channel (black-&gt;white), while images (JPEG) will use 0-255. A movie file's white (235) != a jpeg file's white (255). To make matters worse, the Cr and Cb (ie, U and V) channels use an entirely different set of dynamic ranges for MPEG files (though jpeg is always (0-255)). Oh my.

Note: if you are here because you are having similar yuv/rgb problems and google led you here, I strongly suggest you read every single word of these three links:
<ul>
	<li><a href="http://en.wikipedia.org/wiki/YUV">Wikipedia: YUV</a></li>
	<li><a href="http://en.wikipedia.org/wiki/YCbCr">Wikipedia: YCbCr</a></li>
	<li><a href="http://www.fourcc.org/fccyvrgb.php">fourcc.org: yuv to rgb</a></li>
</ul>
<h3>The Fix, part 1</h3>
If all I need to do is rescale to a different dynamic range, that is not a difficult problem to solve. It's a fair bit tricky (watch those unsigned overflows!) but it's nothing that can't be accomplished through the power of C. I spent an hour or so writing a function to convert the three channels to the expanded dynamic range (remembering that the Y channel uses a different range than the U and V channels). I knew I'd lose some information, but what choice did I have?

Once I had finished, I ran all my previous tests and found the output to be far, far better than the one I was using from the previous day. I also tested my new conversion routine on images that failed from the overnight test and what do you know, they were now finding faces. Mission accomplished!
<h3>Not so fast my friend</h3>
It was about this time that I felt the need to vent. Seriously, movie and jpeg people, why are you doing this to me? Why are there two (note: actually more than two) different dynamic ranges for 8-bit YUV pixels? Why oh why? (more notes: if you want to learn why, it's actually a fairly fun and interesting story... taketh thee to wikipedia).

In the need for some complaining, I decided to go onto IRC and complain to <a href="http://x264dev.multimedia.cx/">the only video developer I know</a> (he works on x264 -- the open source h264 encoder). I asked him why "they all" go around screwing with people like me with such nonsense. He laughed and went on to explain there are actually more than two different formats and commiserated with me for a moment. And then he said something important. He said only "<code>--fullrange</code>". Wait. What is <code>--fullrange</code>? <a href="http://www.linuxcertif.com/man/1/x264/">Is that an x264 parameter?</a> Yes, yes it is. What does <code>--fullrange</code> do? It uses the fullrange of YUV. Ah! x264 devs are genius. Why would they leave this silly conversion to us?

Oh wait. Does that mean... does ffmpeg... do it too? It has to, right? Let's <a href="http://cekirdek.pardus.org.tr/~ismail/ffmpeg-docs/ffmpeg-r_2libavutil_2avutil_8h.html#60883d4958a60b91661e97027a85072a">check the docs</a>, shall we. There sure are alot of formats on this list. I wonder if any of them are "full-range" YUV.
<blockquote><code>PIX_FMT_YUVJ420P 	 Planar YUV 4:2:0, 12bpp, full scale (jpeg).
PIX_FMT_YUVJ422P 	 Planar YUV 4:2:2, 16bpp, full scale (jpeg).
PIX_FMT_YUVJ444P 	 Planar YUV 4:4:4, 24bpp, full scale (jpeg).
</code></blockquote>
Does that "jpeg" mean these are "jpeg-style" full-range YUV outputs? I should try this. Within minutes I realized that yes, these formats outputted YUV channels that used the full dynamic range 0-255. Excellent. I reverted all my ugly changes with my own customized range expansion code and committed this final fix.
<pre>-         PIX_FMT_YUV420P,
+         PIX_FMT_YUVJ420P,</pre>
One character. One friggin' "J". 8 hours. I hope no one is keeping track of "lines of code per hour".