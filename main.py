import sqlite3
from tabulate import tabulate as Tabulate
import pyperclip


def init_db(filename):
    """
    Initializes an SQLite database connection and creates a cursor object.

    Args:
        filename (str): The name of the database file.

    Returns:
        tuple: A tuple containing the cursor and connection objects.

    """
    conn = sqlite3.connect(filename)
    # Create a cursor object
    cursor = conn.cursor()
    return (cursor, conn)


def get_filter_parameters():
    """
    Prompts the user to enter filter parameters for the search.

    Returns:
        dict: A dictionary containing the filter parameters.

    """
    filterParameters = {}
    print("Please only enter 'y' or 'n' for each option")
    showOnly4k = input("Only see 4k torrents: ").lower()[0] == "y"
    if showOnly4k == False:
        show720p = input("See 720p torrents: ").lower()[0] == "y"
        show480p = input("See 480p torrents: ").lower()[0] == "y"
        showXvidFormat = input("See xvid format torrents: ").lower()[0] == "y"
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
    """
    Fetches data from the database based on the search term.

    Args:
        searchTerm (str): The search term to be used in the database query.
        cursor (sqlite3.Cursor): The database cursor object.

    Returns:
        list: A list of tuples containing the fetched data.

    """
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
            format: {id: (HASH, TITLE, DATE_OF_UPLOAD, CATEGORY, SIZE_IN_GB)}

    Example:
        data = [(1, 'Film A', 2022, 'Action'),
                (2, 'Film B', 2021, 'Drama')]
        cleaned_data = clean_data(data)

        Result:
            cleaned_data = {1: ('Film A', 2022, 'Action'),
                         2: ('Film B', 2021, 'Drama')}
    """

    cleanedData = {}
    for item in data:
        id = item[0]
        contents = list(item)
        contents.remove(id)

        # if the file size is None or 0
        if contents[4] == None or contents[4] == 0:
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


def display_options(data):
    """
    Displays the options available based on the cleaned data, in a table, using the tabulate python library.

    Args:
        data (dict): A dictionary containing the cleaned film data.

    """
    # {1265355: ('0FCF5037464BE46DABA29C7D90112FA737C8908A', 'Blade.Runner.1982.2160p.BluRay.x264.8bit.SDR.DTS-HD.MA.TrueHD.7.1.Atmos-SWTYBLZ',
    #  '2017-11-15 15:06:47', 'movies_x264_4k', 64.39),

    headers = ["id", "title", "category", "size/GB"]

    # values to populate table with
    table = []

    for key, value in data.items():
        dataTemp = list(value)
        del dataTemp[0]  # remove hash from table
        del dataTemp[1]  # remove date from table
        table.append([key] + dataTemp)

    sortedTable = sorted(table, key=lambda x: x[-1])  # sort by filesize
    sortedTable.reverse()
    with open("torrent-options.txt", "w") as file:
        for entry in sortedTable:
            line = " ".join(str(element) for element in entry)
            file.write(line + "\n")
            file.write("=" * (len(line) + 5))
            file.write("\n")

    print(Tabulate(sortedTable, headers=headers, tablefmt="grid"))


def magnetiser(hash, name):
    """
    Generates a magnet link for a given hash and name. Prints to screen, and copies to clipboard.

    Args:
        hash (str): The hash value.
        name (str): The name of the film.

    """
    # magnet:?xt=urn:btih:7B973E55B2198EAC530440DC7D9589DD708F5692&dn=Shrek+%282001%29+1080p+BrRip+x264+-+1GB-+YIFY
    # +s replace ' 's ??
    print("\n", "magnet:?xt=urn:btih:" + hash + "&dn=" + name.replace(" ", "+"))

    # copies to clipboard
    pyperclip.copy("magnet:?xt=urn:btih:" + hash + "&dn=" + name.replace(" ", "+"))
    pyperclip.paste()


def main():
    cursor, conn = init_db("rarbg_db.sqlite")

    valid = False
    while not valid:
        searchTerm = input("Enter a search term: ")
        if searchTerm != "" or searchTerm != " ":
            valid = True

    rawData = fetch_data(searchTerm, cursor)
    filterParameters = get_filter_parameters()
    cleanedData = clean_data(rawData, filterParameters)

    if len(cleanedData) == 0:
        print("The selected options did not return any results")
        exit()

    display_options(cleanedData)
    print("All of the returned torrents are available to see in 'torrent-options.txt'")

    while True:
        try:
            selectedID = int(
                input("Enter the id of the film to generate a magnet link for it: ")
            )
            hash, title = cleanedData[selectedID][:2]
            magnetiser(hash, title)

            conn.close()
            break
        except ValueError:
            print("\nYou did not enter a numerical id, please try again")
        except KeyError:
            print("\nThat id does not exist, please try again")


if __name__ == "__main__":
    main()
