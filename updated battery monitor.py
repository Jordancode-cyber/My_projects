import psutil
import platform
import time
import logging
import requests
from tkinter import Tk, messagebox

# ===== Configuration =====
SERVER_URL = "https://yourserver.com/upload"  # Replace with your actual server endpoint
LOG_FILE = "system_monitor.log"

# Logging setup
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ===== Utility Functions =====
def log_message(message):
    """Log and display a message."""
    logging.info(message)
    print(message)

def get_user_consent():
    """Prompt the user for consent to collect and share data."""
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    response = messagebox.askyesno(
        "Data Sharing Consent",
        "We'd like to collect anonymized system information to improve this app. "
        "Do you consent to sharing this data?"
    )
    root.destroy()
    return response

def collect_system_data():
    """Collect non-sensitive system information."""
    try:
        battery = psutil.sensors_battery()
        system_data = {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.architecture()[0],
            "cpu_count": psutil.cpu_count(),
            "total_memory": psutil.virtual_memory().total,
            "battery_percentage": battery.percent if battery else None,
            "is_charging": battery.power_plugged if battery else None,
            "timestamp": time.time()
        }
        log_message("System data collected successfully.")
        return system_data
    except Exception as e:
        log_message(f"Error collecting system data: {e}")
        return None

def send_data_to_server(data):
    """Send collected system data to the central server."""
    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            log_message("Data successfully sent to the server.")
        else:
            log_message(f"Failed to send data. Server responded with status: {response.status_code}")
    except Exception as e:
        log_message(f"Error sending data to server: {e}")

# ===== Main Logic =====
def main():
    """Main workflow: ask for consent, collect data, and send it."""
    log_message("Script started.")
    
    # Ask for user consent
    if not get_user_consent():
        log_message("User declined to share data. Exiting.")
        print("You have declined data sharing. No data will be collected.")
        return

    # Collect and send system data
    system_data = collect_system_data()
    if system_data:
        send_data_to_server(system_data)
    else:
        log_message("No data collected. Exiting.")

    log_message("Script completed.")

# ===== Entry Point =====
if __name__ == "__main__":
    main()