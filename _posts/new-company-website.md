---
title: "New Company Website"
date: '2009-03-09'
description:
categories:
tags: []

layout: post

---
No article this week. I spent the last two weeks working with everyone else to relaunch our company's website. I'm sick of writing. The good news for you, though, is there tons of material to be read about face detection, face tracking, and face recognition:

<a href="http://www.pittpatt.com">Pittsburgh Pattern Recognition</a>

The highlight of the page, though, is probably our <a href="http://webdemo.pittpatt.com/recognition_demo/">online face recognition demo</a>. You give it two images, it will try to match the faces between the two. I'll probably write a bit more in the coming weeks about various topics related to face recognition, the new site, and the new demos. Before I go, however, I have two comments to make.

**The web is such a hack.** After doing my first good spell of web programming in a while, I cannot shake the feeling that the entire web infrastructure is a complete hack job. HTML is a "language" that kind of describes the data of the webpage, and half of its layout. CSS is a second "language" that describes the other half of the layout, and the style. Javascript is a third language for the client. PHP (or Python or Ruby) is a fourth language for the server. And then there's SQL. And none of that includes a templating language (we used Python and Textile). There has to be a better way.

**Javascript bug.** Our front page (www.pittpatt.com) crawls to an absolute halt because of the javascript animation. It only happens on Firefox, in Linux, using the propiertary nVidia drivers. I haven't had much of a chance to research this bug but it seemed like a small enough bug to go live knowing about it. I'm going to spend some time this afternoon seeing if there is a workaround. I figured I'd mention it here to see if anyone knew more.