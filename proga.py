import os
import re
txt = "C:\\Users\\Lenovo\\Desktop\\mystem.exe -cnid "
fl = r"C:\Users\Lenovo\Desktop\\Pr\\test.txt"
mystem_plain = txt + fl + " C:\\Users\\Lenovo\\Desktop\\Pr\\glossedtest.txt"
os.system(mystem_plain)
f = open( r'C:\Users\Lenovo\Desktop\Pr\test.txt', 'r', encoding = 'utf-8')
T = f.read().split()
f.close()

Words = []
Punct = [0] *(len(T))
for i in range (len(T)):
    if T[i].strip('.,!?":;') != T[i]:
        word = T[i].strip('.,!?":;')
        Punct[i] += 1
    else:
        word = T[i]
    Words.append(word)


d = open( r'C:\Users\Lenovo\Desktop\Pr\glossedtest.txt', 'r', encoding = 'utf-8')
S = d.read()
d.close()

def find_lemma(text):
    reg = re.compile('{[А-Яа-я]*=')
    A = reg.findall(text)
    Clear_A = []
    for lemma in A:
        lemma = re.sub('{', '', lemma)
        lemma = re.sub ('=', '', lemma)
        Clear_A.append(lemma)
    
    return Clear_A

Lemmas = find_lemma(S)
D = []
for i in range (len(Words)):
    D.append([Words[i], Lemmas[i]])



Clear_Words = [] 
for el in D:
    el[1] = el[1].lower()
    if el not in Clear_Words:
        Clear_Words.append(el)


file = open('table2.txt', 'a', encoding = 'utf-8')
for i in range (len(Clear_Words)):
    string = 'INSERT INTO "2nd" (id, wordform, lemma) VALUES (%d, "%s", "%s"); \n'%(i+1, Clear_Words[i][0], Clear_Words[i][1])
    file.write(string)
file.close()

doc = open ('table1.txt', 'a', encoding = 'utf-8')
for j in range (len(Words)):
    for k in range (len(Clear_Words)):
        if Words[j] == Clear_Words[k][0]:
            trueid = k+1
    string = 'INSERT INTO "1st" (id, wordtoken, rpunctuation, trueid) VALUES (%d, "%s", %d, %d); \n'%(j+1, Words[j], Punct[j], trueid)
    doc.write(string)
doc.close()

#rpunctuation показывает, был ли знак препинания справа от исходного слова или нет...
#а вообще я просто не очень поняла, что нужно делать с левыми и правыми знаками препинания.
