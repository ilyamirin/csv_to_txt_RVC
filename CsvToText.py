import pandas as pd
import re
import os
import datetime


def create_meta(file_dict):
    return "Тема: (* %(theme)s *)\nКласс: %(grade)s\nГод: 2020\nПредмет: английский\nТест: %(type)s\nЭксперт: " \
           "noexp\n\n" % file_dict
           #"%(Exp)s\n" % file_dict


def create_file(file_name, file_meta, file_body):
    f = open(file_name, "w+", encoding='utf-8')
    f.write(file_meta)
    f.write(file_body)
    f.close()


data = pd.read_csv("2801-3489.csv", delimiter=';')

prefix = u'%0d%1s' % (datetime.datetime.utcnow().timestamp(), os.path.sep)
os.mkdir(prefix)

for row in data.iterrows():
    file_dict = dict(row[1])

    if file_dict['theme'] is None or not isinstance(file_dict['theme'], str) or len(file_dict['theme']) == 0:
        file_dict['theme'] = u'_'.join(file_dict['body'].split()[:5])

    file_dict['file_theme'] = re.sub(r'(,|\.|!|\?|;|\s|\\|/|"|%|:|<|>|\*)', u'_', file_dict['theme'], 100)
    file_dict['file_theme'] = re.sub(r'_$', u'', file_dict['file_theme'], 1)
    file_dict['file_theme'] = re.sub(r'_{2}', u'_', file_dict['file_theme'], 1)

    filename = u'00%(number)d_en_%(file_theme)s_%(Exp)s.txt' % file_dict
    if len(filename) > 200:
        filename = filename[:50]+filename[100:]
    file_dict['meta'] = create_meta(file_dict)

    create_file(prefix + filename, file_dict['meta'], file_dict['body'])

