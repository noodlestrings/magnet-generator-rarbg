import sqlite3


def init_db(filename):
    conn = sqlite3.connect(filename)
    # Create a cursor object
    cursor = conn.cursor()
    return (cursor, conn)


def get_filter_parameters():
    filterParameters = {}
    print("Please only enter 't' or 'f' for each option")
    showOnly4k = input("Only see 4k torrents: ").lower()[0] == "t"
    if showOnly4k == False:
        show720p = input("See 720p torrents: ").lower()[0] == "t"
        show480p = input("See 480p torrents: ").lower()[0] == "t"
        showXvidFormat = input("See xvid format torrents: ").lower()[0] == "t"
    else:
        show720p = False
        show480p = False
        showXvidFormat = False

    filterParameters["show-only-4k"] = showOnly4k
    filterParameters["show-720p"] = show720p
    filterParameters["show-480p"] = show480p
    filterParameters["show-xvid-format"] = showXvidFormat

    return filterParameters


def fetch_data(searchTerm, cursor):
    searchTerm = "%" + searchTerm + "%"
    cursor.execute(
        "SELECT * FROM items WHERE title LIKE ? OR title LIKE ? AND cat LIKE ?",
        (searchTerm, searchTerm.replace(" ", "."), "movie%"),
    )
    rows = cursor.fetchall()

    return rows


def clean_data(data, filters):
    """
    Cleans the data obtained from the database and converts it into a dictionary.

    Args:
        data (list): A list of tuples containing film data from the database.
        filters (dict): A dictionary of the filters that the user would like to filter the results by, e.g. resolution:
        {filtername: boolean, ...}

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

    cleanedData = {}
    for item in data:
        id = item[0]
        contents = list(item)
        contents.remove(id)

        if contents[4] == None:
            continue

        if contents[3].lower() == "xxx":
            continue

        if filters["show-only-4k"] == True:
            if "4k" not in contents[3]:
                continue
        if filters["show-720p"] == False:
            if "720" in contents[3]:
                continue
        if filters["show-480p"] == False:
            if "480" in contents[3] or "480" in contents[1]:
                continue
        if filters["show-xvid-format"] == False:
            if "xvid" in contents[3]:
                continue

        # size in gb
        contents[4] /= 1073741824
        contents[4] = round(contents[4], 2)

        cleanedData[id] = tuple(contents[:-2])
    return cleanedData


def magnetiser(hash, name):
    pass


def main():
    cursor, conn = init_db("rarbg_db.sqlite")
    searchTerm = input("Enter a search term: ")
    data = clean_data(fetch_data(searchTerm, cursor), get_filter_parameters())
    for item in data:
        print(data[item])

    conn.close()


if __name__ == "__main__":
    main()
