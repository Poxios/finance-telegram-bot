from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
import telegram
import json

# & Import from local
import controller_sqlite
from api_stock import get_full_finance_info_message


def get_telegram_bot_token_from_secret():
    with open("./src/secrets.json", "r") as file:
        data = json.load(file)
        return (data["TELEGRAM_BOT_TOKEN"], data["TELEGRAM_BOT_ADMIN_USER_ID"])


TELEGRAM_BOT_TOKEN = get_telegram_bot_token_from_secret()[0]
TELEGRAM_ADMIN_USER_ID = get_telegram_bot_token_from_secret()[1]

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
# ! Define Methods


async def send_telegram_message(userId: int, message: str):
    await bot.send_message(chat_id=userId, text=message, parse_mode="HTML")


# ! Registering Command Handlers
# ? Manage Stock
# $ Add stock ticker to user stock list


async def command_handler_add_stock_ticker_to_user(update, context):
    user_id = update.effective_chat.id
    if not len(context.args):
        res_str = "Please enter the stock ticker.\n"
        res_str += "<code>/addstock QQQ</code>"
        await context.bot.send_message(chat_id=user_id, text=res_str, parse_mode="HTML")
        return
    ticker_to_add = context.args[0].upper()
    if controller_sqlite.favorite_stock_add_to_user(user_id, ticker_to_add):
        await context.bot.send_message(chat_id=user_id, text="Add Done")
    else:
        await context.bot.send_message(chat_id=user_id, text="Add Failed")


app.add_handler(
    CommandHandler(
        "addstock", has_args=True, callback=command_handler_add_stock_ticker_to_user
    )
)

# $ Remove stock ticker from user stock list


async def command_handler_remove_stock_ticker_to_user(update, context):
    user_id = update.effective_chat.id
    ticker_to_remove = context.args[0].upper()
    controller_sqlite.favorite_stock_remove_from_user(user_id, ticker_to_remove)
    await context.bot.send_message(chat_id=user_id, text="Remove Done")


app.add_handler(
    CommandHandler(
        "removestock",
        has_args=True,
        callback=command_handler_remove_stock_ticker_to_user,
    )
)

# $ Get my favorite stock list


async def command_handler_get_favorite_stock_list(update, context):
    user_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=TELEGRAM_ADMIN_USER_ID,
        text=controller_sqlite.favorite_stock_get_list(user_id),
    )


app.add_handler(
    CommandHandler("showstocks", callback=command_handler_get_favorite_stock_list)
)


# ? Execute Command
# $ New User Detected


async def command_handler_new_user_detected(update, context):
    user_id = update.effective_chat.id
    user_name = update.effective_user.full_name
    await context.bot.send_message(
        chat_id=TELEGRAM_ADMIN_USER_ID,
        text=f"New user detected: {user_id} / {user_name}",
    )


app.add_handler(CommandHandler("start", command_handler_new_user_detected))

# $ New User add (ADMIN ONLY)


async def command_handler_new_user_add(update, context):
    user_id = update.effective_chat.id
    if str(TELEGRAM_ADMIN_USER_ID) != str(user_id):
        return
    user_id_to_add, user_name = context.args
    controller_sqlite.user_add_new_user(user_id_to_add, user_name)
    await context.bot.send_message(
        chat_id=TELEGRAM_ADMIN_USER_ID,
        text=f"Adding new user done {user_id_to_add} / {user_name}",
    )


app.add_handler(
    CommandHandler("adduser", has_args=True, callback=command_handler_new_user_add)
)

# $ Get User List (ADMIN ONLY)


async def command_handler_get_user_list(update, context):
    user_id = update.effective_chat.id
    if str(TELEGRAM_ADMIN_USER_ID) != str(user_id):
        return
    await context.bot.send_message(
        chat_id=TELEGRAM_ADMIN_USER_ID, text=str(controller_sqlite.user_get_list())
    )


app.add_handler(CommandHandler("getuser", callback=command_handler_get_user_list))


# $ Send Command List


async def command_handler_help(update, context):
    response_str = ""
    response_str += (
        "<code>/addstock QQQ    </code> Add QQQ to your favorite stock list.\n"
    )
    response_str += (
        "<code>/removestock QQQ </code> Remove QQQ from your favorite stock list.\n"
    )
    response_str += "<code>/showstocks      </code> Show your favorite stocks list.\n"
    response_str += "<code>/fetchnow        </code> Fetch finance info now."
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id, text=response_str, parse_mode="HTML")


app.add_handler(CommandHandler("help", command_handler_help))

# $ Fetch finance and send it.


async def command_handler_fetch_now(update, context):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id, text="Fetching finance info..")
    full_message = get_full_finance_info_message(user_id)
    await context.bot.send_message(chat_id=user_id, text=full_message, parse_mode="HTML")


app.add_handler(CommandHandler("fetchnow", command_handler_fetch_now))


async def start_polling():
    print('[SYSTEM] Start telegram polling...')
    await app.run_polling()
