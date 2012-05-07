---
title: "Are you in the text editor dark ages?"
date: '2009-04-06'
description:
categories:
tags: []

layout: post

---
No, this post isn't about how your text editor stinks and mine is awesome. You are probably using a perfectly awesome grown-up text editor. I think a frightening large percentage of us, however, are leaving the full power of our editor on the table, and making due with the kid gloves version.

I present to you, right now, the feature that separates the men from the boys. If your text editor doesn't support this feature, it is a stone age editor. If you text editor does, and you don't use it, you are in the dark ages. That feature is tags. Emacs, vim, and TextMate all support tags. Visual Studio and Eclipse, being full fledged IDEs, have even more powerful versions.
<h2>Tags, tags, tags</h2>
What are tags? Tags are a way of navigating files based on a parsing of your source files. Simply put, it's a way to jump around your codebase. What does this function do? Jump to its header. Jump to its body. Where else is it called? Cycle through all the uses of this function.

Tags are one of those features that many text editor journeyman know about but don't setup because of the mild pain associated with setup. It amazes me how many people have heard of tags but don't use them because of the start-up friction. Seriously, take the next 15 minutes, read this, and then go set them up. I promise you it will change your life. Ok, that might be a stretch. It'll make your morning, though. The first 15 minutes of using tags is a glorious 15 minutes.

Let me share that glory with you, right now.

<a href="http://www.vmunix.com/vim/tags.html">vi users go here.</a>

TextMate users can <a href="http://www.cocoabits.com/TmCodeBrowser/">check this out</a>.

(note: I don't use either of those editors, so I didn't really vet those links. If those links don't work or are otherwise crappy, either use google or use a better text editor. Ha ha.)

Emacs users, come with me.
<h2>Setting up tags in Emacs</h2>
This will require some reasonable knowledge of the unix/linux command-line, including editing your Emacs configuration file (you do have one of those, right?). You will also need etags installed (it often comes pre-installed, so you may already have it).

**Step 1.** Let's get a codebase we can play with...
<pre>svn checkout -r 18337 svn://svn.ffmpeg.org/ffmpeg/trunk ffmpeg
cd ffmpeg</pre>
**Step 2.** Now that we have a codebase, let's generate tags for it.
<pre>mkdir ~/.tags/
find . -name "*.[ch]" | xargs etags -o ~/.tags/TAGS</pre>
Now, what I've done here is created a hidden directory called ".tags" in my home directory, and generated a TAGS file for my codebase in that. Obviously, this is a C codebase so a different language codebase would need an appropriate find command. If you have or want multiple different etags lines you need to use the -a option to append. For example:
<pre>find . -name "*.h" | xargs etags -o ~/.tags/TAGS
find . -name "*.c" | xargs etags -a -o ~/.tags/TAGS</pre>
If you generate tags like this, you'll need to manually update them whenever you've added large sections of the code you want re-parsed. Using a single tags directory and having to manually update your TAGS file from time to time is less than ideal but fine for beginning usage. You can get more advanced as you get more comfortable.

**Step 2. Tell emacs where to find our TAGS file**

Now that we have a codebase, let's generate tags for it.The last step is to tell Emacs where we keep our TAGS files. This can be done by setting a variable (preferably in your custom loaded .el file) like so:
<pre>     (setq tags-table-list
           '("~/.tags"))</pre>
If you don't do this last step, you'll need to manually tell Emacs where it can find your TAGS file on each load. If you try to use tags commands in Emacs, and it asks where the TAGS file is, this above step was screwed up.
<h2>Behold</h2>
So since you are following along at home, we can now open emacs (and hopefully autoload our .el file with our variable correctly set). Let's edit ffmpeg.c. It's in the base directory. Search for "main(", and that will get you to the fairly short and elegant ffmpeg main function.

The first function that gets called is the magical avcodec_register_all(). Place your cursor over avcodec_register_all() and hit M-. (usually alt-.). If you've done everything correctly, hitting M-. with your cursor over avcodec_register_all() you will jump to the allformats.c file and the top of the avcodec_register_all() function.

You can also use the alternate version. Move your cursor off of a symbol (whitespace will work) and hit M-. another time. This time emacs will ask you type in a tag. Type in AVCodec and watch as you jump to avcodec.h at the declaration of the AVCodec struct.

It should be noted that you have not (nor need not) compile anything for this to work. For a complete list of navigation-by-tags commands, see <a href="http://www.gnu.org/software/emacs/manual/html_node/emacs/Tags.html#Tags">the Emacs manual</a>.