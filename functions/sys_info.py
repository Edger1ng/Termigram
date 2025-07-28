import platform
import psutil
import cpuinfo
import GPUtil
import socket
import os
import shutil

from helper.md_helper import escape_md

def get_system_info() -> str:
    info = []

    info.append(f"*🖥 OS:* {escape_md(platform.system())} {escape_md(platform.release())} ({escape_md(platform.version())})")
    info.append(f"*🔧 Architecture:* {escape_md(' '.join(platform.architecture()))}")
    info.append(f"*📦 Machine:* {escape_md(platform.machine())}")
    info.append(f"*🌐 Hostname:* {escape_md(socket.gethostname())}")

    cpu = cpuinfo.get_cpu_info()
    info.append(f"*🧠 CPU:* {escape_md(cpu.get('brand_raw', 'Unknown'))} ({psutil.cpu_count(logical=False)} cores / {psutil.cpu_count()} threads)")
    info.append(f"*📐 CPU Arch:* {escape_md(cpu.get('arch', 'Unknown'))}")

    ram_total = psutil.virtual_memory().total // (1024 ** 3)
    info.append(f"*💾 RAM:* {ram_total} GB")

    total, _, _ = shutil.disk_usage(os.path.abspath(os.sep))
    info.append(f"*🗄 Disk:* {total // (1024 ** 3)} GB total")

    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                info.append(f"*🎮 GPU {i + 1}:* {escape_md(gpu.name)} ({escape_md(gpu.driver)})")
        else:
            info.append("*🎮 GPU:* Not detected")
    except Exception as e:
        info.append(f"*🎮 GPU:* Error - {escape_md(e)}")

    return '\n'.join(info)
