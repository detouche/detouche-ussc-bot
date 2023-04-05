import aiogram
import asyncio
from aiogram import Bot, Router

from config_data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
rt = Router()
