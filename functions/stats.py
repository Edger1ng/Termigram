import psutil
import datetime

def build_resource_stats_message():
    cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    net = psutil.net_io_counters()
    boot_time = psutil.boot_time()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)

    message = (
        "📊 *Resource Statistics*\n\n"
        f"*Uptime:* `{str(uptime).split('.')[0]}`\n\n"
        "🖥 *CPU*\n"
        f"- *Total cores:* {psutil.cpu_count(logical=True)} (physical: {psutil.cpu_count(logical=False)})\n"
        f"- *Frequency:* `{cpu_freq.current:.1f} MHz` (min: `{cpu_freq.min:.1f}`, max: `{cpu_freq.max:.1f}`)\n"
        f"- *Per-core usage:*\n"
    )
    for i, percent in enumerate(cpu_percents):
        message += f"    └ Core {i+1}: `{percent}%`\n"
    message += (
        "\n"
        "💾 *RAM*\n"
        f"- *Used:* `{mem.used // (1024*1024)} MB` / `{mem.total // (1024*1024)} MB` ({mem.percent}%)\n"
        f"- *Available:* `{mem.available // (1024*1024)} MB`\n"
        f"- *Swap:* `{swap.used // (1024*1024)} MB` / `{swap.total // (1024*1024)} MB` ({swap.percent}%)\n\n"
        "🗄 *Disk*\n"
        f"- *Used:* `{disk.used // (1024*1024*1024)} GB` / `{disk.total // (1024*1024*1024)} GB` ({disk.percent}%)\n"
        f"- *Read:* `{disk_io.read_bytes // (1024*1024)} MB`\n"
        f"- *Write:* `{disk_io.write_bytes // (1024*1024)} MB`\n\n"
        "🌐 *Network*\n"
        f"- *Sent:* `{net.bytes_sent // (1024*1024)} MB`\n"
        f"- *Received:* `{net.bytes_recv // (1024*1024)} MB`\n"
    )

    return message
