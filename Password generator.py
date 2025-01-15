import random
import string
from datetime import datetime

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
        characters = characters.translate(str.maketrans('', '', '0OI1'))

    if not characters:
        print("No character types selected. Unable to generate password.")
        return None
    
    password = ''.join(random.choice(characters) for _ in range(length))
    log_password(password)
    print(f"Generated password: {password}")
    return password

def log_password(password):
    log_file = "password_log.txt"
    timestamp = datetime.now().strftime("%D-%m-%y %H:%M")
    with open(log_file, "a") as file:
        file.write(f"{timestamp} - {password}\n")
    print(f"Password logged in: {log_file}")


#User inputs
length = int(input("Enter your desired password length: "))
use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
use_digits = input("Include digits? (y/n): ").lower() == 'y'
use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
avoid_ambiguous = input("Avoid ambiguous characters (e.g., 0, O, I, 1)? (y/n): ").lower == 'y'


generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols, avoid_ambiguous)