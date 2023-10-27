import connect_books as cb
import psycopg as pg

class Books:
    def __init__(self, conn: pg.Connection):
        self.conn = conn

    def insert_book(self, title: str, author: str, year: int, publisher: str, small: str, medium: str,
                    large: str, isbn: str) -> None:
        """
        Insert into the Books Database
        :param title: Book title
        :param author: Author Name
        :param year: Year published
        :param publisher: Publisher of book
        :param small: Small image url
        :param medium: medium image url
        :param large: large image url
        :param isbn: book isbn
        :return:
        """
        cmd = """
        INSERT INTO books (title, author, year, publisher, small, medium, large, isbn)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cur = self.conn.cursor()
            cur.execute(cmd, [title.strip(), author.strip(), year, publisher.strip(), small.strip(), medium.strip(),
                              large.strip(), isbn.strip()])
            self.conn.commit()
            cur.close()
            print("Book Added")
        except pg.errors.UniqueViolation:
            print("This book is already in the database")

    def get_title_by_isbn(self, isbn: str) -> str | None:
        """
        Return the book title using the ISBN
        :param isbn: Book number of interest
        :return: Return the title of the book
        """

        cmd = "SELECT title FROM books WHERE isbn = %s"

        # get a cursor to execute the query
        cur = self.conn.cursor()
        cur.execute(cmd, (isbn.strip(),))

        # get the resultset which is either of
        # size zero or one

        # Python's conditional expression
        # return cur.rowcount == 0 ? None : cur.fetchone()
        rv = "No Book with that ISBN"

        cur.


        if cur.rowcount > 0:
            rv = cur.fetchone()[0]
        cur.close()  # context manager
        return rv

    def get_books_by_author(self, name: str, offset) -> list[[str, str, str]] | str:
        """
        Gets all books by the desired author
        :param name: Author Name
        :return: Books by said Author
        """
        cmd = """
                SELECT 
                    title, publisher, isbn 
                FROM 
                    books 
                WHERE 
                    LOWER(REPLACE(REPLACE(author, ' ', ''), '.', '')) = LOWER(REPLACE(REPLACE(%s, ' ', ''), '.', ''))
                LIMIT 10 OFFSET %s;
                """
        cur = self.conn.cursor()

        offset = 0
        if cur.rowcount == 0:
            return "No authors with that name"
            cur.close()
        while cur.rowcount != 0:
            enter = input("Press Enter to continue")
            cur.execute(cmd, [name, str(offset)])
            offset += 10
            rv = []
            for row in cur:
                rv.append(row)
            tabulate(rv)





            cur.close()
            return rv





    def top_n_authors(self, n: int, offset: int) -> list[[str, int]] | None:
        """
        Returns the top authors
        :param n: number of authors wished to see
        :param offset: variable used to see which area of rankings should be displayed
        :return: ranking of the most popular author
        """
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
            10 OFFSET %n
        """
        cur = self.conn.cursor()
        cur.execute(cmd, [n, offset])

        if cur.rowcount == 0:
            return None
        rv = []
        for row in cur:
            rv.append(row)
        cur.close()
        return rv
