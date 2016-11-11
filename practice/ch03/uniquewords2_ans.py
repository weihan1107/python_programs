#!/usr/bin/python

import collections
import string
import sys


words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + "\"'"
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip(strip)
            if len(word) > 2:
                words[word] += 1

new_words = collections.defaultdict(set)
for key, value in words.items():
    new_words[value].add(key)

for num in sorted(new_words, reverse=True):
    for word in sorted(new_words[num]):
        print("'{0}' occurs {1} times".format(word, num))
