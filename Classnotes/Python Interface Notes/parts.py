import sqlite3 as sq
import csv


class Parts:
    # class data
    # Common SQL commands for parts table
    dt = "DROP TABLE IF EXISTS parts"

    ct = """CREATE TABLE IF NOT EXISTS parts(
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                color text NOT NULL,
                                weight real NOT NULL,
                                city text NOT NULL)"""

    iit = """
            INSERT INTO parts VALUES (?,?,?,?,?)
         """

    def __init__(self, conn: sq.Connection):
        self.conn = conn

    def create_table(self):
        self.conn.execute(Parts.ct)
        self.conn.commit()



    def drop_table(self):
        self.conn.execute(Parts.dt)
        self.conn.commit()

    # Functions/Queries that are specific to parts table

if __name__ == '__main__':
    db = Parts()
    db.create_table()
    db.load_parts()
