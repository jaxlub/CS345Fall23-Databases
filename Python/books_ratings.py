import psycopg as pg


def connect() -> pg.Connection:  # returns a pg connection object
    """
    Return a connection object to the ehar_books database or exit if failure
    :return: Connection object
    """

    # What can go wrong?
    try:
        pwd_file = open("/Users/jaxlub/.CS45pwd", 'r')
    except OSError as e:
        print(f"Error: file not readable: {e}")
        exit()

    # raw string no escape sequences r"____"

    # Connect to an existing DB
    # returns a connection object
    try:
        conn = pg.connect(
            db_name="ehar_books",
            host="ada.hpc.stlawu.edu",
            user="jalubk20",
            password=pwd_file.readline().strip()
        )
    except pg.Error as e:
        print(f"Error: could not connect to database: {e}")
        exit()

    return conn


def get_title_by_isbn(isbn: str, conn: pg.Connection) -> str:
    cmd = "SELECT FROM books WHERE isbn = %s"

    # get a cursor to execute the query
    cur = conn.cursor()
    cur.execute(cmd, (isbn.strip(),))  # isbn must be a tuple


# Main program
if __name__ == "__main__":
    conn = connect()
