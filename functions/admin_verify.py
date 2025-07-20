from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from functions import json_functions as json_f
from commands.start import pending_codes
from helper import random_digits
import random

settings = json_f.load(json_f.SETTINGS_FILE)

async def verify_admin_code(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data.removeprefix("admin_code_")  # Python 3.9+

    correct_code = pending_codes.get(user_id)

    if not correct_code:
        await callback.answer("No code was generated for you!", show_alert=True)
        return

    if data == correct_code:
        if "ADMIN_IDS" not in settings:
            settings["ADMIN_IDS"] = []
        if user_id not in settings["ADMIN_IDS"]:
            settings["ADMIN_IDS"].append(user_id)
            settings["WAITING_FOR_ADMIN_IDS"] = False
            settings["FIRST_START"] = False

            json_f.save(settings)

        await callback.message.edit_text("✅ Correct! You are now an admin.")
        await callback.answer("Access granted!", show_alert=True)
    else:
        await callback.message.edit_text("❌ Incorrect code. Access denied.")
        await callback.answer("Wrong code!", show_alert=True)

    pending_codes.pop(user_id, None) 