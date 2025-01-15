import psutil
import time

def monitor_ram(threshold):
    while True:
        memory = psutil.virtual_memory()
        ram_used = memory.percent
        print(f"RAM Usage: {ram_used}%")
        if ram_used > threshold:
            print(f"Warning! RAM Usage exceeds {threshold}%")
            time.sleep(5)

threshold = int(input("Enter RAM usage threshold (in %): "))
monitor_ram(threshold)