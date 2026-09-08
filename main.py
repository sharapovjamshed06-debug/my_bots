import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# Токени боти худро дар байни нохунакҳо гузоред
TOKEN = "6482109417:AAGdKMqojdNSFqXLYOWjQeBVMwaYwbTP1JQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"Салом, {message.from_user.full_name}! Бот 24/7 фаъол аст."
    )


@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Шумо навиштед: {message.text}")


async def handle_health(request):
    return web.Response(text="Bot is running!")


async def main():
    logging.basicConfig(level=logging.INFO)

    # Веб-сервери хурд барои он ки Render ботро хомӯш накунад
    app = web.Application()
    app.router.add_get("/", handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    # Оғози коркарди паёмҳои бот
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
