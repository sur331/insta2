import os
import time
import random
import logging
import threading
from flask import Flask
import telebot
from instagrapi import Client

# =========================================================
# 1. إعداد السجلات (Logging)
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =========================================================
# 2. إبقاء الخدمة نشطة (Keep-Alive) عبر Flask
# =========================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# =========================================================
# 3. الإعدادات وقائمة 20 كوكيز
# =========================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8556998525:AAFkzISMieqBY9sd4tzQgiIbr8PIgz5qXOw")

# ضع الـ 20 Session ID الخاصة بحساباتك هنا
INSTAGRAM_COOKIES = [
    "59117481775%3AC9L5vYxvafAd5b%3A15%3AAYgjks9wps0rP1Sxij_cZB-gb4A1mh9QvoGCKAxSYQ",
    "58901959845%3A7NQgFE7K6PmmtN%3A2%3AAYgh4JEYV9okgjZlF1giGB8Y37dhYGTtepjqsiK9FQ",
    "58870362793%3ArVglTZ8gRbl9Ds%3A20%3AAYiuhBkRspenB-4PRfEz9hnNn7xaqDBoqRTNqTMCRQ",
    "58495258251%3Axjok4RizMTsxyG%3A13%3AAYhgezjrGW1xTjN03kfMoh4DGnsRSncSWycOQwPNJg",
    "57371951936%3AkOQBfe3Jj7hLLo%3A24%3AAYgd7hNTWe1F4WWK15hrN4_k-xzSfycDCgXnDjwlig",
    "59055986186%3AEc8A1EVc6npEZU%3A9%3AAYgkKtexAfRbSqSnsUNtzfzwg4rqCl8vpGibcf3azQ",
    "59186075359%3AcXLQGisI8y0nUi%3A19%3AAYgS2uPg9eol2i75BZ8ER1CWrVVVM_kW8oBUJ_6K8w",
    "52291323880%3AZyZcxPmG9JS4lf%3A1%3AAYhcHg3G2C7Gy4m3GMDTcVE2wf94YfL1KWDz0UM79g",
    "55602778175%3AxKE3NQ4hnh76Ai%3A23%3AAYgDCY1phIdlNEENTgwxAMh6ZK0vuQvRjuUyv8VqhA",
    "58734756583%3AmioPMHLioNzH34%3A26%3AAYjYUGwKRDEXylTsi3b0cMt329DHMg7MgEP_HjReEQ",
    "55384263881%3AY2cnQo9E8Bz5w3%3A0%3AAYhTCm5oDwgIF_EWOmKGXoT_STKSFyWCKPjDQ64hpA",
    "62474799307%3AgXqedqZhirIvb8%3A8%3AAYhkDWwvpUC3vuwuv-95xVODjF91lmbr6SN9yuTe4Q",
    "58980543304%3AUMo1MUChxT3aM9%3A8%3AAYh_lfx7C92uiagJXt_aoERbD3tXW-IqZa6jS9y-Aw",
    "52253063695%3AZaUARdLN8Uerur%3A24%3AAYg_Li09aBQU_PmYFtBVYpT8qFmxAZtJmpCZz6gpvA",
    "58770039263%3AERGX17SOPLPm4i%3A2%3AAYghoXuCTU8EOd9uJxNQz_NiwdYxFv-5Q8ogcyppTQ",
    "59594625485%3AY1TcokusalPWDh%3A24%3AAYhtVeveyjmvH_25r91eR06TT4vP5pajlxqfmeLghg",
    "62250205211%3AXheYMeUnTRAfOi%3A16%3AAYgkpF1CiowVjeRsZxlK4lSXTzD2EojbYvGrRDr1uA",
    "59067830986%3AwIoKGLe6C8WYKl%3A15%3AAYgVCQKmq6D-vBBAGq_0HPC2IBvhD7QrMsSis6vsLg",
    "59006966797%3AbjE3d3PFru0HGL%3A1%3AAYi0hQZaakFtp29xLsht32y1D9KzZmznXllPW6EDQQ",
    "59203191043%3AHI41qxSIK25Ckd%3A4%3AAYiKhHZnmwxrSdJWWL45859UAbZjWWySvA3UamSyog",
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# =========================================================
# 4. دوال التعامل مع إنستغرام
# =========================================================
def get_instagram_client(session_id):
    cl = Client()
    try:
        cl.login_by_sessionid(session_id)
        return cl
    except Exception as e:
        logger.error(f"فشل الجلسة {session_id[:8]}... : {e}")
        return None

def extract_media_id(url):
    try:
        cl = Client()
        return cl.media_pk_from_url(url)
    except Exception as e:
        logger.error(f"خطأ استخراج المعرف: {e}")
        return None

def send_likes_job(post_url, chat_id):
    media_id = extract_media_id(post_url)
    if not media_id:
        bot.send_message(chat_id, "❌ متعذر جلب المنشور، تأكد أن الرابط صحيح والحساب عام.")
        return

    total_accounts = len(INSTAGRAM_COOKIES)
    bot.send_message(
        chat_id, 
        f"🚀 **بدء العملية:**\n- عدد الحسابات: {total_accounts}\n- الفاصل الزمني: 15-30 ثانية عشوائي بين كل حساب."
    )

    success_count = 0
    fail_count = 0

    for idx, session_id in enumerate(INSTAGRAM_COOKIES, 1):
        cl = get_instagram_client(session_id)
        
        if cl:
            try:
                cl.media_like(media_id)
                success_count += 1
                logger.info(f"[{idx}/{total_accounts}] تم الإعجاب بنجاح.")
            except Exception as e:
                fail_count += 1
                logger.error(f"[{idx}/{total_accounts}] فشل الإعجاب: {e}")
        else:
            fail_count += 1

        # فاصل زمني بين الحسابات لتفادي الحظر
        if idx < total_accounts:
            delay = random.randint(15, 30)
            logger.info(f"انتظار {delay} ثانية...")
            time.sleep(delay)

    report = (
        f"🏁 **انتهت العملية!**\n\n"
        f"👍 إعجابات ناجحة: {success_count}\n"
        f"❌ إعجابات فاشلة: {fail_count}\n"
        f"📊 الإجمالي: {total_accounts}"
    )
    bot.send_message(chat_id, report, parse_mode="Markdown")

# =========================================================
# 5. أوامر البوت
# =========================================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل رابط المنشور لعمل الإعجابات عبر الـ 20 حساباً.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if "instagram.com" in url:
        bot.reply_to(message, "⏳ جاري بدء تنفيذ الإعجابات...")
        threading.Thread(target=send_likes_job, args=(url, message.chat.id)).start()
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط إنستغرام صحيح.")

# =========================================================
# 6. تشغيل البوت
# =========================================================
if __name__ == "__main__":
    logger.info("تم تشغيل البوت...")
    bot.infinity_polling()
