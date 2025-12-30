import os
import hmac
import hashlib

def generate_master_key() -> bytes:
    return os.urandom(32)

def derive_subkeys(master_key: bytes) -> dict:
    def h(label: bytes):
        return hmac.new(master_key, label, hashlib.sha256).digest()

    return{
        "KeyA": h(b"AUTH"),
        "KeyB": h(b"DATA"),
        "KeyC": h(b"META"),
    }