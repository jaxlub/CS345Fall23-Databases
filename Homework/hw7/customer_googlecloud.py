import psycopg2 as pg
from customer import Customer
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


class CustomerGoogleCloud(Customer):
    HOST = '34.118.200.180'
    CT = """
        CREATE TABLE IF NOT EXISTS customer (
            id int not null,
            ccinfo text, -- encrypted cc info in base 64
            PRIMARY KEY (id));
    """
    INS = "INSERT INTO customer VALUES(%s,%s)"
    LU = "Select * FROM customer where id = %s"
    D = "DELETE FROM customer where id = %s"

    def __init__(self):
        with open('../../../pgpass.txt', 'r') as f:
            self.conn = pg.connect(
                host=CustomerGoogleCloud.HOST,
                user='jalubk',
                dbname='jalubk',
                password=f.readline().strip()
            )

        with open('../../../key.txt', 'r') as f:
            str_key = (f.readline().strip()) * 2
            self.key = bytes.fromhex(str_key)

        with open('../../../iv.txt', 'r') as f:
            str_iv = (f.readline().strip()) * 2
            self.iv = bytes.fromhex(str_iv)


    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(CustomerGoogleCloud.CT)
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
        encoded = self.encrypt(ccdata_bytes, self.key, self.iv)

        cur = self.conn.cursor()
        cur.execute(CustomerGoogleCloud.INS, (cid, encoded))
        self.conn.commit()
        cur.close()

    def lookup(self, cid: int) -> dict:
            cur = self.conn.cursor()
            cur.execute(CustomerGoogleCloud.LU, [cid])
            rv = None
            if cur.rowcount > 0:
                rv = cur.fetchone()
                removed = rv[1]
                #removed = removed[2:]
                decrypted = self.decrypt(removed, self.key, self.iv)


                ccjson = json.loads(decrypted)
            return ccjson


    def delete(self, cid: int) -> None:
        cur = self.conn.cursor()
        cur.execute(CustomerGoogleCloud.D, [cid])
        cur.close()
        return None


    def encrypt(self, cc_data_bytes, key, iv) -> bytes:
        aesCipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        aesEncryptor = aesCipher.encryptor()

        # Encode bytes and fill the rest of the block with finalize - result in binary
        ciphertext = aesEncryptor.update(cc_data_bytes) + aesEncryptor.finalize()

        # convert to text from binary
        b64ct = base64.b64encode(ciphertext)
        b64str = b64ct.decode('UTF-8')
        return b64str

    def decrypt(self, cc_data_bytes, key, iv) -> str:

        cc_decode = base64.b64decode(cc_data_bytes)
        aesCipher = Cipher(algorithms.AES(self.key), modes.CTR(self.iv))
        aesDecryptor = aesCipher.decryptor()

        # Decrypt the ciphertext
        decrypted_bytes = aesDecryptor.update(cc_decode) + aesDecryptor.finalize()
        return (decrypted_bytes.decode())
