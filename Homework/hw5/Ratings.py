import connect_books as cb
import psycopg as pg


class Ratings:

    def __init__(self, conn: pg.Connection):
        self.conn = conn


    def avg_rating_by_author(self, name: str) -> list[[int, int]] | None:
        try:
            """
            Get the average rating for the author
            :param name: the author's name
            :return: the average rating (0-10)
            """
            cmd = """
            SELECT
                avg(rating), count(Distinct books.isbn)
            FROM
                ratings NATURAL JOIN books
            WHERE
                LOWER(REPLACE(REPLACE(author, ' ', ''), '.', '')) = LOWER(REPLACE(REPLACE(%s, ' ', ''), '.', ''))
            """
            cur = self.conn.cursor()
            cur.execute(cmd, [name.strip()])


            rv = None
            if cur.rowcount > 0:
                rv = cur.fetchall()
            cur.close()
            return rv
        except pg.errors as error:
            print(f"Error: {error}")

    def add_review(self, id: str, isbn: str, book_rating: str):
        """
        Add a rating to the ratings database
        :param id: the id of the user entering the rating
        :param isbn: the isbn of the book being rated
        :param book_rating: the rating of the book (0-10)
        :return: None
        """
        try:
            cur = self.conn.cursor()
            cmd = """
                INSERT INTO ratings (user_id, isbn, rating) VALUES (%s, %s, %s);
                """
            cur.execute(cmd, [id.strip(), isbn.strip(), book_rating.strip()])
            self.conn.commit()
            print ("Rating Added")
        except pg.errors.UniqueViolation:
            print ("You have already submitted this rating")
        except pg.errors.ForeignKeyViolation:
            print ("Invalid ISBN or User")
        except pg.errors.InFailedSqlTransaction:
            print ("Violated database constraints: numerics are not letters and vice versa")
        except pg.errors as error:
            print(f"Error: {error}")

    def get_avg_by_title_author(self, author: str, title: str):
        try:
            """
            Return rating by title and author
            :param connection: DB Connection
            :param title: Book Title
            :param author: Book Author
            :return:
            """
            cur = self.conn.cursor()
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

            rv = None
            if cur.rowcount > 0:
                rv = cur.fetchall()
            cur.close()
            return rv
        except pg.errors as error:
            print(f"Error: {error}")