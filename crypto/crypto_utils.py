from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def aes_gcm_encrypt(key:bytes, data: bytes) -> tuple:
    nonce= os.urandom(12)
    aes= AESGCM(key)
    ciphertext= aes.encrypt(nonce, data, None)
    return nonce, ciphertext[:-16], ciphertext[-16:]

def aes_gcm_decrypt(key: bytes, nonce:bytes, ct:bytes, tag: bytes) -> bytes:
    aes = AESGCM(key)
    return aes.decrypt(nonce, ct + tag, None) 