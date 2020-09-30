import os
import codecs
import re

PREFIX = 'fixed_texts' + os.sep

path_to_dir = "C:\\Users\\Admin\\Projects\\CsvToText\\marked_texts"

raw_data = dict()
for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        print(filename)
        try:
            f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
            raw_data[filename] = f.read()
        except UnicodeDecodeError:
            f = codecs.open(path_to_dir + os.sep + filename, "r", "cp1251")
            raw_data[filename] = f.read()

print(raw_data['51641_en_Online_education_Bad_or_good_invention_Exp112.txt'])

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

    text = re.sub(r'[0-9]+\sслова', '', text)

    # try to remove explicit linebreaks
    bs = list()
    for b in text.split('\n'):
        b = b.strip()
        if len(b) > 0:
            bs.append(b)
        if re.search(r'^Эксперт\:', b):
            bs.append('')
    text = '\n'.join(bs)

    m = re.search(r'(\(\\[^\n(]+)(\n+)', text)
    if m:
        print(m.group(1))
        text = re.sub(re.escape(m.group(0)), m.group(1) + ' ', text, count=1)

    new_data[filename] = text

print(raw_data['51641_en_Online_education_Bad_or_good_invention_Exp112.txt'], '\n')
print(new_data['51641_en_Online_education_Bad_or_good_invention_Exp112.txt'])

print(new_data['51649_en_What_opportunities_quarantine_gave_me_Exp112.txt'])

for filename in new_data:
    fname = filename
    if not re.search(r'^00', fname):
        fname = '00' + fname
    f = open(PREFIX + fname, "w+", encoding='utf-8')
    f.write(new_data[filename])
    f.close()
