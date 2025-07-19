from aiogram import Bot, Dispatcher, F, types
import asyncio
from aiogram.types import Message

from functions import json_functions as json_f
from commands.start import cmd_start
from functions.admin_verify import verify_admin_code
from commands import panel

settings = json_f.load(json_f.SETTINGS_FILE)

if not settings.get("BOT_TOKEN"):
    print("Bot token is not set. Please set it in settings.json or enter it now:")
    token = input("Enter your bot token: ").strip()
    if token:
        settings["BOT_TOKEN"] = token
        json_f.save(settings)
        print("Bot token saved successfully.Reload bot to apply changes.")
        exit(1)

bot = Bot(token=settings["BOT_TOKEN"])
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

async def main():
    if settings.get("DEBUG"):
        print("Bot is starting with DEBUG mode enabled")
    else:
        print("Bot is starting in production mode")


    if settings.get("FIRST_START"):
        print("This is the first start of the bot. If you did not set the bot token, please do so in settings.json.")
        print("Follow the instructions on the screen OR in Readme.md to setup me")


        if not settings.get("ADMIN_IDS"):
            text = (
                "========\n"
                "Hi! I am very happy to see you here.\n"
                "To gain access to admin panel id, you need to go to chat with me and click 'start' button.\n"
                "After that, you will be able to use admin panel.\n"
                "I would be waiting for you in chat.\n"
                "========"
            )
            print(text)
            settings["WAITING_FOR_ADMIN_IDS"] = True
            json_f.save(settings)
        else:
            print("Admin IDs are already set. Proceeding with bot startup.")

        settings["FIRST_START"] = False
        json_f.save(settings)
    else:
        print("Bot is already set up. Proceeding with normal startup.")
        print("You can change settings in settings.json file.")
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())