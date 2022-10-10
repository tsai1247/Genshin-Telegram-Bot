import os
from typing import List, Union

from Language import Language

from telegram import ForceReply
from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

load_dotenv()

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
text_limit = 4000

async def Reply(update: Update, msg: Union[list, str], forceReply: bool = False) -> None:
    Language.SetLang(update)
    if type(msg) is list:
        for m in msg:
            await update.message.reply_text(m)
    else:
        if(forceReply):
            await update.message.reply_text(msg, reply_markup = ForceReply(selective=forceReply))
        else:
            await update.message.reply_text(msg)
        
async def ReplyPhoto(update: Update, photolink: str) -> None:
    await update.message.reply_photo(photolink)

async def ReplyButton(update: Update, title: str, buttonText = List[List[str]], replyText = List[List[str]]):
    Language.SetLang(update)
    buttonList = buttonText
    for i in range(len(buttonList)):
        for j in range(len(buttonList[i])):
            buttonList[i][j] = InlineKeyboardButton(buttonText[i][j], callback_data = replyText[i][j]) 

    await update.message.reply_text(title, reply_markup = InlineKeyboardMarkup(buttonList))

async def ReplySticker(update: Update, file_id: str) -> None:
    await update.message.reply_sticker(file_id)
    
async def Send(chat_id: int, msg: str):
    Language.SetLang(chat_id)
    return await app.bot.send_message(chat_id, msg)


def GetUserID(update: Update) -> int:
    return update.message.from_user.id

def GetGroupID(update: Update) -> int:
    return update.message.chat.id
