import bcrypt
import os
import re

# --- Global Constants ---
# Using a constant for the filename makes it easy to change later if needed.
USER_DATA_FILE = "users.txt"


# --- PART 1: SECURITY FUNCTIONS ---

def hash_password(plain_text_password):
    """
    Hashes a password using bcrypt.
    Learned from Week 7 Lecture: Hashing is one-way. We never store plain text.
    """
    # 1. Convert string to bytes (bcrypt requires bytes)
    bytes_password = plain_text_password.encode('utf-8')

    # 2. Generate a random salt (adds randomness to prevent Rainbow Table attacks)
    salt = bcrypt.gensalt()

    # 3. Hash the password (slow by design to stop hackers)
    hashed_bytes = bcrypt.hashpw(bytes_password, salt)

    # 4. Decode back to string for storage in users.txt
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    """
    Verifies a login attempt.
    Learned from Week 7 Lecture: We hash the input and compare it to the stored hash.
    """
    # Encode both to bytes
    bytes_password = plain_text_password.encode('utf-8')
    bytes_hashed_password = hashed_password.encode('utf-8')

    # bcrypt.checkpw extracts the salt from the hash and compares safely
    return bcrypt.checkpw(bytes_password, bytes_hashed_password)


# --- PART 2: VALIDATION (Lab Requirement) ---

def validate_username(username):
    """
    Checks if username is valid format.
    Returns: (bool, str) -> (IsValid, Message)
    """
    if not username:
        return False, "Username cannot be empty."

    # Lab requirement: Length between 3 and 20
    if not (3 <= len(username) <= 20):
        return False, "Username must be 3-20 characters long."

    # Lab requirement: Alphanumeric only
    if not re.fullmatch(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username contains invalid characters."

    return True, ""


def validate_password(password):
    """
    Checks password complexity.
    Returns: (bool, str) -> (IsValid, Message)
    """
    # Lab requirement: Length 6-50
    if not (6 <= len(password) <= 50):
        return False, "Password must be 6-50 characters."

    # Lab requirement: Complexity regex
    if not re.search(r"[A-Z]", password):
        return False, "Needs an uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Needs a lowercase letter."
    if not re.search(r"\d", password):
        return False, "Needs a number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Needs a special character."

    return True, ""


# --- PART 3: USER MANAGEMENT ---

def user_exists(username):
    """
    Helper function to check if username is taken.
    """
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            # File format is: username,hash
            parts = line.split(',')
            if len(parts) >= 1:
                if parts[0] == username:
                    return True
    return False


def register_user(username, password):
    """
    Registers a new user after validation.
    """
    # 1. Validate Input
    valid_user, msg_user = validate_username(username)
    if not valid_user:
        print(f"Error: {msg_user}")
        return False

    valid_pass, msg_pass = validate_password(password)
    if not valid_pass:
        print(f"Error: {msg_pass}")
        return False

    # 2. Check Duplicates
    if user_exists(username):
        print(f"Error: User '{username}' already exists.")
        return False

    # 3. Hash and Save
    hashed_pw = hash_password(password)

    # Append mode 'a' adds to end of file
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_pw}\n")

    print("Registration Successful!")
    return True


def login_user(username, password):
    """
    Authenticates a user.
    """
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No registered users found.")
        return False

    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            parts = line.split(',')
            if len(parts) == 2:
                stored_user, stored_hash = parts[0], parts[1]

                if stored_user == username:
                    # Found user, verify password
                    if verify_password(password, stored_hash):
                        print(f"Login Successful! Welcome {username}.")
                        return True
                    else:
                        print("Error: Incorrect password.")
                        return False

    print("Error: Username not found.")
    return False


# --- PART 4: MAIN MENU ---

def main():
    while True:
        print("\n--- SECURE SYSTEM WEEK 7 ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choice: ").strip()

        if choice == '1':
            u = input("Choose Username: ").strip()
            p = input("Choose Password: ").strip()
            register_user(u, p)

        elif choice == '2':
            u = input("Username: ").strip()
            p = input("Password: ").strip()
            login_user(u, p)

        elif choice == '3':
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
