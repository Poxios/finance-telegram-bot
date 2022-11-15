from telegram.ext import CommandHandler
from telegram.ext import Updater
import random
import html
import urllib.request as urllib
import time
import os
import telegram
import json

# Initializing Telegram bot
my_telegram_id = os.environ.get('TELEBOT_MY_ID')
with open('./secrets.json', 'r') as file:
    data = json.load(file)
    print(data['TELEGRAM_BOT_TOKEN'])
bot = telegram.Bot(token=token)
updates = bot.getUpdates()
for u in updates:
    print(u.message)


updater = Updater(token=os.environ.get('TELEBOT_TOKEN'))
dispatcher = updater.dispatcher

my_list = ['\"this is line1\"',
           '\"this is line2\"',
           '\"this is line3\"',
           '\"this is line4\"',
           '\"this is line5\"'
           ]


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=random.choice(my_list))


my_handler = CommandHandler('start', start)

dispatcher.add_handler(my_handler)


def start_polling():
    updater.start_polling()
