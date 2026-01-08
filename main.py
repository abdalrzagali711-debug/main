import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

# --- 1. إعداد سيرفر Flask لضمان استمرارية العمل على Render ---
app = Flask('')

@app.route('/')
def home():
    return "BotTech is Online and Running!"

def run():
    # Render يستخدم المنفذ 10000 أو المنفذ المحدد في البيئة
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- 2. إعداد البوت ---
# ملاحظة: يفضل تغيير التوكن من BotFather (Revoke) قبل وضعه هنا
TOKEN = "8261748166:AAFx1hxtYIT_VgVUGWDniEOYlvSJgEK5OBI"
bot = telebot.TeleBot(TOKEN)

# --- 3. قاعدة البيانات (الجوالات، اللابتوبات، الساعات) ---
tech_data = {
    "📱 الجوالات": {
        "iPhone 15 Pro Max": {
            "السعر": "5100 ريال",
            "المميزات": "شاشة LTPO Super Retina، معالج A17 Pro، هيكل تيتانيوم.",
            "العيوب": "سعر مرتفع جداً، شحن بطيء."
        },
        "Samsung S24 Ultra": {
            "السعر": "4500 ريال",
            "المميزات": "كاميرا 200MP، قلم S-Pen، ذكاء اصطناعي.",
            "العيوب": "حجم ضخم، وزن ثقيل."
        }
    },
    "💻 اللابتوبات": {
        "MacBook Pro M3": {
            "السعر": "7500 ريال",
            "المميزات": "بطارية خرافية (22 ساعة)، أداء صامت.",
            "العيوب": "سعر ترقية الرام مرتفع جداً."
        },
        "HP Spectre x360": {
            "السعر": "5500 ريال",
            "المميزات": "تصميم 2 في 1، شاشة OLED مذهلة.",
            "العيوب": "يسخن قليلاً عند الاستخدام المكثف."
        }
    },
    "⌚ الساعات": {
        "Apple Watch Ultra 2": {
            "السعر": "3200 ريال",
            "المميزات": "مقاومة صدمات، سطوع شاشة عالي.",
            "العيوب": "تعمل مع آيفون فقط، حجم ضخم."
        },
        "Huawei Watch GT 4": {
            "السعر": "900 ريال",
            "المميزات": "بطارية تدوم 14 يوم، سعر ممتاز.",
            "العيوب": "نظام التطبيقات محدود."
        }
    }
}

# --- 4. نظام الأزرار ---

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [types.KeyboardButton(cat) for cat in tech_data.keys()]
    markup.add(*btns)
    return markup

def companies_menu(category):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [types.KeyboardButton(comp) for comp in tech_data[category].keys()]
    markup.add(*btns, types.KeyboardButton("🔙 القائمة الرئيسية"))
    return markup

# --- 5. معالجة الرسائل ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🤖 مرحباً بك في BotTech\n\nاختر القسم الذي تود استكشافه:", 
                     reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text in tech_data.keys())
def select_category(message):
    category = message.text
    bot.send_message(message.chat.id, f"اختر الجهاز من قسم {category}:", 
                     reply_markup=companies_menu(category))

@bot.message_handler(func=lambda message: any(message.text in tech_data[cat] for cat in tech_data))
def show_details(message):
    item = message.text
    for cat in tech_data:
        if item in tech_data[cat]:
            info = tech_data[cat][item]
            res = (f"📍 الجهاز: {item}\n"
                   f"💰 السعر التقريبي: {info['السعر']}\n\n"
                   f"✅ المميزات:\n{info['المميزات']}\n\n"
                   f"❌ العيوب:\n{info['العيوب']}")
            bot.send_message(message.chat.id, res, parse_mode="Markdown")
            break

@bot.message_handler(func=lambda message: message.text == "🔙 القائمة الرئيسية")
def back(message):
    bot.send_message(message.chat.id, "تمت العودة للقائمة الرئيسية", reply_markup=main_menu())

# --- 6. تشغيل البوت مع حل مشكلة الـ Conflict ---
if __name__ == "__main__":
    keep_alive() # تشغيل Flask في الخلفية
    print("BotTech is starting...")
    
    # تنظيف أي Webhook قديم لتجنب خطأ 409
    bot.remove_webhook()
    
    # تشغيل البوت مع تخطي الرسائل القديمة (skip_pending)
    bot.infinity_polling(skip_pending=True)
