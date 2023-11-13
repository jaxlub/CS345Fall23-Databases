import sqlite3 as sq
import csv


class Suppliers:
    dt = "DROP TABLE IF EXISTS suppliers"

    ct = """CREATE TABLE IF NOT EXISTS suppliers(
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status integer NOT NULL,
                                city text NOT NULL)"""
    iit = """
            INSERT INTO suppliers VALUES (?,?,?,?)
         """

    def __init__(self, conn: sq.Connection):
        self.conn = conn

    def create_table(self):

        self.conn.execute(Suppliers.ct)
        self.conn.commit()

    def drop_table(self):
        self.conn.execute(Suppliers.dt)
        self.conn.commit()
    # Functions/Queries that are specific to suppliers table


if __name__ == '__main__':
    db = Suppliers()
    db.create_table()

