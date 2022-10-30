import sqlite3


connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, username TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS reminders("
               "user_id INTEGER, reminder_time TEXT, "
               "CONSTRAINT fk_reminder "
               "FOREIGN KEY(user_id) REFERENCES users(user_id))")
