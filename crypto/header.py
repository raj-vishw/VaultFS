import os
import struct
from .kdf import derive_kek
from .keys import generate_master_key
from .crypto_utils import aes_gcm_decrypt, aes_gcm_encrypt

MAGIC = b"RXJVAULT"
VERSION= 1

def create_header(password: str) -> bytes:
    salt = os.urandom(16)
    kek = derive_kek(password, salt)

    master_key = generate_master_key()
    nonce, enc_mk, tag = aes_gcm_encrypt(kek, master_key)
    
    header = (
        MAGIC + struct.pack("B",VERSION) +
        salt + 
        struct.pack(">III",3,65536,4) +
        nonce +
        enc_mk +
        tag  
    )
    return header
    