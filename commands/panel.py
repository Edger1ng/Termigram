from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from functions import json_functions as json_f

settings = json_f.load(json_f.SETTINGS_FILE)

async def callback_query_menu(event):
    if isinstance(event, types.Message):
        user_name = event.from_user.username or "Unknown User"
        send = event.answer  # просто отправляет новое сообщение
        await send(
            f"Hello, {user_name}! Please choose an option from the menu below:",
            reply_markup=get_menu_keyboard()
        )

    elif isinstance(event, types.CallbackQuery):
        user_name = event.from_user.username or "Unknown User"
        message = event.message
        await message.edit_text(
            f"Hello, {user_name}! Please choose an option from the menu below:",
            reply_markup=get_menu_keyboard()
        )
        await event.answer()  # обязательно отвечать на callback, чтобы убрать крутилку

def get_menu_keyboard():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🖥️ System Control", callback_data="system_control")],
        [types.InlineKeyboardButton(text="📁 File System", callback_data="file_system")],
        [types.InlineKeyboardButton(text="📦 App Manage", callback_data="app_manage")],
        [types.InlineKeyboardButton(text="🌐 Network", callback_data="network")],
        [types.InlineKeyboardButton(text="👤 Users", callback_data="users")],
        [types.InlineKeyboardButton(text="⚙️ Settings", callback_data="settings")]
    ])

async def callback_query_system_control(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🖥️ Stats", callback_data="stats_control")],
        [types.InlineKeyboardButton(text="🔄 Reboot", callback_data="reboot")],
        [types.InlineKeyboardButton(text="🔒 Lock", callback_data="lock")],
        [types.InlineKeyboardButton(text="Shutdown", callback_data="shutdown")],
        [types.InlineKeyboardButton(text="Next Page", callback_data="system_control_2")],
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]                                    
        ])
    text = (
        f'Hi, {user_name}!\n'
        'You are now in menu "System Control"\n'
        'Please, choose the action by buttons below'
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    
async def callback_query_system_control_2(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📊 System Info", callback_data="system_info")],
        [types.InlineKeyboardButton(text="🔄 Update System", callback_data="update_system")],
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]
    ])
    text = (
        f'Hi, {user_name}!\n'
        'You are now in menu "System Control - Page 2"\n'
        'Please, choose the action by buttons below'
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    

async def callback_query_file_system(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📂 View Files", callback_data="view_files")],
        [types.InlineKeyboardButton(text="🗑️ Delete File", callback_data="delete_file")],
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]
    ])
    text = (
        f'Hi, {user_name}!\n'
        'You are now in menu "File System"\n'
        'Please, choose the action by buttons below'
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
        
        

async def callback_query_app_manage(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📦 Install App", callback_data="install_app")],
        [types.InlineKeyboardButton(text="🗑️ Uninstall App", callback_data="uninstall_app")],
        [types.InlineKeyboardButton(text="🔄 Update App", callback_data="update_app")],
        [types.InlineKeyboardButton(text="🔄 Update System", callback_data="update_system")],
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]
    ])
    text = (
        f'Hi, {user_name}!\n'
        'You are now in menu "App Manage"\n'
        'Please, choose the action by buttons below'
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    
async def callback_query_network(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🌐 View Network", callback_data="view_network")],
        [types.InlineKeyboardButton(text="🔄 Restart Network", callback_data="restart_network")],
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]
    ])
    text = (
        f'Hi, {user_name}!\n'
        'You are now in menu "Network"\n'
        'Please, choose the action by buttons below'
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)

async def callback_query_users(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="👤 View Users", callback_data="view_users")],
        [types.InlineKeyboardButton(text="➕ Add User", callback_data="add_user")],
        [types.InlineKeyboardButton(text="🗑️ Delete User", callback_data="delete_user")],
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]
    ])
    text = (
        f'Hi, {user_name}!\n'
        'You are now in menu "Users"\n'
        'Please, choose the action by buttons below'
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    
async def callback_query_settings(callback: types.CallbackQuery):
    user_name = callback.from_user.username or "Unknown User"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="⚙️ Change Settings", callback_data="change_settings")],
        [types.InlineKeyboardButton(text="🔄 Reset Settings", callback_data="reset_settings")],
        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]
    ])
    text = (
        f'Hi, {user_name}!\n'
        'You are now in menu "Settings"\n'
        'Please, choose the action by buttons below'
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)