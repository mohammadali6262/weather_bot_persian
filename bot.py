
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات آب‌وهوام. برای راهنما /help رو بزن.")

async def help(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - شروع\n/help - راهنما\n/weather - وضعیت آب‌وهوا")

async def weather_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("نام شهر رو به فارسی برام بفرست 😊")
    context.user_data['expecting_city'] = True

async def handle_city_name(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('expecting_city'):
        city = update.message.text
        context.user_data['expecting_city'] = False

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&lang=fa&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                await update.message.reply_text("شهری با این نام پیدا نشد ❌")
                return
            name = data['name']
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']

            msg = f"آب‌وهوای {name}:\nدما: {temp}°C\nرطوبت: {humidity}%\nباد: {wind} متر/ثانیه\nوضعیت: {weather}"
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text("خطایی پیش اومد. لطفا دوباره امتحان کن.")
    else:
        await update.message.reply_text("دستور نامعتبره. برای راهنما /help رو بزن.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_name))

    print("ربات روشن است ...")
    app.run_polling()

if __name__ == '__main__':
    main()
