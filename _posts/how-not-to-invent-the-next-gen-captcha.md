---
title: "How NOT to invent the next-gen CAPTCHA"
date: '2009-10-20'
description:
categories:
tags: []

layout: post

---
This is a post I've been kicking around for awhile and I've finally felt compelled to finish it. It seems to be a popular geeky topic for idle conversation and blog posts of all variety to come up with new and exciting ways to replace CAPTCHAs. I've had one too many IM conversations about "new captcha" ideas. <a href="http://news.ycombinator.com/item?id=883480">This week, someone's "next-gen" CAPTCHA idea was posted on Hacker News and promptly "broken" within hours</a>. I don't think it's necessarily a bad thing, by the way, to post your CAPTCHA idea online and have it get destroyed. The only way to succeed on something like this is to fail. Often.

In truth, almost all of the ideas floated on the internets (and for some reason they always seem to revolve around human understanding of images) are fundamentally flawed in at least one respect the author didn't fully consider. So while I do not have my own next-gen idea, I have thought quite a bit about the requirements it should meet, and consequently I've seen how few other ideas actually meet those requirements.
<h3>Questions you need to answer about your CAPTCHA idea</h3>
1. **Is it trivial for a human to answer correctly? <span style="font-weight: normal;">This might seem obvious, but in the process of optimizing your captcha idea for every other factor, this is often the one that suffers. If it is at all difficult to "do" your captcha, it will be <a href="http://www.google.com/search?q=hard+captcha">universally reviled</a>.</span>**

2. **Can humans do it quickly? <span style="font-weight: normal;">This, again, speaks to usability. Humans want to be in and out extremely quickly. Every second a person takes doing the CAPTCHA translates into lost users, sign-ups, etc.</span>**

3. **How is the random guess-rate?** It better be abysmal.

4. **How well do you know the "opposing" technology? **If you don't know the state-of-the-art in the "enemy" technology, you really shouldn't be making claims about your CAPTCHA's utility. For example, the opposite technology for conventional captchas is <a href="http://en.wikipedia.org/wiki/Optical_character_recognition">OCR</a>. You don't need be an "expert" in said field, but you do need to understand its current state.

5. **How is the guess rate of a sophisticated attacker?** Once you've factored in an attacker who is versed in the opposing technology, he still needs to be reasonably far away from getting through (less than 1% is a good upper bound)

6. **How much human input is required to create your captcha?** You absolutely positively must fulfill one of these requirements: 1) the attacker needs exponentially more human effort than the creator or 2) the creator has exponentially more humans. The first case involves doing some (non-reversible) automatic processing of the data to create many permutations from a single human input. In the second case, think reCAPTCHA, which uses the actual participants to help create new captchas.

7. **What are the cultural and accessibility issues?** Does your CAPTCHA require too much cultural knowledge? What about users with bad sight or hearing? This isn't necessarily a deal breaker, but it is something to consider.

Normal CAPTCHAs score remarkably well on this particular test. Humans can usually do it trivially and quickly. The random guess rate is beyond awful. There is absolutely no human input required to generate new CAPTCHAs.  The only downside of CAPTCHAs today is that OCR is slowly improving the guessrate on "easy" CAPTCHAs and "hard" ones become <a href="http://farm4.static.flickr.com/3237/2443601665_214fdcc466.jpg">too difficult for humans</a>. Programmers tend to focus on solving only this last problem, ignoring all the other things that make CAPTCHAs so extremely attractive.
<h3>It's never as simple as it appears</h3>
**Let's walk through an actual idea.** I first heard this from a friend (but seen repeated elsewhere). Take a bunch of images and have the human rotate them so they are "upright". That seems like a good start. How close (in degrees) does the answer need to be correct? Let's say 30, to be safe. Now our random guess rate for a single image is 1/12 which is far, far too low. The only way to remedy this situation is to add more images. Three is probably the absolute minimum. How much can a computer-vision/image-processing expert do to narrow the guess-rate? More than you'd probably think. Time to add more images. This might already result in a CAPTCHA that takes too long and is too annoying for humans.

For this particular idea (which is already in a bit of trouble) there's another even more difficult problem lurking. How do we get and select images for our system? We have two choices:
<ol>
	<li>Have a human filter images and create many artificial variants</li>
	<li> Use some "automatic" method for gathering them: download them from the internet at large and assume that every internet image is "upright". This will obviously fail sometimes but hopefully it will be extremely rare.</li>
</ol>
Option 1 has a major inherent problem. If you can sit down and label 1000 images, so can the attacker. You must assume, then, that the attacker will eventually get a full library of the base images you are using. His primary goal is to figure out which of the base library images is most likely for each input image. This means you are going to need to artifically "distort" images in such a way that the attacker cannot reverse engineer it while still preserving the human's ability to recognize and orient them. This is much more difficult than you might first suspect.

Option 2 has an altogether different set of problems. The first question you must ask is what percentage of internet images are orientable by humans to the precision necessary? From there, what percentage of your CAPTCHAs will consequently be impossible? Remember, you only need one impossible image for the entire CAPTCHA to be impossible, and so as you add more images to the query, the chance of the CAPTCHA becoming impossible skyrockets. You must deal with this "bad" data while maintaining an extremely low frustration quotient.
<h4>A word on "image-based" captchas</h4>
If you don't know much about image processing or computer vision, you probably shouldn't be devising image-based CAPTCHAs. I am by no means an expert on either but your average computer vision 101 course will teach you enough to defeat half the ad-hoc CAPTCHA ideas you see proposed around the internet. There are, of course, ways that human understanding of images can be exploited but to understand what they are, you really need to know what is and isn't possible.

The example submitted to Hacker News last week was an example where the CAPTCHA consists of a set of images broken into strips and the user is required to reassemble a single image. This (and virtually all variants of this) is an absolutely trivial problem for a computer solve. Within hours, someone had posted a working solution. Since the strips were of constant size, the "attacker" in this case simply compared the two adjacent lines of pixels of the two strips to determine which pair of images were most likely the same. The designer could have easily randomized the border between the two images to defeat this naive attack, but he would almost certainly have lost the war. Figuring out if image segments are from the same image (especially if they should be adjacent) is not a difficult problem.