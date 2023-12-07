from customer import Customer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


class CustomerFireStore(Customer):

    def __init__(self):
        base_dir = "/Users/jaxlub/Documents/GitHub"
        priv_key = "jalubk20-cs345fall22-firebase-adminsdk-xus9l-f9dc5a887b.json"

        cred = credentials.Certificate(f'{base_dir}/{priv_key}')
        firebase_admin.initialize_app(cred)

        # reference to firestore DB
        db = firestore.client()
        # Create a CC collections
        self.coll = db.collection("CreditCards")

        with open('../../../key.txt', 'r') as f:
            str_key = (f.readline().strip()) * 2
            self.key = bytes.fromhex(str_key)

        with open('../../../iv.txt', 'r') as f:
            str_iv = (f.readline().strip()) * 2
            self.iv = bytes.fromhex(str_iv)

    def lookup(self, cid: int) -> dict:
        docs = self.coll.where("cid", "==", cid).stream()
        for doc in docs:

            cc_encr = doc.to_dict()["info"]
            decrypted = self.decrypt(cc_encr, self.key, self.iv)
        ccjson = {
            "cid": cid,
            "info": decrypted
        }
        return ccjson

    def create_table(self):
        pass

    def delete(self, cid: int) -> None:
        doc_ref = self.coll.document(str(cid))
        doc_ref.delete()

    def insert(self, cid: int, first: str, last: str, ccnum: str, ccexp: str, cvv: str):
        ccjson = {
            'name': first + ' ' + last,
            'ccnum': ccnum,
            'ccexp': ccexp,
            'cvv': cvv
        }
        # converting object to string and then string to bytes
        ccdata_bytes = json.dumps(ccjson).encode()

        encoded = self.encrypt(ccdata_bytes, self.key, self.iv)

        doc_ref = self.coll.document(str(cid))
        doc_ref.set(
            {
                "cid": cid,
                "info": encoded
            }
        )

    def encrypt(self, cc_data_bytes, key, iv) -> bytes:
        aesCipher = Cipher(algorithms.AES(key), modes.CTR(iv))
        aesEncryptor = aesCipher.encryptor()

        # Encode bytes and fill the rest of the block with finalize - result in binary
        ciphertext = aesEncryptor.update(cc_data_bytes) + aesEncryptor.finalize()

        # convert to text from binary
        b64ct = base64.b64encode(ciphertext)
        return b64ct

    def decrypt(self, cc_data_bytes, key, iv) -> str:
        cc_decode = base64.b64decode(cc_data_bytes)
        aesCipher = Cipher(algorithms.AES(self.key), modes.CTR(self.iv))
        aesDecryptor = aesCipher.decryptor()

        # Decrypt the ciphertext
        decrypted_bytes = aesDecryptor.update(cc_decode) + aesDecryptor.finalize()
        return(decrypted_bytes.decode())
