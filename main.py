import sqlite3


def fetch_data(searchTerm, cursor):
    searchTerm = "%" + searchTerm + "%"
    cursor.execute("SELECT * FROM items WHERE title LIKE ? AND cat LIKE ?", (searchTerm, 'movie%'))
    rows = cursor.fetchall()
    return rows

def clean_data(data):
    # cleans the data from the database
    pass 


def init_db(filename):
    conn = sqlite3.connect(filename)
    # Create a cursor object
    cursor = conn.cursor()
    return (cursor, conn)

def magnetiser(hash, name):
    pass


def main():
    cursor, conn = init_db("rarbg_db.sqlite")
    searchTerm = input("Enter a search term: ")
    data=clean_data(fetch_data(searchTerm, cursor))

    conn.close()


if __name__ == "__main__":
    main()
