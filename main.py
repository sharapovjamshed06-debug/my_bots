import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web
from google import genai

BOT_TOKEN = "6482109417:AAGdKMqojdNSFqXLYOWjQeBVMwaYwbTP1JQ"
GEMINI_API_KEY = "AQ.Ab8RN6Kq-x2X_GRtGKAoUgE19n_ca8aNImwJFiq_17TSA4uovA"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Салом! Ман боти интеллектуалӣ бо Google Gemini ҳастам. Ба ман савол диҳед!")

@dp.message()
async def ai_handler(message: types.Message):
    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("Хатогӣ ҳангоми коркарди савол рӯй дод.")

async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
