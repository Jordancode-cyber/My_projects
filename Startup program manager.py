import winreg

def list_startup_programs():
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ) as key:
            print("Startup Programs:")
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    print(f"{name}: {value}")
                    i += 1
                except OSError:
                    break
    except Exception as e:
        print(f"Error accessing registry: {e}")

def modify_startup_program(name, action, path=None):
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_ALL_ACCESS) as key:
            if action == "add" and path:
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
                print(f"Added {name} to startup.")
            elif action == "remove":
                winreg.DeleteValue(key, name)
                print(f"Removed {name} from startup.")
    except Exception as e:
        print(f"Error modifying startup programs: {e}")

print("1. List startup programs\n2. Add program to startup\n3. Remove program from startup")
choice = input("Enter your choice: ")

if choice == "1":
    list_startup_programs()
elif choice == "2":
    name = input("Enter program name: ")
    path = input("Enter program path: ")
    modify_startup_program(name, "add", path)
elif choice == "3":
    name = input("Enter program name to remove: ")
    modify_startup_program(name, "remove")
else:
    print("Invalid choice.")