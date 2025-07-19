from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functions import json_functions as json_f
from helper import random_digits
import random

settings = json_f.load(json_f.SETTINGS_FILE)
pending_codes = {} 


async def cmd_start(message: Message):
    if settings.get("WAITING_FOR_ADMIN_IDS") or not settings.get("ADMIN_IDS"):
        if message.from_user.id not in settings["ADMIN_IDS"]:
            code = random_digits.generate_random_code(6)
            fake_codes = [random_digits.generate_fake_code(6) for _ in range(4)]
            all_codes = [code] + fake_codes
            random.shuffle(all_codes)

            pending_codes[message.from_user.id] = code  

            text = (
                '========\n'
                'Hi again! I received a request to add a person as an admin.\n'
                'To gain access to the admin panel, you need to enter the code that I will show you.\n'
                'You need to choose the correct code from the buttons below.\n'
                'Please, be careful, because if you choose the wrong code, you will not be able to access the admin panel.\n'
                '\n'
                'Here is the code:\n'
                f'{code}\n'
                '========'
            )
            print(text)

            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text=c, callback_data=f"admin_code_{c}")]
                    for c in all_codes
                ]
            )
            await message.answer("The code has been shown in the console. Choose the correct one below:", reply_markup=keyboard)
        else:
            await message.answer("You are already an admin.")
    else:
        await message.answer("Admin IDs are already set. No action needed.\nIf you want to go to admin panel you need to type ’panel’")