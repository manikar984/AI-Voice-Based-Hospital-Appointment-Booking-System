import sqlite3

connection = sqlite3.connect("appointments.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS doctors")

connection.commit()

connection.close()

print("Doctors table deleted successfully.")