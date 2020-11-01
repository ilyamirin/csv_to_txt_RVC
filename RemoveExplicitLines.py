import os
import codecs
import re

path_to_dir = "C:\\Users\\Admin\\Downloads\\remove lines"
path_to_fixed = "C:\\Users\\Admin\\Downloads\\fixed"


for root, dirs, files in os.walk(path_to_dir):
    for filename in files:
        f = codecs.open(path_to_dir + os.sep + filename, "r", "utf-8")
        text = f.read()
        f.close()

        c = 0
        n = 0
        for line in text.split('\n'):
            n += 1
            if len(line.strip()) == 0:
                c += 1
        if c > 1:
            filename = re.sub(r'nan\.txt', r'noexp.txt', filename)
            f = codecs.open(path_to_fixed + os.sep + filename, "w", 'utf-8')
            f.write(re.sub(u'\n\r\n\r', u'\n\r', text))
            f.close()
            print('Fixed:', filename)
        elif filename.endswith(r'nan\.txt'):
            filename = re.sub(r'nan\.txt', r'noexp.txt', filename)
            if len(filename) > 255:
                splt = filename.split('_')
                filename = '_'.join(splt[0:-3] + splt[-1:])
            f = codecs.open(path_to_fixed + os.sep + filename, "w", 'utf-8')
            f.write(text)
            f.close()
            print('Fixed:', filename)
