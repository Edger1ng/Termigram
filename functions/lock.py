from helper import is_lock_eligible

def lock_screen():
    eligible, message, command = is_lock_eligible.is_lock_eligible()
    
    if not eligible:
        print(f"Locking failed: {message}")
        return False, message
    
    if command:
        print(f"Locking screen using command: {command}")
        import subprocess
        try:
            subprocess.run(command, shell=True)
            return True
        except Exception as e:
            print(f"Error executing lock command: {e}")
            return False, e
    
    print("Locking screen using API call.")
    try:
        command()  
        return True
    except Exception as e:
        print(f"Error locking screen: {e}")
        return False, e