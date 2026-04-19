import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("أهلاً بك 👋 البوت يعمل بنجاح.")

def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("الأمر المتاح الآن: /start")

def run_bot():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))

    print("Bot running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
