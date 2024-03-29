import re
import os
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

OPINIONS = [r'ere are two points of view', r'(opinion|other)s',
            r'(people|they) (think|thought|believe|believed|consider|considered|claim)',
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


path_to_dir = "C:\\Users\\Admin\\Projects\\CsvToText\\fixed_texts"

raw_data = dict()
heads = dict()
for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        if not filename.endswith('txt'):
            continue
        f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
        text = f.read()
        if re.search(r'(ПРОБЛЕМА|АРГУМЕНТ|ПРМНЕНИЕ|ВЫВОД|ЛМНЕНИЕ)', text):
            continue
        raw_data[filename] = list(map(lambda s: s.strip(), text.split('\n')))
        if str(raw_data[filename][0]).count('Тема'):
            heads[filename] = raw_data[filename][:7]
            raw_data[filename] = raw_data[filename][7:]

print(len(raw_data))
print(raw_data['0051498_en_Is_online_schooling_as_effective_as_in-class_education_Exp114.txt'])

result_dict = dict()
for filename in raw_data:
    text = raw_data[filename]
    result = {'text': text}
    h = hash(str(result))

    block = text[0]
    if len(get_problem_matches(block)) > 0:
        result['problem'] = block

    for block in text[1:-2]:
        if len(get_arguments_matches(block)) > 0:
            result['arguments'] = block
        elif len(get_other_opinions(block)) > 0:
            result['other'] = block

    block = text[-1]
    if len(get_conclusion_matches(block)) > 0:
        result['conclusion'] = block

    if len(text) > 1:
        for block in text[:-1]:
            for sentence in tokenize.sent_tokenize(block):
                if len(get_personal_opinion_matches(sentence)) > 0:
                    result['personal'] = block

    if hash(str(result)) != h:
        result_dict[filename] = result

print(len(result_dict))
print(result_dict['0051498_en_Is_online_schooling_as_effective_as_in-class_education_Exp114.txt'])

PROBLEM_PLACEHOLDER = '(\\ ПРОБЛЕМА \\ placeholder :: Введение, формулировка проблемы. \\)'
ARGUMENTS_PLACEHOLDER = '(\\ АРГУМЕНТ  \\ placeholder \\)'
OTHER_PLACEHOLDER = '(\\ ПРМНЕНИЕ \\ placeholder :: Противоположное мнение \\)'
CONCLUSION_PLACEHOLDER = '(\\ ВЫВОД \\ placeholder \\)'
PERSONAL_PLACEHOLDER = '(\\ ЛМНЕНИЕ \\ placeholder :: Личное мнение \\)'


def replace_by_block(addition_text: str, PLACEHOLDER: str, source_text: str) -> str:
    replacement_text = PLACEHOLDER.replace('placeholder', addition_text)
    return re.sub(re.escape(addition_text), replacement_text, source_text)


for filename in result_dict:
    source_text = '\n'.join(raw_data[filename])
    additions = result_dict[filename]
    for addition in additions:
        if addition == 'text':
            continue
        elif addition == 'problem':
            source_text = replace_by_block(additions[addition], PROBLEM_PLACEHOLDER, source_text)
        elif addition == 'arguments':
            source_text = replace_by_block(additions[addition], ARGUMENTS_PLACEHOLDER, source_text)
        elif addition == 'other':
            source_text = replace_by_block(additions[addition], OTHER_PLACEHOLDER, source_text)
        elif addition == 'conclusion':
            source_text = replace_by_block(additions[addition], CONCLUSION_PLACEHOLDER, source_text)
        elif addition == 'personal':
            source_text = replace_by_block(additions[addition], PERSONAL_PLACEHOLDER, source_text)
    print('\n', filename)
    print(source_text)

    f = open('.\\added_texts\\' + filename, "w+", encoding='utf-8')
    head = heads.get(filename)
    if head is not None:
        f.write('\n'.join(head))
        f.write('\n')
    f.write(source_text)
    f.close()


