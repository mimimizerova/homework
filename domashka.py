import urllib.request
import html
import re

def download_page(pageUrl): 
    try:
        page = urllib.request.Request(pageUrl)
        with urllib.request.urlopen(page) as response:
            htmla = response.read().decode('utf-8')
    except:
        print('Error at', pageUrl)
    return htmla

def clear_html (unclear_text):
    reg = re.compile('<p>.*?</p>', flags=re.U | re.DOTALL)
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL) 
    text = reg.findall(unclear_text)
    clear_text = []
    for el in text:
        el = regTag.sub("", el)
        el = html.unescape(el)
        arr = el.split()
        for word in arr:
            clear_word=''
            for j in range (len(word)): #смотрите объяснение этому циклу в readme
                if word[j].isalpha() or word[j].isdigit():
                    clear_word+=word[j]
            if clear_word != '':
                clear_text.append(clear_word.lower())
        arr = []

    return clear_text

def mnoj(Arr):
    return {Arr[i] for i in range (len(Arr))}

def arr(Mnoj):
    Arr = []
    for el in Mnoj:
        Arr.append(el)
    return Arr
    

A = clear_html(download_page(r'http://www.rosbalt.ru/style/2016/12/05/1572874.html'))
B = clear_html(download_page(r'https://life.ru/t/%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83%D1%80%D0%B0/941586/v_dien_50-lietiia_patrisiia_kaas_vypustila_iubilieinyi_albom'))
C = clear_html(download_page(r'http://www.vesti.ru/doc.html?id=2829099'))
D = clear_html(download_page(r'http://muzgazeta.com/pop/201664345/patrisiya-kaas-k-50-letnemu-yubileyu-vypustila-novyj-studijnyj-albom.html'))

a = mnoj(A)
b = mnoj(B)
c = mnoj(C)
d = mnoj(D)

plus_mnoj = a&b&c&d
plus = []
minus = []
clever = []

a1 = a -(a&b)
a2 = a - (a&c)
a3 = a - (a&d)
b1 = b - (b&a)
b2 = b - (b&c)
b3 = b - (b&d)
c1 = c - (c&a)
c2 = c - (c&b)
c3 = c - (c&d)
d1 = d - (d&a)
d2 = d - (d&b)
d3 = d - (c&b)

amin = a1&a2&a3
bmin = b1&b2&b3
cmin = c1&c2&c3
dmin = d1&d2&d3

minus_mnoj = amin|bmin|cmin|dmin

for el in plus_mnoj:
    plus.append(el)
plus.sort()

for el in minus_mnoj:
    minus.append(el)
    
minus.sort()


A1 = arr(amin)
B1 = arr(bmin)
C1 = arr(cmin)
D1 = arr(dmin)


dic1 = {A[i]:0 for i in range (len(A))}
dic2 = {B[i]:0 for i in range (len(B))}
dic3 = {C[i]:0 for i in range (len(C))}
dic4 = {D[i]:0 for i in range (len(D))}

for el in A:
    dic1[el]+=1

for el in A1:
    if dic1[el]>1:
        clever.append(el)
        
for el in B:
    dic2[el]+=1

for el in B1:
    if dic2[el]>1:
        clever.append(el)
        
for el in C:
    dic3[el]+=1

for el in C1:
    if dic3[el]>1:
        clever.append(el)

for el in D:
    dic4[el]+=1

for el in D1:
    if dic4[el]>1:
        clever.append(el)


clever.sort()

f = open ( 'intersection.txt', 'a', encoding = 'utf-8')
for el in plus:
    f.write(el+'\n')
doc = open ('symmetric_difference.txt', 'a', encoding = 'utf-8')
for el in minus:
    doc.write(el+'\n')

file = open ( 'clever_symmetric_difference.txt', 'a', encoding = 'utf-8')
for el in clever:
    file.write(el+'\n')

f.close()
doc.close()
file.close()
