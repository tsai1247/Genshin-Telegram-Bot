#!/usr/bin/env python3
# coding=utf-8
import os
from requests.api import delete
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ApplicationBuilder, filters
from Command import *
from dotenv import load_dotenv

load_dotenv()

# Main
def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(CommandHandler('start', startbot))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('cookie', setcookie))
    app.add_handler(CommandHandler('account', setaccount))
    app.add_handler(CommandHandler('daily', daily))
    app.add_handler(CommandHandler('notice', notice))
    app.add_handler(CommandHandler('gift', gift))
    app.add_handler(CommandHandler('lang', lang))
    app.add_handler(CommandHandler('hi', hi))
    app.add_handler(MessageHandler(filters.TEXT, getText))
    app.add_handler(CallbackQueryHandler(callback))  # button click event



    print("KaTsuGenshinBot Server Running...")
    app.run_polling()

    # updater.start_polling()
    # updater.idle()

if __name__ == '__main__':
    main()

