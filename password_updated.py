import random
import string
from datetime import datetime
from cryptography.fernet import Fernet

# Generate a key and save it to a file (run this once to create a key)
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the key for encryption/decryption
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

# Encrypt a log entry
def encrypt_log_entry(entry, key):
    cipher = Fernet(key)
    return cipher.encrypt(entry.encode())

# Decrypt log entries
def decrypt_log_entries(key):
    cipher = Fernet(key)
    with open("encrypted_log.txt", "rb") as file:
        encrypted_entries = file.readlines()
    return [cipher.decrypt(entry).decode() for entry in encrypted_entries]

# Log a password (encrypted)
def log_password(password):
    key = load_key()
    log_file = "encrypted_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {password}\n"
    encrypted_entry = encrypt_log_entry(entry, key)
    
    with open(log_file, "ab") as file:  # Append encrypted log
        file.write(encrypted_entry + b'\n')
    print(f"Password logged (encrypted) in: {log_file}")

# Generate a password
def generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols, avoid_ambiguous):
    characters = ""
    
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()-_=+[]{};:,.<>?/|\\"
    
    if avoid_ambiguous:
        characters = characters.translate(str.maketrans('', '', '0OIl1'))

    if not characters:
        print("No character types selected. Unable to generate password.")
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    log_password(password)
    print(f"Generated password: {password}")
    return password

# Search log file for a specific date or keyword
def search_log(keyword):
    key = load_key()
    try:
        entries = decrypt_log_entries(key)
        matching_entries = [entry for entry in entries if keyword in entry]
        if matching_entries:
            print("Matching entries:")
            for entry in matching_entries:
                print(entry)
        else:
            print("No matching entries found.")
    except FileNotFoundError:
        print("No log file found. Please generate passwords first.")

# Main function
def main():
    choice = input("Do you want to (1) Generate a password or (2) Search log file? Enter 1 or 2: ")
    
    if choice == '1':
        # Generate password
        length = int(input("Enter password length: "))
        use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
        avoid_ambiguous = input("Avoid ambiguous characters (e.g., 0, O, l, 1)? (y/n): ").lower() == 'y'
        generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols, avoid_ambiguous)
    
    elif choice == '2':
        # Search log file
        keyword = input("Enter the date (YYYY-MM-DD) or keyword to search for: ")
        search_log(keyword)
    
    else:
        print("Invalid choice.")

# Run the program
if __name__ == "__main__":
    # Ensure key exists (only generate once; comment this line after running once)
    # generate_key()
    
    main()