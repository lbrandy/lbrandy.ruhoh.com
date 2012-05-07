---
title: "Memory mapped IO for fun and profit"
date: '2010-11-14'
description:
categories:
tags: []

layout: post

---
What I am going to describe below is a fairly straightforward application of memory mapped IO to get huge benefits versus normal IO when loading static, but large, data structures. <a href="https://github.com/lbrandy/blog_examples/blob/master/mmap/zerocopy.c">You can find the code for it here (note: linux only, though it would be an easy windows port).</a> For our face recognition SDK, our model files are large binary files that are full of various bits of (odd-sized) data. We recently flattened everything out and made our initialization, effectively, zero-copy. This is a write-up of that process on a contrived example to make it a bit simpler. If you've ever used mmap to persist a large static data structure, you'll probably find nothing of value here, but for the rest, read on.

For this example, consider a very large list of strings (and their lengths) that we need to persist to disk. Or, a very large array of these:
<pre>
typedef struct {
  char *data;
  int len;
} data_t;
</pre>

To make the problem non-trivial, we will consider the case of different length strings (in my tests I was using a million strings around 150 bytes in length -- plus or minus a few to keep them from all being the same size).
<h3>Let's get started</h3>
Here is a naive read/write for this data structure:

<pre>
void naive_write(char* filename, data_t* data, int n)
{
  FILE *f;
  int i;
  f = fopen (filename, "wb" );
  fwrite(&amp;n, sizeof(n), 1, f);
  for (i=0;i&lt;n;i++)
  {
    fwrite(&amp;data[i].len, sizeof(data[i].len), 1, f);
    fwrite(data[i].data, sizeof(char), data[i].len, f);
  }
  fclose(f);
}

data_t* naive_read(char* filename)
{
  data_t* answer;
  FILE *f;
  int i, n;
  f = fopen (filename, "rb");
  fread(&amp;n, sizeof(n), 1, f);
  answer = malloc(n * sizeof(data_t));
  for (i=0;i&lt;n;i++)
  {
    fread(&amp;answer[i].len, sizeof(answer[i].len), 1, f);
    answer[i].data = malloc(sizeof(char) * answer[i].len);
    fread(answer[i].data, sizeof(char), answer[i].len, f);
  }
  return answer;
}
</pre>

We first write the number of strings, and then for each string we write its length followed by the string data. When reading, we read the number of strings (and malloc the array of strings) and then for each string we read its length (to malloc the string data itself) and then read the string. This implementation does many mallocs() and it does many freads(). It is, consequently, fairly slow.

With this data format on disk, though, this would be difficult to (easily) optimize much more. So, let's change the layout.
<h4>A better file format</h4>

<pre>
void flat_write(char* filename, data_t* data, int n)
{
  FILE *f;
  int i;
  f = fopen (filename, "wb" );
  fwrite(&amp;n, sizeof(n), 1, f);
  for (i=0;i&lt;n;i++)
    fwrite(&amp;data[i].len, sizeof(data[i].len), 1, f);

  for (i=0;i&lt;n;i++)
    fwrite(data[i].data, sizeof(char), data[i].len, f);

  fclose(f);
}
</pre>

We made a very minor change to how we write the data structure to disk. This time, we put all of the lengths up front, and then all of the strings after that. This is going to allow us two rather large simplifications: 1) we can malloc() once for all of the data strings, 2) we can read them all with a single fread(). This is a pretty big change because it effectively removes all malloc() pressure and puts everything into fread(). The read function does, though, become slightly more complicated:

<pre>
data_t* onecopy_read(char* filename)
{
  data_t* answer;
  FILE *f;
  int i, n, total;
  
  f = fopen (filename, "rb");
  fread(&amp;n, sizeof(n), 1, f);
  answer = malloc(n * sizeof(data_t));

  total = 0;
  for (i=0;i&lt;n;i++)
  {
    fread(&amp;answer[i].len, sizeof(answer[i].len), 1, f);
    total += answer[i].len;
  }

  answer[0].data = malloc(sizeof(char)*total);
  fread(answer[0].data, sizeof(char), total, f);  /* one giant fread */

   /* set all the ptrs */
  total=0;
  for (i=0;i&lt;n;i++)
  {
    answer[i].data = answer[0].data + sizeof(char)*total;     
    total += answer[i].len;
  }
  
  return answer;
}
</pre>

This is a decent optimization but not ideal. fread, still, involves a copy (copying from disk into our program's address space). The only way around this problem is to not use fread.

<h4>Towards zero-copy</h4>
Using the exact same file, we can open it using mmap() (windows users see: <a href="http://msdn.microsoft.com/en-us/library/aa366761%28VS.85%29.aspx">MappedViewOfFile</a>). This maps the file directly into our address space without having to do any copying whatsoever. We can then just setup all the data pointers to point to the memory mapped file, and we've initialized our data structure with zero copies.

<pre>
data_t* zerocopy_read(char* filename)
{
  data_t* answer;
  int f;
  int i, n, total;
  char *data_ptr;
  int* hdr_ptr;
  struct stat sb;
  
  f = open (filename, O_RDONLY);
  fstat(f, &amp;sb);
  hdr_ptr = mmap(0, sb.st_size, PROT_READ, MAP_PRIVATE, f, 0);

  n = *hdr_ptr++;
  answer = malloc(n*sizeof(data_t));
  
  for (i=0;i&lt;n;i++)
    answer[i].len = *hdr_ptr++;

  data_ptr = (char*) hdr_ptr;

  total=0;
  for (i=0;i&lt;n;i++)
  {
    answer[i].data = data_ptr + sizeof(char)*total;
    total += answer[i].len;
  }
  
  return answer;
}
</pre>

<h4>Timings</h4>
So the moral of the story, then, is how much faster are the various versions. Here's some timings:

<pre>
(for num_strings=1,000,000 and str_len= ~150 bytes)
naive_read time: 0.373289
1copy_read time: 0.202408
0copy_read time: 0.011233
</pre>

It's important to understand what we are actually measuring here. I ran this test on Linux (Windows isn't much different) which has a file cache. The actual disk wasn't ever really involved in this program or these timings. We are really testing the summed speed of our processing, malloc() (in the first case), fread(), and the kernel's handling of cached files. (note: if you modified this program to only read the files, and then reboot your machine to clear the file-cache, the first run would be much slower as the file was read in from disk and cached).

<h3>Benefits</h3>

Having these large static data structures persist using memory mapped files has some rather significant advantages beyond just initializing extremely fast. We've shifted the entire burden of managing this memory onto the operating system. If multiple processes are being run, this memory will be shared amongst them. This is not true of the fread() solution. The OS's file cache will effectively keep the file in memory and ready to go whenever it's been recently run. If there are portions of your data you aren't using (in face recognition imagine a scenario where you only do face detection), the rest will never get loaded (or will eventually be swapped out). And last, but not least, the flattening process puts all of the bits contiguous in memory (compare with the naive approach), allowing for the OS to handle the pages of data much more efficiently.