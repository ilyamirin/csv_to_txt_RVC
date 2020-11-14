import os
import docx2txt

broken = list()
short = list()
data = dict()
for root, dirs, files in os.walk('эссе осень 2020'):
    for file in files:
        docx = os.path.join(root, file)
        #print(docx)
        try:
            text = docx2txt.process(docx)
            if len(text.split(' ')) < 200:
                short.append((docx, len(text.split(' '))))
            else:
                text = list(filter(lambda x: len(x.strip()) > 0, text.split('\n')))
                data[docx] = text
        except Exception:
            broken.append(docx)

path_to_save = 'essays'
c = 0
for i in data.items():
    f = open(os.path.join(path_to_save, str(c) + '.txt'), 'w', encoding='utf-8')
    f.write('\n'.join(i[1]))
    f.close()
    c += 1
    print(i[0])
