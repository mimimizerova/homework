import random
from pymorphy2 import MorphAnalyzer

data = dict()
morph = MorphAnalyzer()

f = open('dict.txt', 'r', encoding = 'utf-8')
for line in f:
    words = list(map(str,line.strip().split()))
    tag = morph.parse(words[0])[0].tag
    data[tag] = words
        
f.close()

txt = input()
text = list(map(str, txt.split()))
ans = []
for word in text:
    tag = morph.parse(word)[0].tag
    s = random.choice(data[tag])
    ans.append(s)
print(' '.join(map(str, ans)))
