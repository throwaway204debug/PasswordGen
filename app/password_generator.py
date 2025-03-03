import math
import secrets
import string
from collections import Counter
import hashlib
import requests

def load_word_list(filename):
    with open(filename, 'r') as file:
        return set(line.strip().lower() for line in file)

#common words to avoid
# resource https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/500-worst-passwords.txt
word_set = load_word_list("500-worst-passwords.txt")

allowed_punctuation = r"~!@#$%^&*()-=_+\[{]}"

def generate_password(length):
    if length < 8:
        raise ValueError("Password length must be at least 8!")

    all_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + allowed_punctuation

    while True:
        password_chars = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice(allowed_punctuation)
        ]

        while len(password_chars) < length:
            password_chars.append(secrets.choice(all_chars))

        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        return password

# calculates entropy for a particular password
# resource: https://www.omnicalculator.com/other/password-entropy
def calculate_entropy(password):
    pool_sizes = {
        "digits": 10,
        "lowercase": 26,
        "uppercase": 26,
        "special": 32  # Special characters (typical U.S. keyboard)
    }
    R = 0
    if any(char.isdigit() for char in password):
        R += pool_sizes["digits"]
    if any(char.islower() for char in password):
        R += pool_sizes["lowercase"]
    if any(char.isupper() for char in password):
        R += pool_sizes["uppercase"]
    if any(char in allowed_punctuation
           for char in password):
        R += pool_sizes["special"]

    L = len(password)

    E = L * math.log2(R)

    return E

# Function to test if the generated password distribution is random ( used ChatGpt)
def test_randomness(passwords):
    all_chars = ''.join(passwords)

    # Frequency check (optional)
    char_counts = Counter(all_chars)
    print("\nCharacter Frequencies:")
    for char, count in char_counts.items():
        print(f"{char}: {count}")

    # Additional check: Proportion of each character type should be approximately uniform
    total_chars = len(all_chars)
    for char, count in char_counts.items():
        proportion = count / total_chars
        print(f"Character '{char}' appears {proportion * 100:.2f}% of the time.")

def is_valid_password(password):
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter.")

    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter.")

    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit.")

    if not any(c in allowed_punctuation for c in password):
        errors.append(f"Password must contain at least one special character from {allowed_punctuation}.")

    if any(word in password for word in word_set):
        errors.append("Password must not contain common words!!!")

    entropy = calculate_entropy(password)
    print(f"Password Entropy: {entropy:.2f} bits")

    if errors:
        return False, errors
    return True, []

# def pwned_pwds(password):
#     sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
#     first5char = sha1[:5]
#     pwn_url = f"https://api.pwnedpasswords.com/range/{first5char}"
#     response = requests.get(pwn_url)


if __name__ == "__main__":
    # passwords = [generate_password(12) for _ in range(10000)]
    # test_randomness(passwords)
    action = input("Do you want to generate a password? (y/n): ").strip().lower()

    if action == "y":
        while True:
            try:
                length = int(input("Enter the length of the password (minimum 8, maximum 100): ").strip())
                if length < 8 or (length > 100):
                    print("Password length must be at least 8 or at most 100. Please enter a valid number.")
                else:
                    generated_password = generate_password(length)
                    print(f"Generated Password: {generated_password}")
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    elif action == "n":
        print("Okay, no password generated.")

    else:
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    validate_action = input("Do you want to check for basic password safety? (y/n): ").strip().lower()
    if validate_action == "y":
        password = input("Enter the password : ").strip()
        is_valid, errors = is_valid_password(password)
        # breached =
        if is_valid:
            print("Password seems safe enough.")
        else:
            print("Password is not that safe. Here are the issues:")
            for error in errors:
                print(f"- {error}")
    elif validate_action == "n":
        print("Okay, no validation done.")
    else:
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")