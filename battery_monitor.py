import psutil
import os
import time
import logging
from cryptography.fernet import Fernet
from plyer import notification
from tkinter import Tk, messagebox
import getpass

# ===== Configuration =====
PASSWORD = "iew09325AYVU#€6boqytr8,ay7"
KEY = b'your_saved_key_here'
CIPHER = Fernet(KEY)

# Encrypted configuration values
ENCRYPTED_WARNING_PERCENTAGE = CIPHER.encrypt(b'25')  # Encrypt once and save
ENCRYPTED_SHUTDOWN_PERCENTAGE = CIPHER.encrypt(b'20')

# Logging setup
logging.basicConfig(
    filename="battery_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Notification settings
NOTIFICATION_DURATION = 10
CHECK_INTERVAL = 60
SHUTDOWN_DELAY = 30

# ===== Utility Functions =====
def log_message(message):
    """Log and display a message."""
    logging.info(message)
    print(message)

def authenticate():
    """Prompt the user for a password to authenticate access."""
    entered_password = getpass.getpass("Enter the script password to proceed: ")
    if entered_password != PASSWORD:
        log_message("Unauthorized access attempt.")
        print("Authentication failed. Exiting.")
        exit()

def decrypt_config():
    """Decrypt and retrieve configuration values."""
    warning = int(CIPHER.decrypt(ENCRYPTED_WARNING_PERCENTAGE).decode())
    shutdown = int(CIPHER.decrypt(ENCRYPTED_SHUTDOWN_PERCENTAGE).decode())
    return warning, shutdown

def notify_user(title, message):
    """Display a pop-up notification."""
    notification.notify(
        title=title,
        message=message,
        timeout=NOTIFICATION_DURATION
    )

def confirm_shutdown():
    """Ask the user for shutdown confirmation."""
    root = Tk()
    root.withdraw()  # Hide the main window
    result = messagebox.askyesno(
        "Critical Battery Warning",
        f"Battery critically low. Shutdown will occur in {SHUTDOWN_DELAY} seconds. Do you want to cancel shutdown?"
    )
    root.destroy()
    return result

def shutdown_computer():
    """Perform a system shutdown."""
    notify_user("Shutting down", f"System will shut down in {SHUTDOWN_DELAY} seconds.")
    log_message("System will shut down in 30 seconds.")
    time.sleep(SHUTDOWN_DELAY)
    if os.name == "nt":  # Windows
        os.system("shutdown /s /t 1")
    elif os.name == "posix":  # macOS/Linux
        os.system("shutdown now")

# ===== Main Monitoring Logic =====
def check_battery(warning_percentage, shutdown_percentage):
    """Monitor the battery status and take appropriate action."""
    battery = psutil.sensors_battery()

    if battery is None:
        log_message("Battery status not available.")
        return

    percent = battery.percent
    plugged = battery.power_plugged

    if not plugged:
        if percent <= shutdown_percentage:
            log_message(f"Battery critically low ({percent}%). Attempting to shut down.")
            notify_user("Critical Battery Warning", f"Battery critically low ({percent}%).")
            if not confirm_shutdown():
                shutdown_computer()
            else:
                log_message("Shutdown canceled by user.")
        elif percent <= warning_percentage:
            log_message(f"Warning: Battery low at {percent}%. Please plug in your charger.")
            notify_user("Low Battery Warning", f"Battery is low at {percent}%. Please plug in your charger.")

def main():
    """Main loop to monitor battery status."""
    warning_percentage, shutdown_percentage = decrypt_config()
    while True:
        check_battery(warning_percentage, shutdown_percentage)
        time.sleep(CHECK_INTERVAL)

# ===== Entry Point =====
if __name__ == "__main__":
    authenticate()
    log_message("Script accessed by authorized user.")
    main()