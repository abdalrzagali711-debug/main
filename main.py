import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

# --- إعدادات السيرفر للبقاء حياً 24 ساعة ---
app = Flask('')

@app.route('/')
def home():
    return "BotTech is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
# استبدل TOKEN بـ التوكن الخاص بك من BotFather
TOKEN = "8529228658:AAG9PQs13d_awMgUplnFVesR5WG70Ion5UY"
bot = telebot.TeleBot(TOKEN)

# --- قاعدة بيانات تجريبية (يمكنك توسيعها) ---
tech_data = {
    "الجوالات": {
        "iPhone 15 Pro Max": {
            "السعر": "5100 ريال",
            "المميزات": "شاشة LTPO Super Retina، معالج A17 Pro، هيكل تيتانيوم.",
            "العيوب": "سعر مرتفع جداً، سرعة الشحن لا تزال بطيئة مقارنة بالمنافسين."
        },
        "Samsung S24 Ultra": {
            "السعر": "4500 ريال",
            "المميزات": "كاميرا 200MP، قلم S-Pen مدمج، ذكاء اصطناعي متطور.",
            "العيوب": "حجم الهاتف كبير وثقيل، التصميم لم يتغير كثيراً."
        }
    },
    "اللابتوبات": {
        "MacBook Pro M3": {
            "السعر": "7500 ريال",
            "المميزات": "أداء جبار، بطارية تدوم 22 ساعة، شاشة Liquid Retina XDR.",
            "العيوب": "سعر الترقية للرام غالي، لا يدعم تشغيل جميع الألعاب."
        },
        "Dell XPS 15": {
            "السعر": "6800 ريال",
            "المميزات": "أفضل شاشة في عالم ويندوز، جودة تصنيع ممتازة.",
            "العيوب": "يسخن قليلاً عند العمل المكثف، عدد المنافذ محدود."
        }
    },
    "الساعات الذكية": {
        "Apple Watch Ultra 2": {
            "السعر": "3200 ريال",
            "المميزات": "سطوع شاشة عالي، بطارية أفضل من النسخ العادية، مقاومة للماء.",
            "العيوب": "حجمها ضخم على المعاصم الصغيرة، تعمل مع آيفون فقط."
        },
        "Huawei Watch GT 4": {
            "السعر": "900 ريال",
            "المميزات": "تصميم كلاسيكي فخم، بطارية تدوم أسبوعين، سعر ممتاز.",
            "العيوب": "لا يمكن الرد على رسائل الواتساب بالكامل، نظام التطبيقات محدود."
        }
    }
}

# --- لوحة التحكم والأزرار ---

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [types.KeyboardButton(cat) for cat in tech_data.keys()]
    markup.add(*btns)
    return markup

def companies_menu(category):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [types.KeyboardButton(comp) for comp in tech_data[category].keys()]
    markup.add(*btns, types.KeyboardButton("🔙 العودة للقائمة الرئيسية"))
    return markup

# --- معالجة الأوامر ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في BotTech 🤖\nدليلك للمقارنة بين أحدث الأجهزة التقنية.", 
                 reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text in tech_data.keys())
def select_category(message):
    category = message.text
    bot.send_message(message.chat.id, f"اختر الشركة أو الجهاز من قسم {category}:", 
                     reply_markup=companies_menu(category))

@bot.message_handler(func=lambda message: any(message.text in tech_data[cat] for cat in tech_data))
def show_details(message):
    item = message.text
    for cat in tech_data:
        if item in tech_data[cat]:
            info = tech_data[cat][item]
            res = (f"📌 الجهاز: {item}\n"
                   f"💰 السعر التقريبي: {info['السعر']}\n\n"
                   f"✅ المميزات:\n{info['المميزات']}\n\n"
                   f"❌ العيوب:\n{info['العيوب']}")
            bot.send_message(message.chat.id, res, parse_mode="Markdown")
            break

@bot.message_handler(func=lambda message: message.text == "🔙 العودة للقائمة الرئيسية")
def back(message):
    bot.send_message(message.chat.id, "تمت العودة للقائمة الرئيسية", reply_markup=main_menu())

# --- تشغيل البوت ---
if __name__ == "__main__":
    keep_alive() # تشغيل سيرفر الويب في الخلفية
    print("BotTech is starting...")

    bot.infinity_polling()
