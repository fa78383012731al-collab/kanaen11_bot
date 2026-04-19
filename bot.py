import os
import threading
import requests
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

# 🔥 قاعدة بيانات تجريبية (3 ملفات)
FILES = [
    {
        "name": "شهادات شكر PDF",
        "type": "pdf",
        "keywords": ["شهادة", "شكر"],
        "link": "https://drive.google.com/uc?id=1ARMS91AfzA2YK2oS46dOo9QrlQwK5gSh&export=download"
    },
    {
        "name": "شهادة وورد",
        "type": "docx",
        "keywords": ["شهادة", "وورد"],
        "link": "https://drive.google.com/uc?id=1FrQQceEc3V7LG3bzs29ZkP8hotkXoJPL&export=download"
    },
    {
        "name": "شهادات بوربوينت",
        "type": "pptx",
        "keywords": ["شهادة", "عرض"],
        "link": "https://drive.google.com/uc?id=1v63QRwfCUQ1m8MOXoZGCw8By7NRglgDa&export=download"
    }
]

# ▶️ بدء
def start(update: Update, context: CallbackContext):
    update.message.reply_text("اكتب كلمة للبحث مثل: شهادة")

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

# 📥 إرسال الملف مباشرة
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    file = FILES[int(query.data)]

    url = file["link"]

    # تحميل الملف من الرابط
    response = requests.get(url)

    # إرسال الملف
    query.message.reply_document(
        document=response.content,
        filename=f"{file['name']}.{file['type']}"
    )

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
