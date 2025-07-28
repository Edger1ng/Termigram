import subprocess
import threading
from helper.get_system import get_system_info
from functions import json_functions as json_f

settings = json_f.load(json_f.SETTINGS_FILE)


install_lock = threading.Lock()

def install_app(app_name: str):
    system_info = get_system_info()
    if system_info['system'] != 'Linux':
        return {"Type": 1, "Message": "This function is only for Linux systems."}

    distro = system_info.get('base', '').lower()
    sudo_user = settings.get("SUDO_USER")
    sudo_pass = settings.get("SUDO_PASSWORD")

    if not sudo_user or not sudo_pass:
        return {"Type": 1, "Message": "Missing SUDO_USER or SUDO_PASSWORD in settings."}

    commands = []

    if 'ubuntu' in distro or 'debian' in distro:
        commands = [
            ['sudo', '-S', 'apt', 'update', '-y'],
            ['sudo', '-S', 'apt', 'install', app_name, '-y']
        ]
    elif 'arch' in distro:
        commands = [
            ['sudo', '-S', 'pacman', '-Sy', '--noconfirm', app_name]
        ]
    elif 'fedora' in distro or 'centos' in distro or 'rhel' in distro:
        commands = [
            ['sudo', '-S', 'dnf', 'install', '-y', app_name]
        ]
    else:
        return {"Type": 1, "Message": "Unsupported Linux distribution."}

    with install_lock:
        for cmd in commands:
            try:
                print(f"Running: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    input=f"{sudo_pass}\n",
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error while running {' '.join(cmd)}:\n{e.stderr}")
                return {"Type": 1, "Message": f"Error: {e.stderr.strip()}"}

    return {"Type": 0, "Message": f"App '{app_name}' installed successfully."}


def remove_app(app_name: str):
    system_info = get_system_info()
    if system_info['system'] != 'Linux':
        return {"Type": 1, "Message": "This function is only for Linux systems."}

    distro = system_info.get('base', '').lower()
    sudo_user = settings.get("SUDO_USER")
    sudo_pass = settings.get("SUDO_PASSWORD")

    if not sudo_user or not sudo_pass:
        return {"Type": 1, "Message": "Missing SUDO_USER or SUDO_PASSWORD in settings."}

    commands = []

    if 'ubuntu' in distro or 'debian' in distro:
        commands = [
            ['sudo', '-S', 'apt', 'remove', app_name, '-y']
        ]
    elif 'arch' in distro:
        commands = [
            ['sudo', '-S', 'pacman', '-Rns', app_name, '--noconfirm']
        ]
    elif 'fedora' in distro or 'centos' in distro or 'rhel' in distro:
        commands = [
            ['sudo', '-S', 'dnf', 'remove', '-y', app_name]
        ]
    else:
        return {"Type": 1, "Message": "Unsupported Linux distribution."}

    with install_lock:
        for cmd in commands:
            try:
                print(f"Running: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    input=f"{sudo_pass}\n",
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error while running {' '.join(cmd)}:\n{e.stderr}")
                return {"Type": 1, "Message": f"Error: {e.stderr.strip()}"}

    return {"Type": 0, "Message": f"App '{app_name}' removed successfully."}

def update_system():
    system_info = get_system_info()
    if system_info['system'] != 'Linux':
        return {"Type": 1, "Message": "This function is only for Linux systems."}

    distro = system_info.get('base', '').lower()
    sudo_user = settings.get("SUDO_USER")
    sudo_pass = settings.get("SUDO_PASSWORD")

    if not sudo_user or not sudo_pass:
        return {"Type": 1, "Message": "Missing SUDO_USER or SUDO_PASSWORD in settings."}

    commands = []

    if 'ubuntu' in distro or 'debian' in distro:
        commands = [
            ['sudo', '-S', 'apt', 'update', '-y'],
            ['sudo', '-S', 'apt', 'upgrade', '-y']
        ]
    elif 'arch' in distro:
        commands = [
            ['sudo', '-S', 'pacman', '-Syu', '--noconfirm']
        ]
    elif 'fedora' in distro or 'centos' in distro or 'rhel' in distro:
        commands = [
            ['sudo', '-S', 'dnf', 'upgrade', '-y']
        ]
    else:
        return {"Type": 1, "Message": "Unsupported Linux distribution."}

    with install_lock:
        for cmd in commands:
            try:
                print(f"Running: {' '.join(cmd)}")
                result = subprocess.run(
                    cmd,
                    input=f"{sudo_pass}\n",
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error while running {' '.join(cmd)}:\n{e.stderr}")
                return {"Type": 1, "Message": f"Error: {e.stderr.strip()}"}

    return {"Type": 0, "Message": "System updated successfully."}