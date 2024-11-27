import asyncio
import logging
from bot_config import bot, database, dp
from handlers.start import start_router
from handlers.send_dz import send_dz_router


async def on_startup(bot):
    database.create_tables()


async def main():
    dp.include_router(start_router)
    dp.include_router(send_dz_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
