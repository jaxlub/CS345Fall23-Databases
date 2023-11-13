from parts import *  # dangerous if name collisions of global variables
from suppliers import *
import sqlite3 as sq
import csv


class PartsAndSuppliers:
    def __init__(self, rebuild: bool = False):
        self.conn = sq.connect('parts.db')
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.parts = Parts(self.conn)
        self.suppliers = Suppliers(self.conn)

        self.conn.commit()

        # TODO

        if rebuild:
            # recreate parts table
            self.parts.drop_table()
            self.parts.create_table()
            self.load_table("parts.csv", Parts.iit)

            # recreate suppliers table
            self.suppliers.drop_table()
            self.suppliers.create_table()
            self.load_table("suppliers.csv", Suppliers.iit)

    def load_table(self, fname: str, iit):
        # Context manager
        with open(fname) as f:
            # f = open("parts.csv") and automatically closes the file when done
            reader = csv.reader(f, skipinitialspace=True)
            self.conn.executemany(iit, list(reader))
            self.conn.commit()
