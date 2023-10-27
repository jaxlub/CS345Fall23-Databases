import connect_books as cb
import psycopg2 as pg

# add unique checks for keys
def get_title_by_isbn(conn: pg.Connection,
                      isbn: str) -> str | None:
    cmd = "SELECT title FROM books WHERE isbn = %s"

    def __init__(self, conn: cb.Connection):
        self.conn = conn

    # get a cursor to execute the query
    cur = conn.cursor()
    cur.execute(cmd, (isbn.strip(),))

    # get the resultset which is either of
    # size zero or one

    # Python's conditional expression
    # return cur.rowcount == 0 ? None : cur.fetchone()
    rv = None
    if cur.rowcount > 0:
        rv = cur.fetchall()
    cur.close() # context manager
    return rv

# A cursor is an object that refers to a database
# and is used for executing queries. A single connection
# can have many cursors.


def get_books_by_author(conn: pg.Connection, name: str) -> list[[str, str, str]] | None:
    cmd1 = 'SELECT title FROM books WHERE author = ' + "'" + name + "'"
    cmd = """
            SELECT 
                title, publisher, isbn 
            FROM 
                books 
            WHERE 
                LOWER(REPLACE(REPLACE(author, ' ', ''), '.', '')) = LOWER(REPLACE(REPLACE(%s, ' ', ''), '.', ''));
            """
    cur = conn.cursor()
    # cur.execute(cmd)
    cur.execute(cmd, [name])
    if cur.rowcount == 0:
        return None
    cur.fetchone
    rv = []
    for row in cur:
        rv.append(row)

    cur.close()
    return rv


# Find an authors average book rating. Output is (Avg Rating, #books)
def avg_rating_by_author(conn: pg.Connection, name: str) -> list[[int, int]] | None:
    cmd = """
    SELECT 
        avg(rating), count(books.isbn)
    FROM
        ratings NATURAL JOIN books
    WHERE
        LOWER(REPLACE(REPLACE(author, ' ', ''), '.', '')) = LOWER(REPLACE(REPLACE(%s, ' ', ''), '.', ''))
    """
    cur = conn.cursor()
    cur.execute(cmd, [name.strip()])

    if cur.rowcount == 0:
        return None

    rv = []
    for row in cur:
        rv.append(row)

    cur.close()
    return rv


# Find the average rating for the user that has the most
# book reviews
def avg_rating_most_reviews_user(conn: pg.Connection) -> int | None:
    cmd = """
    SELECT
        avg(rating)
    FROM
        ratings
    WHERE
        user_id = (SELECT 
                    user_id 
                FROM 
                    ratings 
                GROUP BY 
                    user_id 
                ORDER BY count(*) DESC LIMIT 1)
    """
    cur = conn.cursor()
    cur.execute(cmd)

    rv = None
    if cur.rowcount > 0:
        rv = cur.fetchone()[0]
    cur.close()  # context manager
    return rv

# Insert a new book
def insert_book(conn: pg.Connection, title: str, author: str, year: int, publisher: str, small: str, medium: str, large: str, isbn: str) -> None:
    cmd = """
    INSERT INTO books (title, author, year, publisher, small, medium, large, isbn)
    VALUES (%s, %s, %s, %s, %s)
    """
    cur = conn.cursor()
    cur.execute(cmd, [title.strip(), author.strip(), year, publisher.strip(), small.strip(), medium.strip(), large.strip(), isbn.strip()])
    conn.commit()
    cur.close()


# List the top n authors that have the most published books, where n
# is the input by the user. Output is n rows of author name, and number of books
# order from most to least

def top_n_authors(conn: pg.Connection, n: int, offset: str) -> list[[str, int]] | None:
    cmd = """
    SELECT
        LOWER(REPLACE(REPLACE(author, ' ', ''), '.', '')), count(*)
    FROM
        books
    GROUP BY
        LOWER(REPLACE(REPLACE(author, ' ', ''), '.', ''))
    ORDER BY
        count(*) DESC
    LIMIT
        10 OFFSET %s
    """
    cur = conn.cursor()
    cur.execute(cmd, [n, offset])

    if cur.rowcount == 0:
        return None

    rv = []
    for row in cur:
        rv.append(row)

    cur.close()
    return rv

def get_avg_by_title_author(connection, author: str, title: str):
    """
    Return rating by title and author
    :param connection: DB Connection
    :param title: Book Title
    :param author: Book Author
    :return:
    """
    cur = connection.cursor()
    cmd = """
            SELECT 
                avg(rating)
            FROM 
                books natural join ratings
            WHERE
                LOWER(REPLACE(REPLACE(books.author, ' ', ''), '.', '')) = LOWER(REPLACE(REPLACE(%s, ' ', ''), '.', '')) and
                LOWER(REPLACE(REPLACE(books.title, ' ', ''), '.', '')) = LOWER(REPLACE(REPLACE(%s, ' ', ''), '.', ''));
          """
    cur.execute(cmd, [author.strip(), title.strip()])

    return_value = []
    for row in cur:
        return_value.append(row)
    cur.close()
    return return_value



#4
def add_user(connection, new_id: str, location: str, age: str):
    try:
        cur = connection.cursor()
        # Open to SQL Injection
        # print(add_user(conn, "SQLInjTest", "Vermont", "28); INSERT into users VALUES ('Injected', 'Success', '100'"))
        cmd ="INSERT INTO users VALUES (%s, %s," + age + ");"

        print(cmd)
        cur.execute(cmd, [new_id.strip(), location.strip()])
        connection.commit()
        return "User Added"
    except pg.errors.UniqueViolation:
        return "There is already a User with that ID"

#6
def add_review(connection, id: str, isbn: str, book_rating: str):
    try:
        cur = connection.cursor()
        cmd = """
            INSERT INTO ratings VALUES (%s, %s, %s);
            """
        cur.execute(cmd, [id.strip(), isbn.strip(), book_rating.strip()])
        connection.commit()
        return "Rating Added"
    except pg.errors.UniqueViolation:
        return "You have already submitted this rating"
    except pg.errors.ForeignKeyViolation:
        return "Invalid ISBN or User"

#8
def top_n_books(connection, n: str, offset: str):
    cur = connection.cursor()
    cmd = """
        WITH
            counter as(
                SELECT
                    isbn, count(*)
                FROM
                    books natural join ratings
                group by
                    isbn
                ORDER BY
                    count(*) desc
                LIMIT
                    %s)
        SELECT
            books.title, books.author, counter.count
        FROM books natural join counter
        limit 10 OFFSET %s;
    """
    cur.execute(cmd, [n, offset])
    return_value = []
    for row in cur:
        return_value.append(row)
    cur.close()
    return return_value
