from loader import bot, rt
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from aiogram import Dispatcher
import asyncio


async def main():
    dp = Dispatcher()
    dp.include_router(rt)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
