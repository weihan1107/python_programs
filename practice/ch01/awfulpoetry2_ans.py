#!/usr/bin/env python
import random
import sys

articles = ["the", "a", "another", "her", "his"]
subjects = ["cat", "dog", "horse", "man", "woman", "boy", "girl"]
verbs = ["sang", "ran", "jumped", "said", "fought", "swam", "saw",
         "heard", "felt", "slept", "hopped", "hoped", "cried",
         "laughed", "walked"]
adverbs = ["loudly", "quietly", "quickly", "slowly", "well", "badly", "rudely", "politely"]

try:
    num = int(sys.argv[1])
    if not (1 <= num <= 10):
        print "number should between 1 and 10"
        sys.exit()
except IndexError:
    num = 5

for do in range(num):
    sentence_type = random.randint(0,1)
    if sentence_type:
        print random.choice(articles), random.choice(subjects), random.choice(verbs) 
    else:
        print random.choice(articles), random.choice(subjects), random.choice(verbs), random.choice(adverbs)
