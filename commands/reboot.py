from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
import os

from functions import json_functions as json_f

settings = json_f.load(json_f.SETTINGS_FILE)

async def cmd_reboot_main(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    if "REBT" in settings.get("FUNCTIONS_DISABLED", []):
        await callback.answer("This function is disabled", show_alert=True)
        return
    else:
        text = (
            'Are you sure you want to reboot the system?\n'
            'This action will restart the bot and the system.\n'
            'Please confirm by clicking the button below.'
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Reboot", callback_data="reboot_confirm")],
            [types.InlineKeyboardButton(text="Back to Menu", callback_data="system_control")]
        ])
        await callback.message.edit_text(text=text, reply_markup=keyboard)

async def cmd_reboot_confirm(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    if "REBT" in settings.get("FUNCTIONS_DISABLED", []):
        await callback.answer("This function is disabled", show_alert=True)
        return
    else:
        text = f'Bye, {user_name}!\nThe system is rebooting...'
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Back to Menu", callback_data="system_control")]
        ])
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        sudo_user = settings.get("SUDO_USER")
        sudo_password = settings.get("SUDO_PASSWORD")
        if sudo_user and sudo_password:
            os.system(f"echo '{sudo_password}' | sudo -u {sudo_user} -S reboot")
        else:
            os.system("sudo reboot")