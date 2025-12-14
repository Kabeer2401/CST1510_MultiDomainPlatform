import bcrypt
import os
import re
#  WEEK 11: OOP REFACTORING
class User:
    """
    User Entity Class.
    Represents a system user with properties for authentication.
    Refactored for Week 11 Software Architecture requirements.
    """
    def __init__(self, username, role='user'):
        self.username = username
        self.role = role
        self.is_authenticated = False

    def login(self):
        self.is_authenticated = True

from db_manager import DatabaseManager

#  Global Constants
# Using a constant for the filename makes it easy to change later if needed.
USER_DATA_FILE = "users.txt"
# Initialize Database Manager
db = DatabaseManager()


#  PART 1: SECURITY FUNCTIONS

def hash_password(plain_text_password):
    """
    Hashes password using bcrypt.
    Learnt from Week 7 Lecture: Hashing is one-way. Plain text can never be stored.
    """
    # 1. Convert string to bytes (bcrypt requires bytes)
    bytes_password = plain_text_password.encode('utf-8')

    # 2. Generate1 random salt (adds randomness to prevent Rainbow Table attacks)
    salt = bcrypt.gensalt()

    # 3. Hash the password (slow to stop hackers)
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


#  PART 2: VALIDATION

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


#  PART 3: USER MANAGEMENT

def user_exists(username):
    """
    Checks if user exists in the SQLite Database.
    """
    # db.find_user returns the user data or None
    return db.find_user(username) is not None


def register_user(username, password):
    """
    Registers user into SQLite Database.
    """
    # 1. Validate Input
    is_valid_user, msg_user = validate_username(username)
    if not is_valid_user:
        print(f"Error: {msg_user}")
        return False

    is_valid_pass, msg_pass = validate_password(password)
    if not is_valid_pass:
        print(f"Error: {msg_pass}")
        return False

    # 2. Check Database for duplicate
    if user_exists(username):
        print(f"Error: User '{username}' already exists.")
        return False

    # 3. Hash Password
    hashed_pw = hash_password(password)

    # 4. Add to Database
    if db.add_user(username, hashed_pw):
        print("Registration Successful (Saved to Database)!")
        return True
    else:
        print("Database Error.")
        return False


def login_user(username, password):
    """
    Authenticates against SQLite Database.
    """
    # 1. Find user in DB
    user_record = db.find_user(username)

  # user_record format: (id, username, password_hash, role)
    stored_hash = user_record[2]

    # 2. Verify Password
    if verify_password(password, stored_hash):
        print(f"Login Successful! Welcome {username}.")
        # Week 11 Note: In a full OOP architecture, we instantiate the User class here:
        # current_user = User(username)
        # current_user.login()

        return True
    else:
        print("Error: Incorrect password.")
        return False


#  PART 4: MAIN MENU

def main():
    while True:
        print("\n SECURE SYSTEM WEEK 7 ")
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
# Minor update to trigger commit for history correction
