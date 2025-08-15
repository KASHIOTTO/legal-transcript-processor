import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

class AuthError(Exception):
    pass

class Auth:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash BLOB NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password, role):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            self.conn.execute(
                'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                (username, password_hash, role)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise AuthError('User already exists')

    def authenticate(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT password_hash, role FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        if not row:
            raise AuthError('Invalid username')
        pw_hash, role = row
        if bcrypt.checkpw(password.encode(), pw_hash):
            return role
        else: 
            raise AuthError('Invalid password')
