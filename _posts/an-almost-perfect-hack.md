---
title: "An almost perfect real-world hack"
date: '2009-08-03'
description:
categories:
tags: []

layout: post

---
Almost immediately after we bought our house I received a letter in the mail. The local school district was appealing the tax assessment of my house. The issue in question was the value of my property in 2002 (don't ask, it's a long story, and a silly law). My property tax is some percentage of the 2002 value of my home, and they thought my assessed value was too low. Great.
<h3>Researching...</h3>
We bought our house in 2009 for almost $15,000 less than the previous owners paid for it in 2004. I was amazed that the school district thought our taxes should go <em>up</em> despite the fact that the house's price had gone <em>down</em>. This was my first piece of evidence, but I needed to understand more about these tax hearings.

Turns out that most people don't show up to their assessment. The school districts use your sale price in 2009, multiply it by some magical number (say 90%) and they argue that is what your house should be assessed at. This strikes me (and many others) as a ridiculous method of determining the value of the house. Since few people show up, they tend to win and people's assessments tend to go up.

In order to counter argue, you need to establish what your house was worth in 2002 based on comparable sales that occurred in and around 2002. I decided to do some research. Lucky for me, <a href="http://www2.county.allegheny.pa.us/RealEstate/Search.aspx">my county has a website</a> that lets you look up the history of each house (including when it was sold, and its measurements like sq.footage, number of beds and baths, etc.).
<h3>The Allegheny Assessment Website</h3>
So <a href="http://www2.county.allegheny.pa.us/RealEstate/Search.aspx">this website</a> lets you look up details for each house by address. I tried looking at the history of each house in my neighborhood trying to find, in vain, houses that matched mine and that was sold in 2001 or 2002. Actually finding comparables with this website was going to be quite a tedious adventure.

It's important to note that it's only by address (or by parcel number). You can't do things like "show me all the houses that sold in 2002". That would be too convenient, of course. I wonder how many tax assessment appeals the county and the school districts have won precisely because the website was so difficult to search.

After about 10 minutes of wandering around aimlessly through nearby neighborhoods, I got an idea. This is why God invented computers. <strong>Let's build a web scraper.</strong>
<h3>Scraping the detail pages</h3>
The very first thing I noticed was that if you knew the parcel number of a property, you could look up the property with a simple GET request. <a href="http://www2.county.allegheny.pa.us/RealEstate/GeneralInfo.aspx?ParcelID=0008J00030000000%20%20%20%20&amp;SearchType=2&amp;SearchStreet=Art%20Roone&amp;SearchNum=&amp;SearchMuni=">Here is an example page (this is Heinz Field, home of the Pittsburgh Steelers)</a>.

Ten minutes later, I had some scripts in python to download all the necessary pages, given a parcel number, and extract all the vitals: address, square footage, sales dates, sales prices, number of bathrooms &amp; bedrooms, lot size, and so on. The script then dumped that information into a database.

So far so good, now I just needed to get all the parcel numbers for my area.
<h3>Getting the parcel number list information</h3>
I needed to find the parcel id for every single house in my town.

Their search box wouldn't let me search for '\*'. Searching for 'A' in the street address, however, gets you a paginated list of every house in that town on a street that began with the letter 'A'. These searches were all conducted with a POST to a single url. All I had to do was figure out to form these POSTs and how to turn the page. This is where I hit a speed bump.

The "next page" button on the results page was a javascript call that formed a new POST. Their POSTs had some "features" (I believe from some windows web development tool -- __VIEWSTATE, __EVENTVALIDATION were the arguments in the POST) that made crawling it non-trivial. The POST required some magical numbers that were formed in javascript.

It probably wouldn't have been too difficult to grep out the magic numbers and emulate the javascript code in python to formulate a properly formed POST to get the data I needed. I had a quicker solution.
<h3>iMacros</h3>
<a href="https://addons.mozilla.org/en-US/firefox/addon/3863">iMacros is a nifty firefox plugin</a> that I've used from time to time that turns your browser into a scraper. It's a heck of a lot slower than doing it from python, but you can "scrape" a page as if you were the user. This works brilliantly for very simple stateful tasks that require things like cookies or javascript. In iMacros, I could tell it to record all the parcel numbers on a particular page and then click "next", and repeat.

I was only about a half hour into my adventure and I already had the necessary scripts to scrape their site. Not bad. I let iMacros run for an hour, getting the parcel numbers of every property. One more hour later I had run my python scripts with the parcel number list and had a database filled with every single house in my town.

I had just ran about 2 hours of constant web requests on a county server to build a database of about 5000 homes. And now I just posted this information on the internet. I hope I don't get arrested.
<h3>Comparables, Comparables</h3>
Once I had my database, it was time to search. One SQL statement later I had found every house that had as much square footage, as much lot size, as many bedrooms, as many bathrooms, that was sold in 2000-2002 for less than my current tax assessment. 84 results. Ha ha.

That's probably too many, huh? My town is shaped funny, and so some of these houses on this list were actually quite far away. Luckily for me, the parcel numbering is fairly sane. I was quickly able to figure out which parcels were near me based on the first portion of the number. I removed anything that was too far away.

I ended up with 31 residential homes that were within 4 miles of my house that were sold in 2000-2002 that had all better measurements and sold for less than my assessment. I began printing. Every one of these houses was better than my house (on paper, at least), very close by, and sold for less than my assessment. I was going to walk into court and argue that my assessment was too high.

I picked the 7 best to state my case, and printed up detailed reports on each of those as well. I'd open with these 7, make my case that my assessment was too high. I'd say we bought our house for less than the previous owners, more proof it was too high. And if I needed it, I'd bust out the list of 31.
<h3>Court</h3>
I spent most of the night before rehearsing my speech for court. I wasn't rehearsing the part about how they should lower my tax assessment. I was rehearsing the part where I explained how I got such detailed comparables, how it was totally legal, and how they shouldn't throw me in jail for "hacking".

I walked into the courtroom with about 100 pages of documentation in a nifty leather notebook. 31 comparables and 7 of those in detail. I had absolutely no idea what they would do. I imagine lawyers or real estate agents have access to databases like this, so they'd probably just assume I knew someone. There was the outside chance that no one had ever done anything like this before.

In the room sat two lawyers (my opponents) and the guy in charge (I presume he was a judge). It wasn't in a court room but an office adjacent to the court room. This is basically what happened:

<blockquote>**Judge:** What's your name?

**Me: **Louis Brandy.

<em>The judge and opponent lawyers shuffled a lot of papers around. The two lawyers looked at the their papers for awhile. </em>

**Judge, to lawyers: **Alright, what are we doing?

**Lawyer:** This appeal was been going on for 2 years, with the previous owners. They (me+my wife) are the new owners. They bought it for $15,000 less than the previous owners. That puts their house into agreement with our numbers. There's no need to change this assessment. We will withdraw the appeal.

**Judge, to me**: You can go forward, if you want, and I'll decide what to do with the assessment -- up or down. They are willing to withdraw the appeal, is that ok with you?</blockquote>

Ah, crap. I had a decision to make. Should I push forward and risk being embarrassed? What if I printed up the wrong numbers? What if my comparables were garbage? What if they had equal comparables to keep my price at the same level? Accepting the the draw was the obvious choice. My only hesitation was that it would ruin my story.

I thought briefly but there wasn't really a choice. I said yes, their withdrawal was fine by me. I signed the papers and walked out of my hearing.

It took all of five minutes and I said exactly three words. I showed no one the 100 pages of awesomeness in my little notebook. Such a good story was going to be wasted on such an anticlimax. C'est la vie.