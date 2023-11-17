import psycopg2 as pg
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Customer:
    HOST = '34.118.200.180'
    CT = """
        CREATE TABLE IF NOT EXISTS customer (
            id int not null,
            ccinfo text, -- encrypted cc info in base 64
            PRIMARY KEY (id));
    """
    INS = "INSERT INTO customer VALUES(%s,%s)"
    def __init__(self):
        with open('../pgpass.txt', 'r') as f:
            self.conn = pg.connect(
                host=Customer.HOST,
                user='jalubk',
                dbname='jalubk',
                password=f.readline().strip()
            )

    def create_table(self):
        self.conn.execute(Customer.CT)
        self.conn.commit()

    def insert(self, cid: int, first: str, last: str, ccnum: str, ccexp: str, cvv: str):
        # Python dictionary = Json object
        # Python dictionary is key/value pairs

        ccjson = {
            'name': first + ' ' + last,
            'ccnum': ccnum,
            'ccexp': ccexp,
            'cvv': cvv
        }
        ccdata_bytes = json.dumps(ccjson).encode()

        # encrypt cc data
        # insecure method
        key = bytes.fromhex('1234567890abcdef' * 2)

        # seed for built-in randomness for AES (initialization vector)
        iv = bytes.fromhex('0987654321fedcba' * 2)

        aesCipher = Cipher(algorithms.AES(key), modes.CTR(iv))





    def lookup(self, cid: int) -> str:
        pass
