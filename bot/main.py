from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config.settings import TOKEN
from handlers.start import router as start_router
from handlers.photo_handler import router as photo_router
from handlers.stats import router as stats_router

import asyncio

if not TOKEN:
    raise ValueError("токен не задан.")

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(start_router)
dp.include_router(photo_router)
dp.include_router(stats_router)

async def main():
    print("бот запущен.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())