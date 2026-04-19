import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

# 🔥 قاعدة بيانات تجريبية (3 ملفات فقط)
FILES = [
    {
        "name": "شهادات شكر وتقدير PDF",
        "type": "PDF",
        "keywords": ["شهادة", "شكر", "تقدير"],
        "link": "https://drive.google.com/uc?id=1ARMS91AfzA2YK2oS46dOo9QrlQwK5gSh&export=download"
    },
    {
        "name": "شهادة شكر Word",
        "type": "Word",
        "keywords": ["شهادة", "وورد"],
        "link": "https://drive.google.com/uc?id=1FrQQceEc3V7LG3bzs29ZkP8hotkXoJPL&export=download"
    },
    {
        "name": "شهادات PowerPoint",
        "type": "PPT",
        "keywords": ["شهادة", "عرض", "بوربوينت"],
        "link": "https://drive.google.com/uc?id=1v63QRwfCUQ1m8MOXoZGCw8By7NRglgDa&export=download"
    }
]

def start(update: Update, context: CallbackContext):
    update.message.reply_text("اكتب اسم الملف أو كلمة مثل: شهادة")

# 🔍 البحث
def search(update: Update, context: CallbackContext):
    text = update.message.text

    results = []
    for file in FILES:
        if any(k in text for k in file["keywords"]):
            results.append(file)

    if not results:
        update.message.reply_text("❌ لا يوجد نتائج")
        return

    keyboard = []
    for i, file in enumerate(results):
        keyboard.append([InlineKeyboardButton(file["name"], callback_data=str(i))])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("📂 اختر الملف:", reply_markup=reply_markup)

# 📥 عند الضغط
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    file = FILES[int(query.data)]

    query.message.reply_text(f"⬇️ تحميل:\n{file['link']}")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
