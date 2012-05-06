# A really dirty script to convert wordpress -> ruhoh.
#
# I'm writing this to convert my blog over. It might be useful for you. Feel free
# to steal, appropriate, misappropriate or copy any code or ideas that you find herein.
#
# author: lbrandy


# figure out where we are
import os

basepath = "./"
if os.path.isdir("_posts"):
    pass
elif os.path.isdir("../_posts"):
    basepath = "../"
else:
    print "I can't find _posts :("
    exit(1)
    

hdr = """---
title: "%s"
date: '%s'
description:
categories:
tags: []

layout: post
%s
---
"""

def is_draft(p):
    if p["post_status"] == "draft":
        return True
    elif p["post_status"] == "publish":
        return False
    else:
        raise "ruhoh"
    
def header(p):
    if is_draft(p):
        t = "type: draft"
    else:
        t = ""
        
    date = p["post_date"]
    title = p["post_title"].replace('"', '\\"')
    return hdr % (title, 
                  date.strftime("%Y-%m-%d"), 
                  t)


def write_post(p):
    write(p, basepath+"_posts/")

def write_page(p):
    write(p, basepath+"_pages/")
     
draftcounter = 1  
def write(p, dirname):
    if is_draft(p):
        global draftcounter
        filename = "untitled-%d.md" % draftcounter
        draftcounter+=1
    else:
        filename = "%s.md" % p["post_name"]

    
    f=open(dirname+filename, 'w')
    f.write(header(p))
    f.write(p["post_content"])
    print "Wrote", ("(DRAFT)"if is_draft(p) else "") + p["post_title"]

import MySQLdb as db
import sys

con = None

con = db.connect('localhost', '', '', 'wordpress');

cur = con.cursor(db.cursors.DictCursor)
cur.execute("select post_title, post_name, post_status, post_date, post_content from wp_posts where post_status in ('publish', 'draft') and post_type='post';")
data = cur.fetchall()

for p in data:
    write_post(p)

cur = con.cursor(db.cursors.DictCursor)
cur.execute("select post_title, post_name, post_status, post_date, post_content from wp_posts where post_status in ('publish', 'draft') and post_type='page';")
data = cur.fetchall()
for p in data:
    write_page(p)

    
