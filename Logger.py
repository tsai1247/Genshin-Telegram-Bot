import logging
from typing import Union
from telegram import Update

def appendlog(update: Union[Update, int], msg: Union[str, None] = None):
    if type(update) is Update:
        try:
            name = update.message.from_user.name
        except:
            name = update.message.from_user.full_name

        id = update.message.from_user.id
    else:
        name = r'{unknown}'
        id = update

    if msg == None:
        msg = update.message.text
        
    logging.info(f"[id]{id} [name]{name} [msg]\"{msg}\"")