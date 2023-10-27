import psycopg2 as pg


def connect():  # returns a pg connection object
    """
    Return a connection object to the ehar_books database or exit if failure
    :return: Connection object
    """

    # What can go wrong?
    try:
        pwd_file = open("/Users/jaxlub/.CS345pwd", 'r')
    except OSError as e:
        print(f"Error: file not readable: {e}")
        exit()

    # raw string no escape sequences r"____"

    # Connect to an existing DB
    # returns a connection object
    try:
        conn= pg.connect(host='ada.hpc.stlawu.edu',
                         user='jalubk20',
                         password=pwd_file.readline().strip(),
                         dbname='ehar_books')
    except pg.Error as e:
        print(f"Error: could not connect to database: {e}")
        exit()
    finally:
        pwd_file.close() # close for good security practice
    return conn