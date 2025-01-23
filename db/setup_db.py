import sqlite3

def initialize_database():
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    # Insert sample data
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
                   ('abc', 'abc'))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized and sample user added.")
