#!/usr/bin/env python

import sys
import unicodedata
import io

def print_unicode_table(word):
    filename = "unicode-table.txt"
    fh = io.open(filename, "w", encoding="utf8")
    fh.write(u"decimal   hex   chr  {0:^40}\n".format("name"))
    fh.write(u"-------  -----  ---  {0:-<40}\n".format(""))

    code = ord(" ")
    end = min(0xD800, sys.maxunicode) # Stop at surrogate pairs

    while code < end:
        c = chr(code)
        name = unicodedata.name(unicode(c), "*** unknown ***")
        if word is None or word in name.lower():
            fh.write(u"{0:7}  {0:5X}  {0:^3c}  {1}\n".format(code, name.title()))
        code += 1

word = None
if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print "usage: {0} [string]".format(sys.argv[0])
        word = 0
    else:
        word = sys.argv[1].lower()

if word !=0:
    print_unicode_table(word)
