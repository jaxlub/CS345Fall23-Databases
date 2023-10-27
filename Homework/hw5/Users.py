import psycopg as pg

class Users:
    def __init__(self, conn: pg.Connection):
        self.conn = conn
    def add_user(self, new_id: str, location: str, age: str):
        """
        Add a new user
        :param new_id: User ID
        :param location: User Location
        :param age: User age
        :return: Message of result
        """
        try:
            cur = self.conn.cursor()
            # Open to SQL Injection
            # print(add_user(conn, "SQLInjTest", "Vermont", "28); INSERT into users VALUES ('Injected', 'Success', '100')

            #SQLInjTest
            #Vermont
            #28),('Injected', 'Success', '100'
            cmd ="INSERT INTO users(id, location, age) VALUES (%s, %s," + age + ");"
            cur.execute(cmd, [new_id.strip(), location.strip()])
            self.conn.commit()
            print("User Added")
        except pg.errors.UndefinedColumn as error:
            print(f"Error: {error}")
        except pg.errors.UniqueViolation as error:
            print(f"Error: {error}")


    def avg_rating_most_reviews_user(self) -> int | None:
        try:
            """
            Find the avg rating of the user with the most reviews
            :return: Avg. Review Score
            """
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
            cur = self.conn.cursor()
            cur.execute(cmd)

            rv = None
            if cur.rowcount > 0:
                rv = cur.fetchone()[0]
            cur.close()  # context manager
            return rv
        except pg.errors as error:
            print(f"Error: {error}")