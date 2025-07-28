import platform
import os
import shutil
import platform
if platform.system() == "Windows":
    from ctypes import windll
else:
    windll = None


def is_lock_eligible():
    system = platform.system().lower()
    
    if system == "linux":
        display = os.environ.get('DISPLAY')
        if not display:
            return False, "Linux (No display server)", None
            
        lockers = {
            'xdg-screensaver': 'xdg-screensaver lock',
            'gnome-screensaver-command': 'gnome-screensaver-command -l',
            'light-locker': 'light-locker-command -l',
            'i3lock': 'i3lock',
            'slock': 'slock'
        }
        
        for locker, cmd in lockers.items():
            if shutil.which(locker):
                return True, f"Linux ({locker} available)", cmd
                
        return False, "Linux (No screen locker found)", None
        
    elif system == "windows":
        try:
            return True, "Windows (LockWorkStation available)", windll.user32.LockWorkStation
        except Exception as e:
            return False, f"Windows (API error: {e})", None
            
    return False, f"Unsupported platform: {system}", None
