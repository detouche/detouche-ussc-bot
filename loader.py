from aiogram import Bot, Router

from config_data import config

bot = Bot(token=config.BOT_TOKEN)
rt = Router()
