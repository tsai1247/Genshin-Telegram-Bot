#!/usr/bin/env python3
# coding=utf-8
import logging
import threading
from dotenv import load_dotenv

from Command import *
from TelegramApi import app

from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ApplicationBuilder, filters

load_dotenv()
logging.basicConfig(level=logging.INFO)

def AutoClaim_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(Daily.AutoClaim())
    loop.close()

# Main
def main():
    threading.Thread(target= AutoClaim_loop).start()
    
    # commands
    app.add_handler(CommandHandler('start', startbot))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('cookie', setcookie))
    app.add_handler(CommandHandler('daily', daily))
    app.add_handler(CommandHandler('note', note))
    app.add_handler(CommandHandler('gift', gift))
    app.add_handler(CommandHandler('hi', hi))
    app.add_handler(CommandHandler('notice', notice))
    app.add_handler(CommandHandler('account', setaccount))
    app.add_handler(CommandHandler('math', math))
    
    # when getting a text without command
    app.add_handler(MessageHandler(filters.TEXT, getText))

    # button click event
    app.add_handler(CallbackQueryHandler(callback))

    # error handler
    app.add_error_handler(error_handler)

    # run
    logging.info("KaTsuGenshinBot Server Running...")
    app.run_polling(stop_signals=None)

if __name__ == '__main__':
    main()

