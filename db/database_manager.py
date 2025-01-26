import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "prescriptions" (
                "serial_no"	INTEGER,
                "doctor_id"	INTEGER,
                "date"	TEXT,
                "name"	TEXT,
                "age"	TEXT,
                "sex"	TEXT,
                "weight"	TEXT,
                "bp"	NUMERIC,
                "observations"	TEXT,
                "prescription"	TEXT,
                "phone_no"	NUMERIC,
                PRIMARY KEY("serial_no" AUTOINCREMENT)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "images" (
                    "image_id"	INTEGER,
                    "serial_no"	INTEGER,
                    "image_path"	TEXT,
                    PRIMARY KEY("image_id" AUTOINCREMENT),
                    FOREIGN KEY("serial_no") REFERENCES "prescriptions"("serial_no")
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "users" (
                   "id"	INTEGER,
                    "username"	TEXT NOT NULL UNIQUE,
                    "password"	TEXT NOT NULL,
                    "clinic_name"	TEXT,
                    "name"	TEXT,
                    "qualifications"	TEXT,
                    "designation"	TEXT,
                    "doctor_id"	INTEGER,
                    "phone_no"	NUMERIC,
                    "email"	TEXT,
	                "mac_address"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )   
            """)
            conn.commit()

    def fetch_prescription(self, serial_no):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prescriptions WHERE serial_no = ?", (serial_no,))
            return cursor.fetchone()

    def insert_prescription(self, doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prescriptions (doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no))
            conn.commit()
            return cursor.lastrowid

    def update_prescription(self, serial_no, doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE prescriptions SET doctor_id = ?, date = ?, name = ?, age = ?, sex = ?, weight = ?, bp = ?, observations = ?, prescription = ?, phone_no = ?
                WHERE serial_no = ?
            """, (doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no, serial_no))
            conn.commit()

    def insert_image(self, serial_no, image_path):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO images (serial_no, image_path)
                VALUES (?, ?)
            """, (serial_no, image_path))
            conn.commit()

    def fetch_images(self, serial_no):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT image_path FROM images WHERE serial_no = ?", (serial_no,))
            return cursor.fetchall()

    def authenticate_user(self, username, password):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            return result

    def search_patients(self, query):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT serial_no, name, phone_no
                FROM prescriptions
                WHERE name LIKE ? OR phone_no LIKE ?
            """, (f"%{query}%", f"%{query}%"))
            return cursor.fetchall()
        
    def insert_user(self, username, password, clinic_name, name, qualifications, designation, doctor_id, phone_no, email, mac_address):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, clinic_name, name, qualifications, designation, doctor_id, phone_no, email, mac_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, password, clinic_name, name, qualifications, designation, doctor_id, phone_no, email, mac_address))
            conn.commit()
            return cursor.lastrowid
                
    def get_serial_no(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(serial_no) FROM prescriptions")
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
        
    def fetch_mac_address(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT mac_address, username FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            return result
        
    def insert_mac_address(self, username, mac_address):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET mac_address = ? WHERE username = ?", (mac_address, username))
            conn.commit()
        