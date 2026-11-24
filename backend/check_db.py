import sqlite3

connection = sqlite3.connect("appointments.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
SELECT doctor_id, name, status
FROM doctors
ORDER BY doctor_id;
""")

rows = cursor.fetchall()

for row in rows:
    print(dict(row))

connection.close()