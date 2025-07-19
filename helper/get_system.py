import platform
import os

def get_system_info():
    system = platform.system()
    if system == "Linux":
        distro = "Unknown"
        base = "Unknown"
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            distro = line.strip().split("=")[1].strip('"')
                        elif line.startswith("ID_LIKE="):
                            base = line.strip().split("=")[1].strip('"')
            return {"system": "Linux", "distro": distro, "base": base}
        except Exception:
            return {"system": "Linux", "distro": distro, "base": base}
    elif system == "Windows":
        return {"system": "Windows", "distro": None, "base": None}
    elif system == "Darwin":
        return {"system": "macOS", "distro": None, "base": None}
    else:
        return {"system": system, "distro": None, "base": None}


