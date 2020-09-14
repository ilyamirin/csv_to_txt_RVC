import re
import codecs

f = codecs.open('50101_en_The_major_disease_exp101.txt', "r", "utf-8")
text = f.read()

print('-------------')

i = 0
for j in range(0,5):
    for m in re.finditer(r'\(\\[^\(\)]+\)', text):
        g = m.group()
        text = re.sub(re.escape(g), '{%d}'%i, text) 
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
    
