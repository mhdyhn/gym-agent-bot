mhdy, [07.07.25 13:57]
import telebot
import os
import json
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")  # توکن ربات از متغیر محیطی گرفته میشه
bot = telebot.TeleBot(TOKEN)

# فایل ذخیره‌سازی داده‌ها (عضویت و فیدبک)
DATA_FILE = "data.json"

# بارگذاری داده‌ها از فایل
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"members": {}, "feedback": []}

# ذخیره داده‌ها در فایل
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# خوش‌آمدگویی و ثبت کاربر جدید
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name or "دوست"
    if user_id not in data["members"]:
        data["members"][user_id] = {
            "name": user_name,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_data(data)
    bot.reply_to(message, f"سلام {user_name}! من ایجنت باشگاه‌تم. هر کمکی خواستی بگو 😎💪")

# دستور کپشن برای کمک به تولید محتوا
@bot.message_handler(commands=['کپشن'])
def caption_handler(message):
    topic = message.text.replace("/کپشن", "").strip()
    if not topic:
        bot.reply_to(message, "بگو موضوع کپشن چیه؟ مثلا: /کپشن تمرین")
        return
    captions = [
        f"با انرژی و تمرکز، امروز رو بساز! 💥 #باشگاه #{topic}",
        f"هر قطره عرق، قدمی به سمت موفقیتِ {topic} 🏋️‍♂️🔥",
        f"بدن قوی = ذهن قوی! امروز رو از دست نده! #{topic} #فیتنس"
    ]
    import random
    bot.reply_to(message, random.choice(captions))

# دستور هشتگ برای کپشن‌ها
@bot.message_handler(commands=['هشتگ'])
def hashtags_handler(message):
    topic = message.text.replace("/هشتگ", "").strip() or "بدنسازی"
    tags = f"#بدنسازی #{topic} #فیتنس #باشگاه #تغذیه #پروگرشن"
    bot.reply_to(message, tags)

# پیشنهاد تمرین روزانه
@bot.message_handler(commands=['پیشنهاد'])
def suggestion_handler(message):
    suggestions = [
        "امروز یه تمرین کامل برای زیربغل انجام بده! نکته: فرم حرکت رو رعایت کن 🎯",
        "پیشنهاد امروز: ۳۰ دقیقه دویدن سبک بعد تمرین 🚀",
        "تمرین با وزنه‌های آزاد، عضلاتت رو قوی‌تر می‌کنه 💪",
        "یادت باشه استراحت کافی هم جزو برنامه‌ت باشه 😉"
    ]
    import random
    bot.reply_to(message, random.choice(suggestions))

# دریافت سوال از کاربر و پاسخ صمیمی
@bot.message_handler(commands=['سوال'])
def question_handler(message):
    question = message.text.replace("/سوال", "").strip()
    if not question:
        bot.reply_to(message, "سوالت رو بعد از /سوال بنویس لطفا 😊")
        return
    answers = [
        f"سوال خوبیه درباره «{question}». معمولاً باید به تغذیه و تمرینات دقت کنی. اگه دوست داشتی دقیق‌تر راهنمایی می‌کنم!",
        f"برای «{question}»، پیشنهاد می‌کنم حتماً با مربی‌هات مشورت کنی و برنامه دقیق داشته باشی.",
        f"سوالت عالی بود! من اینجا هستم که کمکت کنم تو مسیر فیتنس."
    ]
    import random
    bot.reply_to(message, random.choice(answers))

# دریافت فیدبک (بازخورد) از کاربران
@bot.message_handler(commands=['فیدبک'])
def feedback_handler(message):
    feedback = message.text.replace("/فیدبک", "").strip()
    if not feedback:
        bot.reply_to(message, "لطفاً بعد از دستور /فیدبک نظر یا پیشنهادت رو بنویس.")
        return
    user_id = str(message.from_user.id)
    data["feedback"].append({
        "user_id": user_id,
        "text": feedback,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(data)
    bot.reply_to(message, "ممنون که فیدبک دادی! نظرت خیلی برامون مهمه 😊")

# دستور وضعیت عضویت
@bot.message_handler(commands=['وضعیت'])
def status_handler(message):
    user_id = str(message.from_user.id)
    if user_id in data["members"]:
        join_date = data["members"][user_id]["join_date"]
        bot.reply_to(message, f"تو از {join_date} عضو این باشگاه هستی 💪")
    else:
        bot.reply_to(message, "فعلاً عضو نیستی، لطفاً /start رو بزن تا ثبت‌نام کنی.")

mhdy, [07.07.25 13:57]
# مدیریت پیام‌های غیر دستوری (متن معمولی)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    greetings = ["سلام", "درود", "خوبی", "چطوری"]
    if any(greet in text for greet in greetings):
        bot.reply_to(message, "سلام رفیق! چطور می‌تونم کمکت کنم؟ 💪")
    else:
        bot.reply_to(message, "معذرت، این دستور رو نمی‌فهمم 😕. از دستورهای زیر استفاده کن:\n"
                             "/کپشن\n/هشتگ\n/پیشنهاد\n/سوال\n/فیدبک\n/وضعیت")

# اجرای ربات به صورت دائم
bot.infinity_polling()
