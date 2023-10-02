import connect_books as cb
import psycopg2 as pg


def get_title_by_isbn(connection, isbn: str) -> str:
    cmd = "SELECT title FROM books WHERE isbn = %s"

    # get a cursor to execute the query
    cur = conn.cursor()
    cur.execute(cmd, (isbn.strip(),))  # isbn must be a tuple

    # get the resultset which is either of size 0 or 1 (as it is a primary key)
    if cur.rowcount == 0:
        cur.close()
        return ""
    else:
        return_val = cur.fetchone()[0]
        cur.close()
        return return_val


# A cursor is an object that refers to a database and is used for executing queries.
# A single connection can have many cursors.


def get_books_by_author(connection, author: str) -> list[str]:
    cur = connection.cursor()
    cmd = """
            SELECT 
                title, pub_year, publisher, isbn 
            FROM 
                books 
            WHERE 
                books.author = %s
          """
    cur.execute(cmd, (author.strip(),))  # isbn must be a tuple

    # Bad Security Practice
    # cmd = "SELECT title FROM books where books.author = '" + author + "'"
    # cur.execute(cmd)  # isbn must be a tuple

    return_value = []
    for row in cur:
        return_value.append(row)
    cur.close()
    return return_value


# Main program
if __name__ == "__main__":
    conn = cb.connect()
    print(get_title_by_isbn(conn, '0440418569'))
    print(get_title_by_isbn(conn, '1234'))
    print(get_books_by_author(conn, 'A. A. Milne'))
