import flask
import telebot 
import conf
import re
import random

rules = ['Чаще всего разделительные запятые используются при однородных членах предложения, связанных бессоюзной связью: «По волнам носились барки, лодки, доски, бревна, крыши, вырванные с корнем деревья»',
         'Обратите внимание: разделительная запятая не ставится в устойчивых оборотах (поговорить о том о сём, проснулся ни свет ни заря) и не употребляется в составных наименованиях (ложки чайные мельхиоровые)',
         'Определите, используются ли в предложении между однородными членами повторяющиеся союзы. В этом случае запятые ставятся, в отличие от конструкций с одиночными сочинительными союзами. Например: «Я успевал быть и на катке, и в театре»; «Я успевал быть на катке и в театре».',
         'Всегда используйте разделительную запятую перед противительными союзами (а, но, однако, зато, да): «Всюду пахнет цветущей липой, а тут особенно»',
         'Используйте парные выделительные запятые, если предложение осложнено конструкциями, грамматически не связанными с другими его членами. К таким конструкциям относятся обращения, вводные слова и вводные предложения.',
         'Отделяйте запятыми простые предложения в составе сложного. Для этого найдите грамматические основы, определите границы простых предложений и расставьте знаки.']
      

def com_count(text):
    return len(re.findall(',', text))

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded = False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает количество запятых в вашем сообщении.")
	
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Сомневаетесь, правильно ли Вы поставили запятую? Чтобы освежить в памяти какое-нибудь правило, напишите /rules :)")

@bot.message_handler(commands=['rules'])
def send_help(message):
    bot.send_message(message.chat.id, rules[random.choice(range(0,6))])
    
@bot.message_handler(func=lambda m: True)  
def send_len(message):
    n = com_count(message.text)
    if n%10 == 1 and n != 11:
        bot.send_message(message.chat.id, 'В вашем сообщении {} запятая'.format(n))
    elif n%10 == 2 and n != 12:
        bot.send_message(message.chat.id, 'В вашем сообщении {} запятые'.format(n))
    elif n%10 == 3 and n != 13:
        bot.send_message(message.chat.id, 'В вашем сообщении {} запятые'.format(n))
    else:
        bot.send_message(message.chat.id, 'В вашем сообщении {} запятых'.format(n))
               
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

