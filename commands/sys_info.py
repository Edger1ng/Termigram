from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from functions import json_functions as json_f
from functions.sys_info import get_system_info

settings = json_f.load(json_f.SETTINGS_FILE)

async def cmd_sys_info(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    if "SYSI" in settings.get("FUNCTIONS_DISABLED", []):
        await callback.answer("This function is disabled", show_alert=True)
        return
    else:
        system_info = get_system_info()
        
        text = (
            f'Hi, {user_name}!\n'
            'Here is the system information:\n\n'
            f'{system_info}'
        )
        
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Back to Menu", callback_data="system_control")]
        ])
        
        await callback.message.edit_text(text=text, reply_markup=keyboard)