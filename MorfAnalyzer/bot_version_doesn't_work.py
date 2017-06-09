#Имя бота - @WordchangeBot
#Я не знаю в чём проблема, кажется, в кодировках...
import telebot 
import conf
import random
from pymorphy2 import MorphAnalyzer

data = dict()
morph = MorphAnalyzer()
bot = telebot.TeleBot(conf.TOKEN)

f = open('dict.txt', 'r', encoding='utf-8')
for line in f:
    words = list(map(str,line.strip().split()))
    tag = morph.parse(words[0])[0].tag
    data[tag] = words
        
f.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который заменяет все слова в вашем сообщении.")

@bot.message_handler(func=lambda m: True)  
def send_len(message):
    txt = message.text
    text = list(map(str, txt.split()))
    ans = []
    for word in text:
        tag = morph.parse(word)[0]
        s = random.choice(data[tag])
        ans.append(s)
    bot.send_message(message.chat.id, ' '.join(map(str, ans)))

if __name__ == '__main__':
    bot.polling(none_stop=True)
