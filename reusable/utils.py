import base64
from uuid import UUID
from cryptography.fernet import Fernet


def encrypt_message(message, secret_key: UUID):
    secret_key = str(secret_key).replace('-', '')
    secret = base64.urlsafe_b64encode(secret_key.encode())
    fernet = Fernet(secret)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message.decode()


def decrypt_message(encrypted_message, secret_key: UUID):
    secret_key = str(secret_key).replace('-', '')
    secret = base64.urlsafe_b64encode(secret_key.encode())
    fernet = Fernet(secret)
    decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()
    return decrypted_message
