import pandas as pd
import re
import os
import datetime
import codecs
from nltk import tokenize

PERSONAL_OPINIONS = [r'(I|My|my)[^,]+opinion[^s]', r'I[^,]+(think|believe|agree)[^s]', r'(I|i)n my mind',
                     r'(I|i)t would seem that', r'(T|t)h(is|at) (proves|suggests|supports) th(at|e)',
                     r'(I|i)t could be argued']


def get_personal_opinion_matches(s: str) -> list:
    res = list()
    for op in PERSONAL_OPINIONS:
        res.append(re.search(op, s))
    return res


def get_problem_matches(p_block: str) -> list:
    res = list()
    sentences = tokenize.sent_tokenize(p_block)
    if len(sentences) < 2:
        return res
    m1 = re.search(r'\?$', sentences[-1])
    m2 = re.search(r'\?$', sentences[-2:-1][0])
    if not (m1 or m2):
        m = re.search(r'(his essay|estion is)', p_block)
        if m:
            res.append(sentences[-2:-1])
    else:
        res.append(sentences[-2:-1])
    return res


path_to_dir = "C:\\Users\\Admin\\Projects\\CsvToText\\1599499468"

raw_data = dict()
for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
        raw_data[filename] = list(map(lambda s: s.strip(), f.read().split('\n')[7:]))

print(raw_data['0050477_en_Nowadays_the_problem_of_the_spread_of_coronovirus_infection_noexp.txt'])

# analyse
for text in raw_data.values():
    for block in text[1:-1]:
        print(block)
        # for sentence in block.split('.'):
        #    if sentence.count('his proves that') > 0:
        #        print(sentence.strip())

# working
for text in raw_data.values():
    for block in text:
        for sentence in tokenize.sent_tokenize(block):
            for m in get_personal_opinion_matches(sentence):
                if m:
                    print(sentence)

# FINAL
for text in raw_data.values():
    for block in text:
        for sentence in tokenize.sent_tokenize(block):
            for m in get_personal_opinion_matches(sentence):
                if m:
                    print(sentence)

    block = text[0]
    print(get_problem_matches(block))