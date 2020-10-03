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

print(raw_data['50541_en_Is_online_schooling_as_effective_as_in-class_education_exp107.txt'])

new_data = dict()

for filename in raw_data:
    text = raw_data[filename] + ''
    m = re.search(r'^Тема:', text)
    if not m:
        print(filename)
        m2 = re.search(r'^[0-9]+_en(.+)(\е|e)xp([0-9]+)\.txt', filename, re.IGNORECASE)
        if not m2:
            m2 = re.search(r'^[0-9]+_en(.+)(\е|e)([0-9]+)xp\.txt', filename, re.IGNORECASE)
        if not m2:
            m2 = re.search(r'^[0-9]+_en(.+)(\е|e)x([0-9]+)p\.txt', filename, re.IGNORECASE)
        if not m2:
            m2 = re.search(r'^[0-9]+_en(.+)(\е|e)xp\s?([0-9]+)\.txt', filename, re.IGNORECASE)
        if m2:
            meta = "Тема: (* %(theme)s *)\nКласс: 1 курс\nГод: 2020\nПредмет: английский\nТест: эссе тренировка\nЭксперт: " \
                   "exp%(exp)d\n\n" % {'theme': m2.group(1).replace('_', ' '), 'exp': int(m2.group(3))}
        elif m2 := re.search(r'^[0-9]+_en(.+)([0-9]+)(\е|e)xp\.txt', filename, re.IGNORECASE):
            meta = "Тема: (* %(theme)s *)\nКласс: 1 курс\nГод: 2020\nПредмет: английский\nТест: эссе тренировка\nЭксперт: " \
                   "exp%(exp)d\n\n" % {'theme': m2.group(1).replace('_', ' '), 'exp': int(m2.group(2))}
        elif m2 := re.search(r'^[0-9]+_en(.+)no(\е|e)xp\.txt', filename, re.IGNORECASE):
            meta = "Тема: (* %(theme)s *)\nКласс: 1 курс\nГод: 2020\nПредмет: английский\nТест: эссе тренировка\nЭксперт: " \
                   "noexp\n\n" % {'theme': m2.group(1).replace('_', ' ')}

        print(meta)
        text = meta + text
    new_data[filename] = text

print(new_data['50550_en_How_can_you_keep_in_touch_with_friends_while_staying_in_quarantine_Exp114.txt'])

for filename in new_data:
    text = new_data[filename] + ''

    # try to remove gorged whitespaces
    m = re.search(r'\\\)[^,;:\.\?\!\-\n\s]', text)
    if m:
        text = text[:m.end()] + ' ' + text[m.end():]

    m = re.search(r'\S\(\\', text)
    if m:
        text = text[:m.end()] + ' ' + text[m.end():]

    #text = re.sub(r'[0-9]+\sслова', '', text)

    # try to remove explicit linebreaks
    bs = list()
    for b in text.split('\n'):
        b = b.strip()
        if re.search(r'^(E|eЕ|е)xp[0-9]+$', b):
            continue
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

print(new_data['0050549_en_Is_online_schooling_as_affective_as_in-class_education_Exp106.txt'])

re.search(r'\r\n', new_data['50550_en_How_can_you_keep_in_touch_with_friends_while_staying_in_quarantine_Exp114.txt'])

for filename in new_data:
    fname = filename
    if not re.search(r'^00', fname):
        fname = '00' + fname
    f = open(PREFIX + fname, "w", encoding='utf-8')
    f.write(new_data[filename])
    f.close()
