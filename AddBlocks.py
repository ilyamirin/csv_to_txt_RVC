import pandas as pd
import re
import os
import datetime
import codecs
from nltk import tokenize

OPINIONS = [r'(I|My|my)[^,]+opinion[^s]', r'I[^,]+(think|believe|agree)[^s]', r'(I|i)n my mind',
            r'(I|i)t would seem that', r'(T|t)h(is|at) (proves|suggests|supports) th(at|e)', r'(I|i)t could be argued']


def get_opinion_matches(s: str) -> list:
    res = list()
    for op in OPINIONS:
        res.append(re.search(op, s))
    return res


path_to_dir = "C:\\Users\\Admin\\Projects\\CsvToText\\1599499468"

raw_data = dict()
for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
        raw_data[filename] = list(map(lambda s: s.strip(),f.read().split('\n')[7:]))

print(raw_data['0050477_en_Nowadays_the_problem_of_the_spread_of_coronovirus_infection_noexp.txt'])

# analyse
for text in raw_data.values():
    for block in text:
        for sentence in block.split('.'):
            if sentence.count('his proves that') > 0:
                print(sentence.strip())


# working
for text in raw_data.values():
    for block in text:
        for sentence in tokenize.sent_tokenize(block):
            for m in get_opinion_matches(sentence):
                if m:
                    print(sentence)

# final
for text in raw_data.values():
    for block in text:
        for sentence in tokenize.sent_tokenize(block):
            for m in get_opinion_matches(sentence):
                if m:
                    print(sentence)


