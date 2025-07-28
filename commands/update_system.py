from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from functions import json_functions as json_f
from helper import update


settings = json_f.load(json_f.SETTINGS_FILE)


async def cmd_update_system(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    if "UPDT" in settings.get("FUNCTIONS_DISABLED", []):
        await callback.answer("This function is disabled", show_alert=True)
        return
    else:
        text = (
            f'Hi, {user_name}!\n'
            'The system is being updated.\n'
            'Please wait for the process to complete.'
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Back to Menu", callback_data="system_control")]
        ])
        await callback.message.edit_text(text=text, reply_markup=keyboard)
        update_result = update.update_system()
        update_success, update_message = update_result["Type"], update_result["Message"]
        if update_success:
            await callback.message.edit_text(f'Update successful!\n{update_message}')
        else:
            await callback.message.edit_text(f'Update failed!\n{update_message}')
