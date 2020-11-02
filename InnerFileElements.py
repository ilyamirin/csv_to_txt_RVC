import pandas as pd
import re
import os
import yaml

calculations = dict()

for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        calculations[file] = dict()
        calculations[file]['symbols'] = sum(list(map(lambda b: len(b), data.body)))
        calculations[file]['words'] = sum(list(map(lambda b: len(str(b).split(' ')), data.body)))
        calculations[file]['sentences'] = sum(list(map(lambda b: len(re.split(r'(;|\.|,|!|\?)', b, 9999)), data.body)))
        calculations[file]['blocks'] = sum(list(map(lambda b: len(re.split(r'(\r|\n|\n\n|\r\n|\n\r)', b, 9999)), data.body)))
        # m = re.search(r'^([0-9]{2,4})\-([0-9]{2,4})(_new)?\.csv', file)
        # calculations[file]['files'] = int(m.group(2)) - int(m.group(1))
        calculations[file]['files'] = len(data.values)
        calculations[file]['deficiency'] = (calculations[file]['files'] * 220 - calculations[file]['words']) / 200
        calculations[file]['deficiency'] = int(calculations[file]['deficiency'])

calculations_frame = pd.DataFrame.from_dict(calculations)
calculations_frame.to_clipboard()

all_files = dict()
for file in os.listdir('./'):
    if file.count('.csv') > 0:
        data = pd.read_csv(file, delimiter=';')
        for n, row in data.iterrows():
            all_files[row.number] = {'length': len(str(row.body).split(' '))}

all_files_frame = pd.DataFrame.from_dict(all_files)
print(all_files_frame.transpose()['length'].mean())