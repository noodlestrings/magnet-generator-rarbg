import sqlite3

def init_db(filename):
    conn = sqlite3.connect(filename)
    # Create a cursor object
    cursor = conn.cursor()
    return (cursor, conn)

def fetch_data(searchTerm, cursor):
    searchTerm = "%" + searchTerm + "%"
    cursor.execute(
        "SELECT * FROM items WHERE title LIKE ? OR title LIKE ? AND cat LIKE ?", (searchTerm, searchTerm.replace(" ", "."), "movie%")
    )
    rows = cursor.fetchall()


    return rows


def clean_data(data):
    """
    Cleans the data obtained from the database and converts it into a dictionary.

    Args:
        data (list): A list of tuples containing film data from the database.

    Returns:
        dict: A dictionary where the ID of each tuple is the key, and the value is a tuple
              containing the cleaned film details.
        example format: {id: (HASH, TITLE, DATE_OF_UPLOAD, CATEGORY, SIZE_IN_GB)}

    Example:
        data = [(1, 'Film A', 2022, 'Action'),
                (2, 'Film B', 2021, 'Drama')]
        cleaned_data = clean_data(data)
        # Result:
        # cleaned_data = {1: ('Film A', 2022, 'Action'),
        #                 2: ('Film B', 2021, 'Drama')}
    """

    # test input is for the search "blade.runner"
    cleanedData = {}
    for item in data:
        id = item[0]
        contents = list(item)
        contents.remove(id)

        # size in gb
        contents[4] /= 1073741824
        contents[4] = round(contents[4], 2)

        # # removes 720p films
        # if "720" in contents[3]:
        #     continue

        cleanedData[id] = tuple(contents[:-2])
    return cleanedData




def magnetiser(hash, name):
    pass


def main():
    cursor, conn = init_db("rarbg_db.sqlite")
    searchTerm = input("Enter a search term: ")
    data = clean_data(fetch_data(searchTerm, cursor))
    for item in data:
        print(data[item])

    conn.close()


if __name__ == "__main__":
    main()
