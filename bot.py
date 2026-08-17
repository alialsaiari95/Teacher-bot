import os
import telebot
from telebot import types
import google.generativeai as genai

# المفاتيح التي استخرجناها
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 1. القائمة الرئيسية (المراحل الدراسية)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🟢 الصف الأول المتوسط", callback_data="grade_1")
    btn2 = types.InlineKeyboardButton("🔵 الصف الثاني المتوسط", callback_data="grade_2")
    btn3 = types.InlineKeyboardButton("🟡 الصف الثالث المتوسط", callback_data="grade_3")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "أهلاً بك في البوت التعليمي 👋\nالرجاء اختيار المرحلة الدراسية:", reply_markup=markup)

# 2. قائمة المواد عند اختيار مرحلة
@bot.callback_query_handler(func=lambda call: call.data.startswith('grade_'))
def show_subjects(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📘 لغتي", callback_data="sub_lugati")
    btn2 = types.InlineKeyboardButton("📙 الفقه", callback_data="sub_fiqh")
    btn3 = types.InlineKeyboardButton("📗 التوحيد", callback_data="sub_tawheed")
    btn4 = types.InlineKeyboardButton("📕 التجويد", callback_data="sub_tajweed")
    markup.add(btn1, btn2, btn3, btn4)
    bot.edit_message_text("اختر المادة المطلوبة:", call.message.chat.id, call.message.id, reply_markup=markup)

# 3. اختيار الفصل الدراسي
@bot.callback_query_handler(func=lambda call: call.data.startswith('sub_'))
def show_terms(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📅 الفصل الدراسي الأول", callback_data="term_1")
    btn2 = types.InlineKeyboardButton("📅 الفصل الدراسي الثاني", callback_data="term_2")
    markup.add(btn1)
    bot.edit_message_text("اختر الفصل الدراسي:", call.message.chat.id, call.message.id, reply_markup=markup)

# 4. بوابة الدفع والاشتراك
@bot.callback_query_handler(func=lambda call: call.data.startswith('term_'))
def pay_gateway(call):
    markup = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("💳 اضغط هنا لتفعيل الاشتراك والدفع", url="https://moyasar.com") # رابط بوابة الدفع
    markup.add(pay_btn)
    bot.send_message(call.message.chat.id, "🔒 للوصول لمحتوى المادة ومساعد الذكاء الاصطناعي، يرجى إتمام الاشتراك عبر الرابط التالي:", reply_markup=markup)

bot.infinity_polling()
