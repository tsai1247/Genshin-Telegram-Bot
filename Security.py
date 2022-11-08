from Database.Config import *
from TelegramApi import GetUserID
from telegram import Update
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

dos_defence = {}

if Config.Get('penalty')['Val'] == None:
    Config.Set('penalty', 120)
penalty = Config.Get('penalty')['Val']

if Config.Get('dos_maximum')['Val'] == None:
    Config.Set('dos_maximum', 25)
dos_maximum = Config.Get('dos_maximum')['Val']

def isDos(update: Update):
    if update.message.from_user.id != update.message.chat.id:
        return True
    chat_id = GetUserID(update)
    date = update.message.date

    if chat_id not in dos_defence:
        dos_defence[chat_id] = [1, date]
        return False
        
    count = dos_defence[chat_id][0]
    lasttime = dos_defence[chat_id][1]
    during: timedelta = date - lasttime
    during = during.total_seconds()

    if count==-1:
        if during>penalty:
            dos_defence.update({chat_id : [1, date]})
            return False
        else:
            dos_defence.update({chat_id : [-1, date]})
            return True
    elif during>60:
        dos_defence.update({chat_id : [1, date]})
        return False
    elif count<dos_maximum:
        dos_defence.update({chat_id : [count+1, date]})
        return False
    else:
        dos_defence.update({chat_id : [-1, date]})
        return True

# def isAttack(text):
#     if '*' in text or '?' in text or '%' in text or '+' in text or '_' in text:
#         return True
#     if "\"" in text or '\'' in text:
#         return True
#     return False