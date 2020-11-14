import codecs
import pandas as pd
import re
import os
from shutil import copyfile

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


# проверяем уже размеченные файлы на адекватность

def fix_name(path_to_dir_of_fixing_file: str, filename_to_fix: str):
    if not filename_to_fix.startswith('00'):
        os.rename(path_to_dir_of_fixing_file + os.sep + filename_to_fix,
                  path_to_dir_of_fixing_file + os.sep + '00' + filename_to_fix)


path_to_dir = 'marked_texts'
for file in os.listdir(path_to_dir):
    fix_name(path_to_dir, file)

calculations = dict()
for file in os.listdir(path_to_dir):
    fix_name(path_to_dir, file)
    if file.count('.txt') == 0:
        continue
    f = codecs.open(path_to_dir + os.sep + file, "r", "utf-8")
    text = f.read()
    open_braces = re.findall(r'\(\\', text)
    close_braces = re.findall(r'\\\)', text)
    number = re.findall(r'^[0-9]+', file)[0]
    calculations[file] = [len(open_braces), len(close_braces), number]

broken = list()
weak = list()
combinations = dict()
for file in calculations:
    v = calculations[file]
    if v[0] - v[1] != 0:
        broken.append((file, v))
    if v[0] < 5:
        weak.append((file, v))
    if combinations.get(v[2]) is None:
        combinations[v[2]] = list()
    combinations[v[2]].append(v[0])

discrepancies = dict()
for number in combinations:
    v = combinations[number]
    if len(v) < 2:
        continue
    if max(v) / (min(v) + 0.00000000001) > 2:
        discrepancies[number] = v
pd.DataFrame.from_dict(discrepancies).transpose().to_excel(path_to_dir + os.sep + 'расхождения.xlsx')

suspected_experts = list()
for d in discrepancies:
    files = list(filter(lambda calc: str(calc).startswith(d), calculations.keys()))
    for file in files:
        mistakes_found = calculations[file][0]
        expert = re.search(r'([0-9]+)\.txt$', file).group(1)
        suspected_experts.append((expert, mistakes_found))
pd.DataFrame.from_records(suspected_experts).groupby([0]).mean().to_clipboard()

# тексты в которых неразмечены блоки
for file in os.listdir(path_to_dir):
    fix_name(path_to_dir, file)
    if file.count('.txt') == 0:
        continue
    f = codecs.open(path_to_dir + os.sep + file, "r", "utf-8")
    text = f.read()
    if not re.search(r'(ПРОБЛЕМА|АРГУМЕНТ|ПРМНЕНИЕ|ВЫВОД|ЛМНЕНИЕ)', text):
        print(file)
        copyfile(path_to_dir + os.sep + file, 'fixed_texts' + os.sep + file)

