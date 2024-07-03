import hashlib
import sqlite3

print('Add new user to database')
login = input('Login: ')
password = input('Password: ')
hash = hashlib.md5()
hash.update(password.encode())
password = hash.hexdigest()
database = sqlite3.connect('users.db')
cursor = database.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Credentials (id INTEGER PRIMARY KEY, login TEXT NOT NULL, password TEXT NOT NULL)')
cursor.execute('INSERT INTO Credentials (login, password) VALUES (?, ?)', (login, password))
database.commit()
database.close()
print('Registration successful!')