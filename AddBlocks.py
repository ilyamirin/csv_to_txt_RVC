import pandas as pd
import re
import os
import datetime
import codecs
from nltk import tokenize

PERSONAL_OPINIONS = [r'(I|My|my)[^,]+opinion[^s]', r'I[^,]+(think|believe|agree)[^s]', r'(I|i)n my mind',
                     r'(I|i)t would seem that', r'(T|t)h(is|at) (proves|suggests|supports) th(at|e)',
                     r'(I|i)t could be argued', r'(M|m)y point of view', r'(M|m)y perspective']

CONCLUSION = ['As Can Be Seen', 'After All', 'By And Large', 'Generally Speaking', 'In Fact', 'To Sum Up',
              'In The Final Analysis', 'On The Whole', 'All Things Considered', 'In Any Event', 'As Shown Above',
              'In Short', 'In Either Case',
              'In The Long Run', 'In Brief', 'All In All', 'Given These Points', 'In Essence', 'As Has Been Noted',
              'In A Word',
              'On Balance', 'For The Most Part', 'Altogether', 'Obviously', 'Overall', 'Ultimately', 'Ordinarily',
              'Definitely',
              'Usually', 'In this way', 'In conclusion', 'conclusion', 'summary', 'summarize', 'In general',
              'Based on this', 'Thus', 'Therefore', 'Summing up', 'In the end', 'To conclude', 'Finally', 'Overall',
              'conclusions', 'By using', 'In addition', 'Nevertheless', 'Despite', 'Collectively', 'We have shown that',
              'As A Result', 'Hence', 'By All Means', 'To Emphasize', 'Henceforth']

ARGUMENTS = ['Likewise', 'Correspondingly', 'Equally', 'Not only… but also', 'In the same way', 'Similarly',
             'Showing cause and effect', 'Consequently', 'As a result', 'Thus', 'Hence', 'Sinc', 'Because', 'Therefore',
             'Accordingly', 'This suggests that', 'It follows that', 'For this reason', 'Comparing and contrasting',
             'Alternatively', 'However', 'Conversely', 'On the other hand', 'Instead', 'Yet', 'On the contrary',
             'Showing limitation or contradiction', 'Despite', 'in spite of', 'While', 'Even so', 'On the contrary',
             'Nevertheless', 'Nonetheless', 'Although', 'Admittedly']

OPINIONS = [r'(opinion|other)s', r'(people|they) (think|thought|believe|believed|consider|considered)',
            r'(many|other|most|other) people', r'(opposite|in other hand|differently)']


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


def get_conclusion_matches(c_block: str) -> list:
    for concl_sentence in tokenize.sent_tokenize(c_block):
        for concl in CONCLUSION:
            concl_m = re.search(concl, concl_sentence, re.IGNORECASE)
            if concl_m:
                return [re.search(rf"{re.escape(concl_sentence)}.*$", c_block).group(0)]
    for concl_sentence in tokenize.sent_tokenize(c_block):
        print(concl_sentence)
    return []


def get_arguments_matches(c_block: str) -> list:
    res = list()
    for arg in ARGUMENTS:
        m = re.search(arg, c_block, re.IGNORECASE)
        if m:
            res.append(m.group())
    return res


def get_other_opinions(c_block: str) -> list:
    res = list()
    for regexp in OPINIONS:
        m = re.search(regexp, c_block, re.IGNORECASE)
        if m:
            res.append(m.group())
    return res


path_to_dir = "C:\\Users\\Admin\\Projects\\CsvToText\\1599666643"

raw_data = dict()
for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
        raw_data[filename] = list(map(lambda s: s.strip(), f.read().split('\n')[7:]))

print(raw_data['0050602_en_Is_online_schooling_as_effective_as_in-class_education_noexp.txt'])

for text in raw_data.values():
    for block in text:
        for sentence in tokenize.sent_tokenize(block):
            for m in get_personal_opinion_matches(sentence):
                if m:
                    print(sentence)

    block = text[0]
    print(get_problem_matches(block))

    for block in text[1:-2]:
        arguments = get_arguments_matches(block)
        if len(arguments) > 0:
            print(arguments)

    for block in text[1:-1]:
        opinions = get_other_opinions(block)

    block = text[-1]
    conclusion = get_conclusion_matches(block)
    print(conclusion[0])
