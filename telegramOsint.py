import telebot
import re
import subprocess
from dependency import token, telegramID, api_id, api_hash


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    if str(message.from_user.id) not in telegramID:
        bot.send_message(message.chat.id, 'False')
        exit()
    bot.send_message(message.chat.id, 'Найти номер')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if str(message.from_user.id) not in telegramID:
        bot.send_message(message.chat.id, 'False')
        exit()
    if re.match(r"^((8|\+\d{1})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message.text) != None:
        subprocess.run(["python", "client.py", message.text, str(message.chat.id)], stdout=subprocess.DEVNULL)
        #subprocess.run(["python", "client.py ", message.text, str(message.chat.id)])
    elif message.text:
        bot.send_message(message.chat.id, "wrong number, re-enter")

bot.polling()
