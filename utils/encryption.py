from cryptography.fernet import fernet
KEY = Fernet.generate_key()
fernet = Fernet(KEY)

def encrypt_bytes(data: bytes) -> bytes:
    return fernet.encrypt(data)

def decrypt_bytes(token: bytes) -> bytes:
    return fernet.decrypt(token)
