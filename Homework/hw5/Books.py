import connect_books as cb
import psycopg as pg
import tabulate

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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
        try:
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
            if cur.rowcount > 0:
                rv = cur.fetchone()[0]
            cur.close()  # context manager
            return rv
        except pg.errors as error:
            print(f"Error: {error}")

    def get_books_by_author(self, name: str) -> list[[str, str, str]] | str | None:
        try:
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
                        LOWER(REPLACE(REPLACE(author, ' ', ''), '.', '')) = LOWER(REPLACE(REPLACE(%s, ' ', ''), '.', ''));
                    """
            cur = self.conn.cursor()

            if cur.rowcount == 0:
                cur.close()
                return "No authors with that name"
            cur.execute(cmd, [name])
            rv = []
            counter = 0
            for row in cur:
                rv.append(row)
                counter += 1
                if counter == 10:
                    print(tabulate.tabulate(rv))
                    counter = 0
                    rv = []
                    input("Press Enter to continue")
            return None
        except pg.errors as error:
            print(f"Error: {error}")


    def top_n_authors(self, n: str, offset: str) -> list[[str, int]] | None:
        try:
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
                %s OFFSET %s
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
        except pg.errors.NumericValueOutOfRange as error:
            print(f"Error: {error}")

    def top_n_books(self, n: str, offset: str):
        try:
            cur = self.conn.cursor()
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
        except pg.errors.InFailedSqlTransaction as error:
            print(f"Error: {error}")
        except pg.errors.NumericValueOutOfRange as error:
            print(f"Error: {error}")


    def valid_books(self, title: str):
        try:
            cur = self.conn.cursor()
            cmd = """
            SELECT
                title
            FROM
                books
            WHERE
                title = %s
            """
            cur.execute(cmd, [title])
            if cur.rowcount == 0:
                return False
            else:
                return True
        except pg.errors as error:
            print(f"Error: {error}")

    def valid_author(self, name: str):
        try:
            cur = self.conn.cursor()
            cmd = """
            SELECT
                author
            FROM
                books
            WHERE
                author = %s
            """
            cur.execute(cmd, [name])
            if cur.rowcount == 0:
                return False
            else:
                return True
        except pg.errors as error:
            print(f"Error: {error}")

