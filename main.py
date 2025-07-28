from aiogram import Bot, Dispatcher, F, types
import asyncio
from aiogram.types import Message
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from functions import json_functions as json_f
from functions import start as strt
from functions import arg_parse
from helper import register

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import StateFilter


settings = json_f.load(json_f.SETTINGS_FILE)
arg_parse.arg_parse(sys.argv)
if arg_parse.override_security_check_wfa:
    print("WFA check override is ON")

if arg_parse.override_security_check_integrity:
    print("Integrity check override is ON")

if not settings.get("BOT_TOKEN"):
    print("Bot token is not set. Please set it in settings.json or enter it now:")
    token = input("Enter your bot token: ").strip()
    if token:
        settings["BOT_TOKEN"] = token
        json_f.save(settings)
        print("Bot token saved successfully.Reload bot to apply changes.")
        exit(1)

bot = Bot(token=settings["BOT_TOKEN"], default=DefaultBotProperties(
    parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

register.register_handlers(dp)

async def main_f():
    strt.main_f()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main_f())
