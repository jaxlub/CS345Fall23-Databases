import psycopg2 as pg
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


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
        cur = self.conn.cursor()
        cur.execute(Customer.CT)
        self.conn.commit()
        cur.close()

    def insert(self, cid: int, first: str, last: str, ccnum: str, ccexp: str, cvv: str):
        # Python dictionary = Json object
        # Python dictionary is key/value pairs

        ccjson = {
            'name': first + ' ' + last,
            'ccnum': ccnum,
            'ccexp': ccexp,
            'cvv': cvv
        }

        # converting object to string and then string to bytes
        ccdata_bytes = json.dumps(ccjson).encode()

        # encrypt cc data
        # insecure method
        key = bytes.fromhex('1234567890abcdef' * 2)

        # seed for built-in randomness for AES (initialization vector)
        iv = bytes.fromhex('0987654321fedcba' * 2)

        aesCipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        aesEncryptor = aesCipher.encryptor()

        # Encode bytes and fill the rest of the block with finalize - result in binary
        ciphertext = aesEncryptor.update(ccdata_bytes) + aesEncryptor.finalize()

        # convert to text from binary
        b64ct = base64.b64encode(ciphertext)

        cur = self.conn.cursor()
        cur.execute(Customer.INS, (cid, b64ct))
        self.conn.commit()
        cur.close()





    def lookup(self, cid: int) -> str:
        pass
