import sqlite3
import bcrypt

def get_db_connection():
    #Establishes a connection to the database
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def close_db_connection(conn):
    #Closes the database connection
    if conn:
        conn.close()

def hash_password(password):
    #Hashes a password for storing.
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    #Checks a password against a stored hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def init_db():
    #Initializes the database and creates the users table.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    # Add sample users with hashed passwords
    sample_users = [
        ('John Doe', 'john@example.com', hash_password('password123')),
        ('Jane Smith', 'jane@example.com', hash_password('secret456')),
        ('Bob Johnson', 'bob@example.com', hash_password('qwerty789'))
    ]
    cursor.executemany("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", sample_users)
    conn.commit()
    conn.close()
    print("Database initialized with sample data.")