#!/usr/bin/python
import random

articles = ["the", "a", "another", "her", "his"]
subjects = ["cat", "dog", "horse", "man", "woman", "boy", "girl"]
verbs = ["sang", "ran", "jumped", "said", "fought", "swam", "saw",
         "heard", "felt", "slept", "hopped", "hoped", "cried",
         "laughed", "walked"]
adverbs = ["loudly", "quietly", "quickly", "slowly", "well", "badly", "rudely", "politely"]

for do in range(5):
    sentence_type = random.randint(0,1)
    if sentence_type:
        print random.choice(articles), random.choice(subjects), random.choice(verbs) 
    else:
        print random.choice(articles), random.choice(subjects), random.choice(verbs), random.choice(adverbs)
