import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

# Токени боти Telegram ва калиди тозаи Gemini
BOT_TOKEN = "6482109417:AAGdKMqojdNSFqXLYOWjQeBVMwaYwbTP1JQ"
GEMINI_API_KEY = "AQ.Ab8RN6Kq-x2X_GRtGKAoUgEi9n_ca8aNImwJFiq_17TSA4uovA"

# Танзими Gemini API
ai_client = genai.Client(api_key=GEMINI_API_KEY)

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
  await message.answer(
      "Салом! Ман боти интеллектуақӣ бо Google Gemini ҳастам. Ба ман савол диҳед!"
  )


@dp.message()
async def chat_handler(message: types.Message):
  try:
    processing_msg = await message.answer("⏳ Дар ҳоли коркарди савол...")

    # Дархост ба модели gemini-2.5-flash
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message.text,
    )

    await processing_msg.delete()
    await message.answer(response.text)
  except Exception as e:
    logging.error(f"Хатогӣ: {e}")
    await message.answer("Хатогӣ ҳангоми коркарди савол рӯй дод.")


async def main():
  bot = Bot(token=BOT_TOKEN)
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
