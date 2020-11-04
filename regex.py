import re
import codecs


def unwind(file_to_unwind: str) -> dict:
    f = codecs.open(file_to_unwind, "r", "utf-8")
    text = f.read()

    result = dict()

    text = re.sub(r'(?<=[^\*\\])\)', ']', text)
    text = re.sub(r'\((?=[^\*\\])', '[', text)

    i = 0
    for j in range(0, 12):
        for m in re.finditer(r'\(\\[^\(\)]+\\\)', text):
            g = m.group()
            text = re.sub(re.escape(g), '{%d}' % i, text)
            result[i] = {'text': g, 'start': m.start(), 'end': m.end()}
            i += 1
        i *= 10
    result[i] = text

    return result


unwound = unwind('C:\\Users\\Admin\\Projects\\CsvToText\\fixed_texts\\0050153_en_My_future_exp107.txt')
for i in unwound:
    print(i, unwound[i])
