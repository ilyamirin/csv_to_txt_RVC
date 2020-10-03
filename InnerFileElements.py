import pandas as pd
import re
import os
import yaml

for file in os.listdir('./'):
    if file.count('.csv') > 0:
        print(file)

for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        print(sum(list(map(lambda b: len(b), data.body))))

for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        print(sum(list(map(lambda b: len(str(b).split(' ')), data.body))))

for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        print(sum(list(map(lambda b: len(re.split(r'(;|\.|,|!|\?)', b, 9999)), data.body))))

for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        print(sum(list(map(lambda b: len(re.split(r'(\r|\n|\n\n|\r\n|\n\r)', b, 9999)), data.body))))

for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        print(len(data.values))

short_files = list()
for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        for n, row in data.iterrows():
            if len(str(row.body).split(' ')) < 220:
                short_files.append(row.number)

with open(r'./short_files.yaml', 'w+') as file:
    documents = yaml.dump(short_files, file)