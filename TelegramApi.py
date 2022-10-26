import os
from typing import List, Union

from telegram import ForceReply, Message
from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

load_dotenv()

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
text_limit = 4000

async def Reply(update: Update, msg: Union[list, str], forceReply: bool = False) -> None:
    if type(msg) is list:
        for m in msg:
            replyMsg = await update.message.reply_text(m)
    else:
        if(forceReply):
            replyMsg = await update.message.reply_text(msg, reply_markup = ForceReply(selective=forceReply))
        else:
            replyMsg = await update.message.reply_text(msg)
    return replyMsg

async def ReplyPhoto(update: Update, photolink: str) -> None:
    replyMsg = await update.message.reply_photo(photolink)
    return replyMsg

async def ReplyButton(update: Update, title: str, buttonText = List[List[str]], replyText = List[List[str]]):
    
    buttonList = buttonText
    for i in range(len(buttonList)):
        for j in range(len(buttonList[i])):
            buttonList[i][j] = InlineKeyboardButton(buttonText[i][j], callback_data = replyText[i][j]) 

    replyMsg = await update.message.reply_text(title, reply_markup = InlineKeyboardMarkup(buttonList))
    return replyMsg

async def ReplySticker(update: Update, file_id: str) -> None:
    replyMsg = await update.message.reply_sticker(file_id)
    return replyMsg
    
async def Send(chat_id: int, msg: str):
    if type(msg) is list:
        for m in msg:
            replyMsg = await app.bot.send_message(chat_id, m)
    else:
        replyMsg = await app.bot.send_message(chat_id, msg)
    return replyMsg

async def EditText(message: Message, text: str):
    await message.edit_text(text)
    return message

def GetUserID(update: Update) -> int:
    return update.message.from_user.id

def GetGroupID(update: Update) -> int:
    return update.message.chat.id
