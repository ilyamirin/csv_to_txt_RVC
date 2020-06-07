import pandas as pd
import re
import os
import datetime


def create_file(file_name, file_body):
    print(file_name)
    f = open(file_name, "w+", encoding='utf-8')
    for i in file_body:
        f.write(file_body.trim() + "\r\n")
    f.close()


data = pd.read_csv("500.csv", delimiter=';')

prefix = u'%0d%1s' % (datetime.datetime.utcnow().timestamp(), os.path.sep)
os.mkdir(prefix)

for row in data.iterrows():
    file_dict = dict(row[1])

    if file_dict['theme'] is None or len(file_dict['theme']) == 0:
        print(file_dict)
        file_dict['theme'] = u'_'.join(file_dict['body'].split()[:5])

    file_dict['theme'] = re.sub(r'(,|\.|!|\?|;|\s|\\|/|"|%|:|<|>|\*)', u'_', file_dict['theme'], 100)
    file_dict['theme'] = re.sub(r'_$', u'', file_dict['theme'], 1)
    file_dict['theme'] = re.sub(r'_{2}', u'_', file_dict['theme'], 1)
    #print(file_dict['theme'])

    filename = u'%(number)d_en_%(theme)s_%(Exp)s.txt' % file_dict
    #print(filename)
    create_file(prefix + filename, file_dict['body'])

