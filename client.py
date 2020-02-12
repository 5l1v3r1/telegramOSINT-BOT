import sys
import os
from telethon import TelegramClient, types, sync, events
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
import pytz
import telebot
from dependency import token, telegramID, api_id, api_hash, passwordFor2Factor

bot = telebot.TeleBot(token)
client = TelegramClient('telegramOsint', api_id, api_hash)
client.start(password=passwordFor2Factor)
contact_phone_number = str(sys.argv[1])
chatId = sys.argv[2]
contact = InputPhoneContact(client_id=0, phone=contact_phone_number, first_name="", last_name="")
result = client(ImportContactsRequest([contact]))
res = []
try:
    contact_info = client.get_entity(contact_phone_number)
    res.append(contact_info.phone)
    userid = contact_info.id
    res.append(userid)
    res.append(contact_info.username)
    try:
        UsrInfo = bot.get_chat_member(userid, userid).user
        res.append(UsrInfo.first_name)
        res.append(UsrInfo.last_name)
        res.append(UsrInfo.language_code)
    except:
        res.append(contact_info.first_name)
        res.append(contact_info.last_name)
        res.append(contact_info.lang_code)
    res.append(client.download_profile_photo(contact_info.id))
    if hasattr(contact_info.status, "was_online"):
        res.append(contact_info.status.was_online.astimezone(pytz.timezone('Europe/Kiev')))
    else:
        res.append("Online")
except Exception as err:
    print(err)
    bot.send_message(chatId, "Nomer nezaregan ili scrut")
    exit()


masName = ["Number", "ID", "Username", "First_name", "Last_name", "language_code", "Photo", "Last_Online"]
resultString = ""
for i in range(len(masName)):
        resultString += str(masName[i]) + ": " + str(res[i]) + "\n"
bot.send_message(chatId, resultString)
if res[5] != None:
    bot.send_photo(chatId, open(res[6], "rb"))
    os.remove(res[6])
