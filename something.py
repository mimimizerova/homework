from flask import Flask
from flask import url_for, render_template, request, redirect
import json 
app = Flask(__name__)

@app.route('/')
def personal_form():
    if request.args:
        name = request.args['name']
        gender = request.args['gender']
        age = request.args['age']
        p1 = request.args['понавыдумывать']
        p2 = request.args['понаоткрывать']
        p3 = request.args ['понаприклеить']
        p4 = request.args ['понаубираться']
        p5 = request.args ['понарассказать']
        p6 = request.args ['поназакрасить']
        json_d = {'name':name, 'gender':gender, 'age':age, 'понавыдумывать':p1, 'понаоткрывать':p2, 'понаприклеить': p3, 'понаубираться': p4, 'понарассказать': p5, 'поназакрасить': p6}
        data = json.dumps(json_d)
        file = open ('data.txt', 'a')
        file.write (data+'\n')
        file.close()
        f = open ('stats.txt', 'a')
        f.write (name + ' '+age + ' ' + gender + ' понавыдумывать: ' +p1 + ' понаоткрывать: '+ p2 + ' понаприклеить: ' + p3 + ' понаубираться: '+ p4 + ' понарассказать: ' + p5 + ' поназакрасить: '+ p6 + '\n')
        f.close()
        return render_template('answer.html', name=name)
    return render_template('form.html')

@app.route('/stats')
def stats():
    f = open ('stats.txt', 'r')
    words = f.read().split()
    f.close()
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    p5 = 0
    p6 = 0
    k = 0
    for i in range (len(words)):
        if i%15 == 2:
            if words[i] == 'ж':
                k+=1
        if i%15 == 4:
            p1 += int(words[i])
        if i%15 == 6:
            p2 += int(words[i])
        if i%15 == 8:
            p3 += int(words[i])
        if i%15 == 10:
            p4 += int(words[i])
        if i%15 == 12:
            p5 += int(words[i])
        if i%15 == 14:
            p6 += int(words[i])
    n = len(words)//14
    k = round((k/n)*100)
    m = 100 - k
    return render_template('stats.html', n=n, m=m, k=k, p1=p1/n, p2=p2/n, p3=p3/n, p4=p4/n, p5=p5/n, p6=p6/n)

@app.route('/json')
def json_str():
    f = open('data.txt', 'r')
    s = f.read()
    f.close()
    a = s.split('\n')
    json_str = json.dumps(a)
    return json_str

@app.route('/search')
def search():
    if request.args:
        word = request.args['word']
        f = open ('stats.txt', 'r')
        words = f.read().split()
        f.close()
        b = []
        for i in range (len(words)):
            if word in words[i]:
                if word.startswith('пона'):
                    b.append('<b>'+word+'</b>'+' '+words[i+1])
                elif word.isdigit() and int(word) <= 5 and word==words[i]:
                    b.append(words[i-1]+' '+'<b>'+word+'</b>')
                else:
                    k = i%15
                    s = ''
                    for j in range ((i-k), (i+15-k)):
                        s += words[j]+' '
                    s = s.replace(word, '<b>'+word+'</b>')
                    b.append(s)
        
        if b == []:
            b.append('Извините, по вашему запросу ничего не найдено. Попробуйте ещё!')
                 
                
        return render_template('result.html', b=b)
    return render_template('search.html')




if __name__ == "__main__":
    app.run()
