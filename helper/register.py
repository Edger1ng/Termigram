from aiogram import Dispatcher, F, types
from aiogram.types import Message

from commands.start import cmd_start
from functions.admin_verify import verify_admin_code
from commands import panel, stats, reboot, shutdown, lock

def register_handlers(dp: Dispatcher):
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

    @dp.callback_query(F.data == "system_control_2")
    async def handle_system_control_2(callback: types.CallbackQuery):
        await panel.callback_query_system_control_2(callback)

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

    @dp.callback_query(F.data == "reboot")
    async def handle_reboot(callback: types.CallbackQuery):
        await reboot.cmd_reboot_main(callback)

    @dp.callback_query(F.data == "reboot_confirm")
    async def handle_reboot_confirm(callback: types.CallbackQuery):
        await reboot.cmd_reboot_confirm(callback)

    @dp.callback_query(F.data == "shutodwn")
    async def handle_shutdown(callback: types.CallbackQuery):
        await shutdown.cmd_shutodwn_main(callback)

    @dp.callback_query(F.data == "shutodwn_confirm")
    async def handle_shutdown_confirm(callback: types.CallbackQuery):
        await shutdown.cmd_shutodwn_confirm(callback)

    @dp.callback_query(F.data == "lock")
    async def handle_lock(callback: types.CallbackQuery):
        await lock.lock(callback)

    @dp.callback_query(F.data == "lock_confirm")
    async def handle_lock_confirm(callback: types.CallbackQuery):
        await lock.lock_confirm(callback)
