import os
import urllib.request
import html
import re
import csv

def download_page(pageUrl):  
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'  
    try:
        page = urllib.request.Request(pageUrl, headers={'User-Agent':user_agent})
        with urllib.request.urlopen(page) as response:
            html = response.read().decode('windows-1251')
    except:
        print('Error at', pageUrl)
    return html

def clear_html (unclear_text):
    reg = re.compile('<div class=\"txt\">.*?</div>', flags=re.U | re.DOTALL)
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL) 
    text = reg.search(unclear_text)
    text = text.group(0)
    text = re.sub('</?div( class=\"txt\")?>',"", text)
    clean_t = regTag.sub("", text)
    clean_t = re.sub('\t\t\t', "", clean_t)
    return html.unescape(clean_t)
    
def find_name(html):
    reg = re.compile('<title>.*?</title>')
    name = reg.search(html)
    name = name.group(0)
    name = re.sub('</?title>', "", name)
    name = re.sub(' - воронежский информационный портал МОЁ! Online', "", name)
    return name.strip('.?!,""')

def find_author(text):
    reg = re.compile('<div class="news_author">.+</div>')
    author = reg.search(text)
    if author != None:
        author = author.group(0)
        author = re.sub('</?div ?(class="news_author")?>', "", author)
        author = author.split()
        surname = author[1]
        surname = surname[0] + surname[1:].lower()
        author = author[0] +' '+ surname
        return author
    else:
        return 'Noname'


def find_date(html):
    reg = re.compile('<a class="g_vol".*?>.*?</a>')
    time = re.compile('\d{1,2}\.\d{1,2}\.\d{4}')
    if reg.search(html)!= None:
        answer = reg.search(html)
        answer = answer.group(0)
        date = time.search(answer)
        if date != None:
            return date.group(0)
        else:
            return '01.01.2001'
    else:
        return '01.01.2001'


def clear_table(file, clearfile): # Ну, я же обещала код, который будет чистить таблицу
    f = open(file, 'r', encoding = 'utf-8')
    a = [line.strip() for line in f.readlines()]
    f.close()
    for line in a:
        if not line.find('01.01.1970') == -1:
            f1 = open(clearfile, 'a', encoding = 'utf-8')
            f1.write(line+'\n')
            f1.close()
        
        

commonUrl = 'http://newspaper.moe-online.ru/view/'
s=''
for i in range(217345, 241000):
    pageUrl = commonUrl + str(i) +'.html'
    date = find_date(download_page(pageUrl))
    a = date.split('.')
    var1='plain'
    var2='mystem-plain'
    var3='mystem-xml'
    directory1 = 'C:\\Users\\Lenovo\\Desktop\\Project\\MOE\\%s\\%s\\%s'%(var1, a[2],a[1])
    directory2 = 'C:\\Users\\Lenovo\\Desktop\\Project\\MOE\\%s\\%s\\%s'%(var2, a[2],a[1])
    directory3 = 'C:\\Users\\Lenovo\\Desktop\\Project\\MOE\\%s\\%s\\%s'%(var3, a[2],a[1])
    if not os.path.exists(directory1):
        os.makedirs(directory1)
        os.makedirs(directory2)
        os.makedirs(directory3)
    name = directory1 + '\\' + str(i) + '.txt'
    spisok = '@au %s\n@ti %s\n@da %s\n@url %s'
    try:
        doc = open(name, 'a', encoding = 'utf-8')
        doc.write(spisok %(find_author(download_page(pageUrl)), find_name(download_page(pageUrl)), find_date(download_page(pageUrl)), pageUrl))
        doc.write(clear_html(download_page(pageUrl)))
        doc.close()
    except:
        s+='%s '%(name) #я это делала для того, чтоб иметь список страниц, у которых были какие-то проблемы с кодировкой и просто почистить от них компьютер
    if not find_date(download_page(pageUrl)) == '01.01.1970' and not find_date(download_page(pageUrl)) == '01.01.2001': #придумала, как избежать лишних строк в таблице 
                     file = open('metadata2.txt', 'a', encoding = 'utf-8')
                     s1 = '%s\t%s\t\t\t%s\t%s\t\t'%(name, find_author(download_page(pageUrl)),find_name(download_page(pageUrl)), find_date(download_page(pageUrl)))
                     s2 = '\t\t\t\tнейтральный\tн-возраст\tн-уровень\tгородская\t'
                     s3 = '%s\tМОЁ\t\t%s\tгазета\tРоссия\tВоронеж\tru'%(pageUrl, a[2])
                     file.write(s1+s2+s3+'\n')
                     file.close()



for j in range (2007, 2016):
    for k in range (1, 13):
        n=k//10
        m=k%10
        k=str(n)+str(m)
        inp = "C:\\Users\\Lenovo\\Desktop\\Project\\MOE\\plain\\%d\\%s"%(j,k)
        txt = "C:\\Users\\Lenovo\\Desktop\\mystem.exe -cnid "
        xml = "C:\\Users\\Lenovo\\Desktop\\mystem.exe -cnid --format xml --eng-gr "
        if os.path.exists(inp):
            lst = os.listdir(inp)
            for fl in lst:
                mystem_plain = txt + inp + os.sep + fl + " C:\\Users\\Lenovo\\Desktop\\Project\\MOE\\mystem-plain\\%d\\%s"%(j,k) + os.sep + fl
                mystem_xml = xml + inp + os.sep + fl + " C:\\Users\\Lenovo\\Desktop\\Project\\MOE\\mystem-xml\\%d\\%s"%(j,k) + os.sep + fl[:len(fl)-4]+'.xml'
                os.system(mystem_plain)
                os.system(mystem_xml)

clear_table('metadata.txt', 'metadata1.txt')        

        

        
        
        






