---
title: "The parable of the wiki"
date: '2009-04-27'
description:
categories:
tags: []

layout: post

---
Once upon a time, in a cubicle right next to mine, lived a developer. This developer was tasked with building a bare-bones <a href="http://en.wikipedia.org/wiki/Customer_relationship_management">CRM</a> for our company's internal use. This was not an ambitious project. We wanted to be able to put in basic contact information, keep copies of all the pdfs and other various legal agreements, and so on.

This is the type of project that your average web framework lets you hammer out in a day. In fact, I think with <a href="http://guides.rubyonrails.org/getting_started.html">Rails scaffolding</a>, you could have built it inside an hour, and had it polished up and ready to use inside of two days.

If the story ended there, it wouldn't be very exciting, would it?

Once it was built, there was this one tiny feature that would have made it a lot better. And so it was asked, of our developer, if we could find an easy way to let people write little notes about what's happened. Ah, notes, said the dev. That would be easy.

So he decided to make a note database, and let people tack in little notes. Simple text box, add it into the database, no problem. Maybe, he thought, it should show who posted the note? Yes, it should. But we don't really have a proper log in system. It looks like we need one. What about editing or deleting notes? What if someone were to screw up? What happens to the "authored by so-and-so" when someone else edits it? Ugh.

Screw it. This was going to be more work than it was worth. How about we just allow one gigantic text box and let people edit it all they want. That's simple. Ugh, we need to sanitize this input to keep people from screwing up the page. Oh, but, what if someone wants to add a link? They are definitely going to want to add links. We are going to need to add some markdown to this. But, still, what if someone accidentally wipes out the entire text box and saves it? No one wanted to be restoring text boxes from database backups...

After about two days of this game, I heard the words burned into my memory, "God dammit, I just reimplemented a wiki". Except for the colorized diffs, I noted.

Turns out the moment you want a community note repository, all the natural problems associated with it lead you inexorably toward wikidom. It strikes me that there is a larger lesson to be drawn here, as well (ignoring the one about feature creep). Popular solutions to popular problems are popular for a reason. Early on in the process, a full fledged wiki might have been deemed too heavyweight. However, once you start looking deeply, you begin to notice all those devils in all those details, and suddenly you need all those features.