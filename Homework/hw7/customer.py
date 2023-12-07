from abc import ABC, abstractmethod
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

# define customer interface
class Customer(ABC):

    @abstractmethod
    def lookup(self, cid: int) -> dict:
        """
        Return decrypted CC infor
        :param cid:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def insert(self, cid: int, first: str, last: str, ccnum: str, ccexp: str, cvv: str):
        """
        Insert encrypted ccinfo into DB
        :param cid:
        :param first:
        :param last:
        :param ccnum:
        :param ccexp:
        :param cvv:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, cid: int) -> None:
        """
        Delete customer
        :param cid:
        :return:
        """
        raise NotImplementedError


    @abstractmethod
    def create_table(self):
        """
        Create customer database
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def encrypt(self, cc_data_bytes, key, iv) -> bytes:
        """
        Encrypt CC info
        :param cc_data_bytes:
        :param key:
        :param iv:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def decrypt (self, cc_data_bytes, key, iv) -> str:
        """
        Decrypt CC info
        :param cc_data_bytes:
        :param key:
        :param iv:
        :return:
        """
        raise NotImplementedError
