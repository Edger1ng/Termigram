from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
import os

from functions import json_functions as json_f
from functions import lock as lock_utils

settings = json_f.load(json_f.SETTINGS_FILE)

async def lock(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    if "LOCK" in settings.get("FUNCTIONS_DISABLED", []):
        await callback.answer("This function is disabled", show_alert=True)
        return
    else:
        text = (
            'Are you sure you want to lock the system?\n'
            'This action will lock the screen.\n'
            'Please confirm by clicking the button below.'
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Lock", callback_data="lock_confirm")],
            [types.InlineKeyboardButton(text="Back to Menu", callback_data="system_control")]
        ])
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        
async def lock_confirm(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    if "LOCK" in settings.get("FUNCTIONS_DISABLED", []):
        await callback.answer("This function is disabled", show_alert=True)
        return
    else:
        text = f'Locking the system, {user_name}...'
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Back to Menu", callback_data="system_control")]
        ])
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        
        success, message, cmd = lock_utils.lock_screen()
        if success:
            os.system(cmd)
        else:
            await callback.message.edit_text(message)