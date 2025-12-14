import sqlite3
import os

# Global constant for the database name
DB_NAME = "platform_data_final.db"


class DatabaseManager:
    """
    Handles all SQLite database interactions.
    Learnt from Week 8: We use a Class to encapsulate DB logic and keep it organized.
    """

    def __init__(self, db_name=DB_NAME):
        """
        Constructor: Checks if DB exists and initializes tables if needed.
        """
        self.db_name = db_name
        # If the file doesn't exist yet, we create the tables immediately
        if not os.path.exists(self.db_name):
            print(f"--- Database '{self.db_name}' not found. Initializing... ---")
            self.create_tables()

    def get_connection(self):
        """
        Opens a connection to the SQLite database.
        Added timeout to prevent OneDrive/File locking errors.
        """
        return sqlite3.connect(self.db_name, timeout=30)

    def create_tables(self):
        """
        Creates the required tables for the coursework.
        Includes: Users, Cyber Incidents, Datasets, and IT Tickets.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. Users Table (Stores credentials)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')

        # 2. Cyber Incidents Table (Domain 1)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_type TEXT,
                severity TEXT,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 3. Datasets Metadata Table (Domain 2 - Placeholder for now)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT,
                row_count INTEGER,
                file_size_mb REAL
            )
        ''')

        # 4. IT Tickets Table (Domain 3 - Placeholder for now)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE,
                issue_desc TEXT,
                priority TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("Database tables created successfully.")

    # --- USER MANAGEMENT & MIGRATION ---

    def add_user(self, username, password_hash):
        """
        Helper function to add a user safely.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # Parameterized query to prevent SQL Injection
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                           (username, password_hash))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def find_user(self, username):
        """
        Finds a user by username. Used for Login.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def migrate_from_text_file(self, text_filename="users.txt"):
        """
        Reads users from Week 7 text file and moves them to SQLite.
        """
        if not os.path.exists(text_filename):
            print(f"Migration Skipped: {text_filename} not found.")
            return

        print(f"--- Migrating users from {text_filename} to SQLite ---")
        count = 0
        with open(text_filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        u = parts[0]
                        p_hash = parts[1]
                        # Use our add_user method to insert into DB
                        if self.add_user(u, p_hash):
                            count += 1
                            print(f"Migrated user: {u}")
                        else:
                            print(f"Skipped duplicate: {u}")
        print(f"Migration Complete. {count} users moved.")

    # --- CYBER INCIDENT CRUD OPERATIONS (Week 8 Requirement) ---

    def create_cyber_incident(self, incident_type, severity, status):
        """
        C: Create a new incident.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO cyber_incidents (incident_type, severity, status) VALUES (?, ?, ?)"
        cursor.execute(sql, (incident_type, severity, status))

        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def read_cyber_incidents(self):
        """
        R: Read all incidents.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM cyber_incidents"
        cursor.execute(sql)
        incidents = cursor.fetchall()

        conn.close()
        return incidents

    def update_cyber_incident(self, incident_id, status):
        """
        U: Update an incident's status.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
        cursor.execute(sql, (status, incident_id))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def delete_cyber_incident(self, incident_id):
        """
        D: Delete an incident.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM cyber_incidents WHERE id = ?"
        cursor.execute(sql, (incident_id,))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success


# --- TEMPORARY TEST CODE ---
if __name__ == "__main__":
    db = DatabaseManager()

    # 1. Test Migration
    db.migrate_from_text_file("users.txt")

    # 2. Test CRUD operations for cyber incidents
    print("\n--- Testing Cyber Incident CRUD ---")

    # Create
    new_id = db.create_cyber_incident("Phishing", "High", "Open")
    print(f"Created incident with ID: {new_id}")

    # Read
    all_incidents = db.read_cyber_incidents()
    print(f"All incidents: {all_incidents}")

    # Update
    if db.update_cyber_incident(new_id, "Closed"):
        print(f"Updated incident {new_id} to Closed")

    # Delete
    if db.delete_cyber_incident(new_id):
        print(f"Deleted incident {new_id}")
