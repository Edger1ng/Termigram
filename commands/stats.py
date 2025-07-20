from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from functions import json_functions as json_f
from functions import stats as stts

settings = json_f.load(json_f.SETTINGS_FILE)

async def cmd_stats(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    if "STTS" in settings.get("FUNCTIONS_DISABLED", []):
        await callback.answer("This function is disabled", show_alert=True)
        return
    else:
        stts_data = stts.build_resource_stats_message()
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="system_control")]
    ])
    await callback.message.edit_text(
        text=stts_data,
        reply_markup=keyboard
    )