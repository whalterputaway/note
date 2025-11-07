import secrets
import configparser


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))


def encrypt_with_master(plaintext: str, master_key: bytes):
    file_key = secrets.token_bytes(32)
    encrypted_text = xor_bytes(plaintext.encode(), file_key)
    encrypted_file_key = xor_bytes(file_key, master_key)
    mass = [encrypted_text, encrypted_file_key]
    return mass

def decrypt_with_master(encrypted_text: bytes, encrypted_file_key: bytes, master_key: bytes):
    file_key = xor_bytes(encrypted_file_key, master_key)
    decrypted_text = xor_bytes(encrypted_text, file_key)
    return decrypted_text.decode()
