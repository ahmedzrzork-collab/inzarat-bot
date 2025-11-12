import telebot
import json
from datetime import datetime
import os

BOT_TOKEN = os.environ.get("8513816478:AAHZzlZB9s8fv7191jJCgQTttLnejuOVNuY")  # التوكن من متغير البيئة

bot = telebot.TeleBot(BOT_TOKEN)
DATA_FILE = "inzarat.json"

try:
    with open(DATA_FILE, "r") as f:
        warnings = json.load(f)
except:
    warnings = {}

ADMINS = [1400339937]  # حط الـ Telegram ID مالتك هنا

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(warnings, f, indent=4)

@bot.message_handler(commands=["انذار"])
def warn_user(message):
    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "🚫 ما عندك صلاحية تستخدم هذا الأمر.")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "💬 رد على رسالة الشخص اللي تريد تسجل عليه إنذار.")
        return

    user_id = str(message.reply_to_message.from_user.id)
    user_name = message.reply_to_message.from_user.first_name
    reason = message.text.replace("/انذار", "").strip()

    if user_id not in warnings:
        warnings[user_id] = {"name": user_name, "count": 0, "list": []}

    warnings[user_id]["count"] += 1
    warnings[user_id]["list"].append({
        "reason": reason,
        "by": message.from_user.first_name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data()

    bot.reply_to(message, f"⚠️ تم إعطاء إنذار لـ {user_name}\n📝 السبب: {reason}\n🔢 عدد الإنذارات: {warnings[user_id]['count']}")

@bot.message_handler(commands=["الانذارات"])
def check_warnings(message):
    if not message.reply_to_message:
        bot.reply_to(message, "💬 رد على رسالة الشخص حتى أشوف إنذاراته.")
        return

    user_id = str(message.reply_to_message.from_user.id)
    if user_id not in warnings:
        bot.reply_to(message, "✅ هذا اللاعب ما عنده إنذارات.")
    else:
        count = warnings[user_id]["count"]
        bot.reply_to(message, f"🧾 اللاعب {warnings[user_id]['name']} عنده {count} إنذار{'ات' if count > 1 else ''}.")

@bot.message_handler(commands=["مسح"])
def clear_warnings(message):
    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "🚫 ما عندك صلاحية تستخدم هذا الأمر.")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "💬 رد على رسالة الشخص حتى أمسح إنذاراته.")
        return

    user_id = str(message.reply_to_message.from_user.id)
    if user_id in warnings:
        del warnings[user_id]
        save_data()
        bot.reply_to(message, "🧹 تم مسح كل الإنذارات.")
    else:
        bot.reply_to(message, "✅ ما عنده إنذارات أساساً.")

bot.infinity_polling()
