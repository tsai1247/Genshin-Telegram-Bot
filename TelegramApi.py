from telegram import ForceReply
from telegram import Update
from typing import Union

async def Send(update: Update, msg: Union[list, str], forceReply: bool = False) -> None:
    if type(msg) is list:
        for m in msg:
            await update.message.reply_text(m)
    else:
        if(forceReply):
            await update.message.reply_text(msg, reply_markup = ForceReply(selective=forceReply))
        else:
            await update.message.reply_text(msg)
        
async def SendPhoto(update: Update, photolink: str) -> None:
    await update.message.reply_photo(photolink)

def GetUserID(update: Update) -> int:
    return update.message.from_user.id

def GetGroupID(update: Update) -> int:
    return update.message.chat.id
