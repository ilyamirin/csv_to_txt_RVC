import os
import codecs
import re

path_to_dir = "C:\\Users\\Admin\\Projects\\CsvToText\\marked_texts"

raw_data = dict()
for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        print(filename)
        f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
        #raw_data[filename] = list(map(lambda s: s.strip(), f.read().split('\n')[7:]))
        raw_data[filename] = f.read()

print(raw_data['50841_en_COVID-19_exp106.txt'])


new_data = dict()
print('-------------------------------------------------------------')
for filename in raw_data:
    text = raw_data[filename] + ''
    new_text = ''

    m = re.search(r'\\\)[^,;:\.\?\!\-\n\s]', text)
    if m:
        #prit(text[m.start()-4:m.end()+3])
        #print(text[m.start() - 4:m.start()+2] + ' ' + text[m.start()+2:m.end()+3])
        text = text[:m.start() + 2] + ' ' + text[m.start() + 2:]

    m = re.search(r'\S\(\\', text)
    if m:
        text = text[:m.start()+1] + ' ' + text[m.start()+1:]

    text = re.sub(r'[^\:]\n\s*\n', '\n', text)
    text = re.sub(r'[^\:]\s{2,}', '\n', text)

    new_data[filename] = text

print(new_data['50841_en_COVID-19_exp106.txt'])
