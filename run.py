import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
from dotenv import load_dotenv

# загружаю api
load_dotenv()

tg_token_bot = os.getenv("TG_BOT_TOKEN")
open_weather_token = os.getenv("OPEN_WEATHER_TOKEN")

# Инициализация бота
bot = Bot(token=tg_token_bot)
dp = Dispatcher()


# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Отправь мне геолокацию 📍 (через скрепку), и я покажу погоду!"
    )

    # Ставим реакцию на первое сообщение
    try:
        await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji="❤️")]
        )
    except Exception as e:
        print("Ошибка при установке реакции:", e)


# Получение погоды по гео
@dp.message(F.location)
async def get_weather_by_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={open_weather_token}&units=metric&lang=ru"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("main"):
            city = data.get("name", "Неизвестное место")
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_report = (
                f"📍 Город: {city}\n"
                f"🌡 Температура: {temp}°C\n"
                f"☁️ Описание: {description}\n"
                f"💧 Влажность: {humidity}%\n"
                f"💨 Ветер: {wind_speed} м/с"
            )

            await message.answer(weather_report)

            # Ставим реакцию на сообщение с гео
            try:
                await bot.set_message_reaction(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reaction=[ReactionTypeEmoji(emoji="❤️")]
                )
            except Exception as e:
                print("Ошибка при установке реакции:", e)

        else:
            await message.answer("Не удалось получить данные о погоде 😔")

    except Exception as e:
        await message.answer("Ошибка при запросе к OpenWeather 😔")
        print("Ошибка:", e)


# Ответ на простой текст
@dp.message()
async def handle_text(message: Message):
    await message.answer("Отправь геолокацию 📍, чтобы я показал погоду!")

    # Ставим реакцию на текстовое сообщение
    try:
        await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji="❤️")]
        )
    except Exception as e:
        print("Ошибка при установке реакции:", e)


#  Бот запущен ✅, если появился в терминале то бот работает
async def main():
    print("Бот запущен ✅")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())