#! /usr/bin/env python

from collections import Counter
import string
import numpy as np
import matplotlib.pyplot as plt
import wordcloud
from scipy.misc import imread
from os import path

curdir = path.dirname(__file__)

print curdir

exclude = set(string.punctuation)

counter = Counter()

with open("natday-songs.txt") as f:
    for line in f:
        # Remove possessives
        line = line.replace("'s", "")

        # Remove all punctuation
        line = ''.join(ch for ch in line if ch not in exclude)

        # Split into words
        words = line.strip().split(' ')

        # Make the words lowercase and remove empty words
        words = [w.lower() for w in words if w is not '']
        
        counter.update(words)

# Remove useless words
stopwords = wordcloud.STOPWORDS
stopwords.add("wooh")
stopwords.add("hooh")
stopwords.add("oh")
stopwords.add("will")
stopwords.add("ohohohohohohoh")

# Combine it back for word cloud
combined_text = ""
for k, v in counter.iteritems():
    combined_text += (k + " ") * v

singapore_mask = imread(path.join(curdir, "singapore-outline.jpg"))

# Generate word cloud
wc = wordcloud.WordCloud(margin=0,
                         font_path="/System/Library/Fonts/MarkerFelt.ttc",
                         mask=singapore_mask,
                         max_words=100,
                         stopwords=stopwords).generate(combined_text)

plt.imshow(wc)
plt.axis("off")
plt.show()

wc.to_file(path.join(curdir, "output.png"))

