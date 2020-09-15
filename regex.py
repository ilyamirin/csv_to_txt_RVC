import re
import codecs

f = codecs.open('C:\\Users\\Admin\\Projects\\CsvToText\\added_texts\\0050009_en_An_early_choice_of_a_carrier_path_is_the_key_to_success_Exp105.txt', "r", "utf-8")
text = f.read()

text = re.sub(r'(?<=[^\*\\])\)', ']', text)
text = re.sub(r'\((?=[^\*\\])', '[', text)

print('-------------')

i = 0
for j in range(0, 12):
    for m in re.finditer(r'\(\\[^\(\)]+\\\)', text):
        g = m.group()
        text = re.sub(re.escape(g), '{%d}' % i, text)
        print(i, g, m.start(), m.end())
        i += 1
    i *= 10

print('skeleton', text)

#i = 0
#for m in re.finditer(r'\([^\)]+\([^)]+\)[^\(]+\)', text):
#    print(i, m.group(), m.start(), m.end())
#    i += 1

#i = 0
#for m in re.finditer(r'\(.+\(.+\).+\)', text):
#for m in re.finditer(r'\(\\[^\)]+\([^\)]+\)[^\)]+\)', text):
    #print(i, m.group(), m.start(), m.end())
 #   i += 1
    
