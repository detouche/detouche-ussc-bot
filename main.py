from loader import bot, rt
import handlers  # noqa
import asyncio

from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_default_commands():
    bot_commands = [
        BotCommand(command="/start", description="Главное меню")
    ]
    await bot.set_my_commands(bot_commands)


async def main():
    dp = Dispatcher()
    dp.include_router(rt)
    dp.startup.register(set_default_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
