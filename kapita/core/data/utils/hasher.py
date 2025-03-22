import binascii
import hashlib
import os
from random import SystemRandom


class Hasher:
    """Hasher."""

    random = SystemRandom()

    @staticmethod
    def parse_hash(hash: str) -> tuple[str, bytes, str, int]:
        """parse_hash.

        :param hash:
        :type hash: str
        :rtype: tuple[str, str, str, int]
        """
        algorithm, hash_data, salt, iterations = hash.split(":")

        return algorithm, binascii.unhexlify(hash_data.encode()), salt, int(iterations)

    @classmethod
    def hash(cls, value: str, algorithm: str = "blake2b") -> str:
        """hash.

        :param value:
        :type value: str
        :rtype: str
        """
        salt = binascii.hexlify(os.urandom(32)).decode()
        iterations = 100000
        hash_data = binascii.hexlify(
            hashlib.pbkdf2_hmac(algorithm, value.encode(), salt=salt.encode(), iterations=iterations)
        ).decode()

        return f"{algorithm}:{hash_data}:{salt}:{iterations}"

    @classmethod
    def verify(cls, value: str, hash: str) -> bool:
        """Verify hash.

        :param value:
        :param hash:
        :type value: str
        :type hash: str
        :rtype: str
        """
        algorithm, hash_data, salt, iterations = cls.parse_hash(hash)

        verify_data = hashlib.pbkdf2_hmac(algorithm, value.encode(), salt=salt.encode(), iterations=iterations)

        return hash_data == verify_data
