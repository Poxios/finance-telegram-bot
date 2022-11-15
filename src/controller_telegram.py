from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Updater
import telegram
import json

# & Import from local
import controller_sqlite


def get_telegram_bot_token_from_secret():
    with open('./secrets.json', 'r') as file:
        data = json.load(file)
        return (data['TELEGRAM_BOT_TOKEN'], data['TELEGRAM_BOT_ADMIN_USER_ID'])


TELEGRAM_BOT_TOKEN = get_telegram_bot_token_from_secret()[0]
TELEGRAM_ADMIN_USER_ID = get_telegram_bot_token_from_secret()[1]

bot = telegram.bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(token=TELEGRAM_BOT_TOKEN)

# ! Define Methods


def send_telegram_message(userId: int, message: str):
    bot.sendMessage(chat_id=userId, text=message)


def get_complete_finance_message():
    raise Exception('IMPLEMENT')


def reply_to_command_wrapper(text: str):
    def send_message_via_commandhandler(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)
    return send_message_via_commandhandler


def fetch_finance_data_now_and_send(fetcher):
    def send_message_via_commandhandler(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=fetcher())
    return send_message_via_commandhandler


def test_handler(bot, update):
    """ 
    TEST
    """
    print(update)


dp = updater.dispatcher

# ! Registering Command Handlers
COMMAND_LIST_STR = 'addstock \n \
                    removestock \n \
                    fetchnow \n '
# ? Manage Stock
# $ Add stock ticker to user stock list
dp.add_handler(CommandHandler('addstock', pass_args=True,
               callback=controller_sqlite.add_stock_to_user))
# $ Remove stock ticker from user stock list
dp.add_handler(CommandHandler(
    'removestock', pass_args=True, callback=controller_sqlite.remove_stock_from_user))

# ? Execute Command
# $ Send Command List
dp.add_handler(CommandHandler(
    'help', reply_to_command_wrapper(COMMAND_LIST_STR)))

# $ Fetch finance and send it.
dp.add_handler(CommandHandler(
    'fetchnow', reply_to_command_wrapper(get_complete_finance_message)))

# ! Registering Normal Message Handlers
dp.add_handler(MessageHandler(callback=test_handler))


def start_polling():
    updater.start_polling()
