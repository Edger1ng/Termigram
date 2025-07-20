from aiogram import Bot, Dispatcher, F, types
import asyncio
from aiogram.types import Message
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from functions import json_functions as json_f
from commands.start import cmd_start
from functions.admin_verify import verify_admin_code
from commands import panel, stats
from functions import start as strt
from functions import arg_parse



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
dp = Dispatcher()


@dp.message(F.text == "/start")
async def handle_start(message: Message):
    await cmd_start(message)


@dp.callback_query(F.data.startswith("admin_code_"))
async def handle_admin_code(callback: types.CallbackQuery):
    await verify_admin_code(callback)


@dp.message(F.text == "panel")
async def handle_panel(message: Message):
    await panel.callback_query_menu(message)


@dp.callback_query(F.data == "system_control")
async def handle_system_control(callback: types.CallbackQuery):
    await panel.callback_query_system_control(callback)


@dp.callback_query(F.data == "file_system")
async def handle_file_system(callback: types.CallbackQuery):
    await panel.callback_query_file_system(callback)


@dp.callback_query(F.data == "app_manage")
async def handle_app_manage(callback: types.CallbackQuery):
    await panel.callback_query_app_manage(callback)


@dp.callback_query(F.data == "network")
async def handle_network(callback: types.CallbackQuery):
    await panel.callback_query_network(callback)


@dp.callback_query(F.data == "users")
async def handle_users(callback: types.CallbackQuery):
    await panel.callback_query_users(callback)


@dp.callback_query(F.data == "settings")
async def handle_settings(callback: types.CallbackQuery):
    await panel.callback_query_settings(callback)


@dp.callback_query(F.data == "back")
async def handle_back(callback: types.CallbackQuery):
    await panel.callback_query_menu(callback)

@dp.callback_query(F.data == "stats_control")
async def handle_stats_control(callback: types.CallbackQuery):
    await stats.cmd_stats(callback)


async def main_f():
    strt.main_f()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main_f())
