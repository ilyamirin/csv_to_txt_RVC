import os
import codecs
import re

PREFIX = 'fixed_texts' + os.sep

path_to_dir = "C:\\Users\\Admin\\Projects\\CsvToText\\marked_texts"

raw_data = dict()
for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        print(filename)
        f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
        raw_data[filename] = f.read()

print(raw_data['50841_en_COVID-19_exp106.txt'])

new_data = dict()
print('-------------------------------------------------------------')
for filename in raw_data:
    text = raw_data[filename] + ''
    new_text = ''

    # try to remove gorged whitespaces
    m = re.search(r'\\\)[^,;:\.\?\!\-\n\s]', text)
    if m:
        text = text[:m.end()] + ' ' + text[m.end():]

    m = re.search(r'\S\(\\', text)
    if m:
        text = text[:m.end()] + ' ' + text[m.end():]

    # try to remove explicit linebreaks
    bs = list()
    for b in text.split('\n'):
        b = b.strip()
        if len(b) > 0:
            bs.append(b)
        if re.search(r'^Эксперт\:', b):
            bs.append('')
    text = '\n'.join(bs)

    new_data[filename] = text

print(raw_data['50552_en_Has_quarantining_due_to_the_coronavirus_caused_families_to_be_closer_or_farther_apart_Exp116.txt'])
print(new_data['50552_en_Has_quarantining_due_to_the_coronavirus_caused_families_to_be_closer_or_farther_apart_Exp116.txt'])

for filename in new_data:
    fname = filename
    if not re.search(r'^00', fname):
        fname = '00' + fname
    f = open(PREFIX + fname, "w+", encoding='utf-8')
    f.write(new_data[filename])
    f.close()
