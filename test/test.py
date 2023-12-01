from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
import telegram

app = ApplicationBuilder().token("TOKEN_HERE").build()
bot = telegram.Bot("TOKEN_HERE")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get user id
    print(update.message.from_user.id)
    print("------------------")
    # context.bot.send_message(chat_id=update.message.from_user.id, text='Hello',parse_mode=")
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


def command_handler_help(update, context):
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
    print(context.args)
    context.bot.send_message(chat_id=user_id, text=response_str, parse_mode="HTML")


app.add_handler(CommandHandler("hello", hello, has_args=True))
app.add_handler(CommandHandler("help", command_handler_help))

app.run_polling()
