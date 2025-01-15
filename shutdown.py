import psutil
import os
import time
import logging
import getpass
from cryptography.fernet import Fernet
from plyer import notification
from tkinter import Tk, messagebox

#Securing access to shutdown script to user only
#Secure key and encrypted configuration
key = b'your_saved_key_here'
cipher = Fernet(key)

encrypted_Warning_percentage = cipher.encyrpt(b'25')  #Run once and save encrypted values
encrypted_Shutdown_percentage = cipher.encyrpt(b'20')

#Password for access
PASSWORD = "your_secure_password"

#Logging setup
logging.basicConfig(
    filename = "access.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

#========FUNCTIONS===========
def log_access(message):
    """Log access or modification attempts."""
    logging.info(message)
    print(message)

def authenticate():
    """
    Prompt the user for a password to authenticate access.
    """
    entered_password = getpass.getpass("Enter the script password to proceed: ")
    if entered_password != PASSWORD:
        log_access("Unauthorized access attempt.")
        print("Authentication failed. Exiting.")
        exit()

def decrypt_config():
    """
    Decrypt the configuration.
    """
    warning = int(cipher.decrypt(encrypted_Warning_percentage).decode())
    shutdown = int(cipher.decrypt(encrypted_Shutdown_percentage).decode())
    return warning, shutdown

def notify_user(title, message):
    """
    Show a pop-up notification.
    """
    notification.notify(title=title, message=message, timeout=10)

def shutdown_computer():
    """Shut down the system."""
    notify_user("Shutting Down", "System will shut down in 30 seconds.")
    time.sleep(30)
    if os.name == "nt":
        os.system("shutdown /s /t 1")
    elif os.name == "posix":
        os.system("shutdown now")

# ===== MAIN FUNCTION =====
def main():
    """Main battery monitor loop."""
    WARNING_PERCENTAGE, SHUTDOWN_PERCENTAGE = decrypt_config()
    while True:
        battery = psutil.sensors_battery()
        if battery and not battery.power_plugged:
            if battery.percent <= SHUTDOWN_PERCENTAGE:
                log_access("Critical battery level. Shutting down.")
                shutdown_computer()
            elif battery.percent <= WARNING_PERCENTAGE:
                notify_user("Low Battery", f"Battery at {battery.percent}%. Please charge.")
        time.sleep(60)

# ===== ENTRY POINT =====
if __name__ == "__main__":
    authenticate()  # Require authentication to start
    log_access("Script accessed by authorized user.")
    main()

#Configuration
#Battery script
#Battery Thresholds
Warning_percentage = 25 # Notifies the user when the battery reaches this percentage
Shutdown_percentage = 20 # Shutsdown the pc at this percentage

#Notification and delay of settings
Notification_duration = 10 # How long the notification stays visible 
Check_interval = 60 # Seconds between each battery check
Shutdown_delay = 30 # Seconds before shutdown after critical warning

#Warning
Warned = False # Tracks if a warning has already been issued or passed
Shutdown_canceled = False # Tracks if shutdown has been cancled by the user

#Logging
# Keeps track of all activities in a file for debugging purposes
logging.basicConfig(
    filename="battery_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_status(message):
    """Log and display a message."""
    logging.info(message)
    print(message)
# Prints to the console for real-time feedback

#Notification functionality
def notify_user(title,message):
    """
    Display a pop-up notification to the user.
    - `plyer` ensures cross-platform compatibility.
    """
    notification.notify(
    title = title,
    message = message,
    timeout = Notification_duration
)

#Shutdown confirmation
def confirm_shutdown():
    """
    Display a confirmation dialog to the user asking whether to cancel shutdown
    - `tkinter` ensures the dialog works on all platforms.
    """
    global Shutdown_canceled

    #Initialize tkinter
    root = Tk()
    root.withdraw()    #Hide the main tkinter window

    #Display the confirmation dialog
    result = messagebox.askyesno(
        "Critical Battery Warning",
        f"Battery critcally low. Shutdown will occur in {Shutdown_delay} seconds. Do you want to cancel shutdown?"
    )

    #Handles user's response
    if result:     #User clicked "Yes" to cancel
        Shutdown_canceled = True
        log_status("Shutdown cancelled by the user.")
        notify_user("Shutdown canceled", "Shutdown has been canceles by the user.")
    else:
        log_status("Shutdown confirmed by the user or timeout.")
    root.destroy()   #Destroy the tkinter window

#Shutdown function
def shutdown_computer():
    """
    Perform a system shutdown unless canceled by the user.
    - Allows a  delay for user intervention
    """
    global Shutdown_canceled
    Shutdown_canceled = False   # Reset cancel flag

    # Ask for confirmation to shutdown
    confirm_shutdown()
    # Proceed if the shutdown is not canceled
    if not Shutdown_canceled:
        notify_user("Shutting down", f"Your system will shutdown in {Shutdown_delay} seconds.")
        log_status("Shutting down system in 30 seconds.")
        time.sleep(Shutdown_delay)    # Delay before shutdown

        # Perform shutdown
        if  os.name == "nt":      # Windows
            os.system("shutdown /s /t 1")
        elif os.name == "posix":      # macOS and Linux
            os.system("shutdown now")
    else:
        log_status("Shutdown aborted by user.")

#Battery monitoring
def check_battery():
    """
    Monitor the battery status and take action based on percentage.
    - Sends a warning notification at `Warning_percentage`.
    - Initiates shuytdown at `Shutdown_percentage`.
    """
    global Warned
    battery = psutil.sensors_battery()

    if battery is None:
        log_status("Battery status not available.")
        return
    
    percent = battery.percent
    plugged = battery.power_plugged   #True if device is charging

    # Action when the device is not plugged in and charging
    if not plugged:
        if percent <= Shutdown_percentage:
            log_status(f"Battery critically low ({percent}%). Attempting to shutdown.......")
            notify_user("Critical battery warning", f"Battery critically low ({percent}%). Shutting down.......")
            shutdown_computer()
        elif percent <= Warning_percentage and not Warned:
            log_status(f"Warning: Battery low at {percent}%. Please plug in your charger.")
            notify_user("Low battery warning", f"Battery is low at {percent}%. Please plug in your charger.")
            Warned = True    # Prevent duplicate battery warnings
        elif percent > Warning_percentage:
            Warned = False     # Reset warning when battery level recovers

# Main loop
def main():
    """
    Main loop to continuously monitor battery status.
    - Executes every `Check_interval` seconds
    """
    while True:
        check_battery()
        time.sleep(Check_interval)
#Entry point
if __name__ == "__main__":
    main()