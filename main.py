import sqlite3

conn = sqlite3.connect('rarbg_db.sqlite')

# Create a cursor object
cursor = conn.cursor()

# Fetch data
searchTerm = "%monty%"
cursor.execute("SELECT * FROM items WHERE title LIKE ?", (searchTerm))
rows = cursor.fetchall()
for row in rows:
    print(row)



# Close the connection
conn.close()
