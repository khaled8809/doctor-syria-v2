from base64 import b64decode, b64encode

from cryptography.fernet import Fernet
from django.conf import settings


class DataEncryption:
    def __init__(self):
        self.key = (
            settings.ENCRYPTION_KEY.encode()
            if hasattr(settings, "ENCRYPTION_KEY")
            else Fernet.generate_key()
        )
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data):
        """تشفير البيانات"""
        try:
            if isinstance(data, str):
                encrypted_data = self.cipher_suite.encrypt(data.encode())
                return b64encode(encrypted_data).decode()
            raise ValueError("Data must be a string")
        except Exception as e:
            raise Exception(f"Encryption error: {str(e)}")

    def decrypt_data(self, encrypted_data):
        """فك تشفير البيانات"""
        try:
            if isinstance(encrypted_data, str):
                decrypted_data = self.cipher_suite.decrypt(b64decode(encrypted_data))
                return decrypted_data.decode()
            raise ValueError("Encrypted data must be a string")
        except Exception as e:
            raise Exception(f"Decryption error: {str(e)}")
