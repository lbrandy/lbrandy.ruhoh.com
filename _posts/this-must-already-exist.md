---
title: "This MUST already exist"
date: '2009-10-12'
description:
categories:
tags: []

layout: post

---
I encounter this feeling frequently. I have a sudden need (or idea) and I realize that such and such a tool or service must already exist. As a software engineer, I've learned to not let that feeling pass. Usually, it's a chance to learn something (because usually it does exist) and sometimes it's a chance to to build something useful and new. 
<h3>The time that my google-fu failed</h3>
In our work, we tend to chain a bunch of command together like this:
<pre>./face_detector input.mpg | ./face_tracker | ./visualize</pre>
This is a great formalism. The problem is that sometimes something goes horribly, horribly wrong. Let's say this time the error occured between step #2 and step #3. This isn't so bad unless, say, step #1 takes a few hours to run and now standard-output has vanished into the never ending ether. And now we've lost the output of step #1 and need to rerun it. This isn't a complicated problem. All I really need is a program that takes what comes in on standard input, writes it to a file, and then pipes it straight back out to standard output. How does this not exist? I had this problem a while ago and searched the internet. Nothing. I wrote a 5 line python script to do it for me.

Six months later I'm wandering around reddit reading some topic about "nifty unix programs that no one knows about" and someone mentions <a href="http://unixhelp.ed.ac.uk/CGI/man-cgi?tee">tee</a>. Well, I'll be. There it is! I guess I don't need my little python script anymore.

Four more months go by, and I finally need tee again. Except now I don't remember what it is called. And I can't find it or the reddit post that contained it!

Two more months go by and I decide to write a post about it. I still can't find the reddit post. I suck at the internet.
<h3>Someone already built it</h3>
This is an actual IM conversation I had recently:
<pre>me: I've had this song stuck in my head for like 5 days....
me: I think it's a christmas song... but I can't remember any of the words
me: no words = no google = pure torture
me: i looked through lists of xmas songs... nothing
me: i even searched for sites that let me hum the song and they tell me the name..
him: there is one, saw it on reddit
him: you can "tap it out" on some webpage
him: and it tells you what it is
me: this is a lie
him: there is a webpage i have no idea how well it works
&lt;tick-tock tick-tock&gt;
me: HOLY
me: <span style="font-size: small;"><a id="buvj21" href="http://www.bored.com/songtapper/s/tappingmain.bin?dotap=1">http://www.bored.com/songtapper/s/tappingmain.bin?dotap=1</a></span>
me: it worked!
me: are you fucking kidding me?</pre>
It was <a href="http://www.youtube.com/watch?v=oIc9Bcw7hTM&amp;feature=video_response">Greensleeves</a>, by the way.
<h3>This MUST exist -- Parallelizing commands on the command line</h3>
One thing that is constantly happening at our office is the need to fire off a whole bunch of really time consuming jobs. Here is an example. Let's say you want to test how the face detector behaves at various resolutions. So, you want to resize a directory full of jpegs to some other resolution. Here's how you might do it:
<pre>$ ls -1 *.jpg | awk -F. '{printf "convert %s.jpg -resize 320x240 %s-sm.jpg\n",$1,$1}'
convert 92.jpg -resize 320x240 92-sm.jpg
convert 93.jpg -resize 320x240 93-sm.jpg
convert 94.jpg -resize 320x240 94-sm.jpg
...
$ !! | sh</pre>
Quick word about what this does: The first command creates the commands and just prints them out. The second line pipes the output (!! means repeat the previous command) into sh. In other words, it executes the previous output as commands.

The problem with this solution is that it is single-threaded. (update: as I write this, I realize a second problem and yet another 'this must already exist moment'. Using awk in this manner is something I tend to do constantly and it seems a bit awkward. Maybe there is a cleaner way to do this?). On most of our machines we have 4 cores, and it would be really nice to have something like this finish 4x as quickly by using all of the cores on my machine. What I want to do is this:

<pre>
$ls *.jpg | awk -F. '{printf "convert %s.jpg -resize 320x240 %s-sm.jpg\n",$1,$1}' 
convert 92.jpg -resize 320x240 92-sm.jpg
convert 93.jpg -resize 320x240 93-sm.jpg
convert 94.jpg -resize 320x240 94-sm.jpg
...
$ !! | gogo -t4 
</pre>

The mythical 'gogo' program would take a list of commands on std-in and do them N at a time (4, in this case). It is apparently <a href="http://www.spinellis.gr/blog/20090304/">a well-kept secret that (gnu's) xargs</a> is capable of this:

<pre>
$ls *.jpg | awk -F. '{printf "%s.jpg -resize 320x240 %s-sm.jpg\n",$1,$1}'
92.jpg -resize 320x240 92-sm.jpg
93.jpg -resize 320x240 93-sm.jpg
94.jpg -resize 320x240 94-sm.jpg
...
$ !! | xargs -0 -n 1 -P 4 convert
</pre>

You'll notice you have to move the command (convert) to the xargs command, and then remember all of the parameters (-0, -n, -P). I find the above command to be extremely awkward to use, in practice, and almost never do it. The problem is that xargs allows you to do so many other things that if you don't use it frequently, it's terribly easy to forget all the parameters you need to do this properly.