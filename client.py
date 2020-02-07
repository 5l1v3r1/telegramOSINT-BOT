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
    res.append(contact_info.id)
    res.append(contact_info.username)
    res.append(contact_info.first_name)
    res.append(contact_info.last_name)
    res.append(client.download_profile_photo(contact_info.id))
    try:
        res.append(contact_info.status.was_online.astimezone(pytz.timezone('Europe/Kiev')))
    except:
        res.append("None")
except:
    bot.send_message(chatId, "Nomer nezaregan ili scrut")
    exit()
bot.send_message(chatId, "Number\tID\tUsername\tFirst_name\tLast_name\tPhoto\tLast_Online\n\n" + '\t'.join(str(x) for x in res))
if res[5] != None:
    bot.send_photo(chatId, open(res[5], "rb"))
    os.remove(res[5])