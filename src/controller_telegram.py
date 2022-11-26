from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Updater
import telegram
import json

# & Import from local
import controller_sqlite
from api_stock import get_full_finance_info_message


def get_telegram_bot_token_from_secret():
    with open('./src/secrets.json', 'r') as file:
        data = json.load(file)
        return (data['TELEGRAM_BOT_TOKEN'], data['TELEGRAM_BOT_ADMIN_USER_ID'])


TELEGRAM_BOT_TOKEN = get_telegram_bot_token_from_secret()[0]
TELEGRAM_ADMIN_USER_ID = get_telegram_bot_token_from_secret()[1]

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(token=TELEGRAM_BOT_TOKEN)

# ! Define Methods


def send_telegram_message(userId: int, message: str):
    bot.sendMessage(chat_id=userId, text=message, parse_mode='MarkdownV2')


dp = updater.dispatcher

# ! Registering Command Handlers
# ? Manage Stock
# $ Add stock ticker to user stock list


def command_handler_add_stock_ticker_to_user(update, context):
    user_id = update.effective_chat.id
    ticker_to_add = context.args[0]
    if controller_sqlite.favorite_stock_add_to_user(
            user_id, ticker_to_add):
        context.bot.send_message(
            chat_id=user_id, text='success')
    else:
        context.bot.send_message(
            chat_id=user_id, text='failed')


# dp.add_handler(CommandHandler('addstock', pass_args=True,callback=command_handler_add_stock_ticker_to_user))
# $ Remove stock ticker from user stock list
# dp.add_handler(CommandHandler('removestock', pass_args=True, callback=controller_sqlite.favorite_stock_remove_from_user))

# ? Execute Command
# $ New User Detected
def command_handler_new_user_detected(update, context):
    user_id = update.effective_chat.id
    user_name = update.effective_user.full_name
    context.bot.send_message(
        chat_id=TELEGRAM_ADMIN_USER_ID, text=f'New user detected: {user_id} / {user_name}')


dp.add_handler(CommandHandler('start', command_handler_new_user_detected))

# $ Send Command List
COMMAND_LIST_STR = 'addstock \n \
                    removestock \n \
                    fetchnow \n '


def command_handler_help(update, context):
    user_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=user_id, text=COMMAND_LIST_STR)


dp.add_handler(CommandHandler(
    'help', command_handler_help))

# $ Fetch finance and send it.


def command_handler_fetch_now(update, context):
    user_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=user_id, text='Fetching finance info..')
    full_message = get_full_finance_info_message()
    context.bot.send_message(
        chat_id=user_id, text=full_message, parse_mode='HTML')


dp.add_handler(CommandHandler('fetchnow', command_handler_fetch_now))


def start_polling():
    updater.start_polling()
