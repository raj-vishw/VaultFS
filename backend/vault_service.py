import os
from crypto.header import create_header
from mount import mount_vault, unmount_vault

def create_vault(path, password):
    os.makedirs(path, exist_ok=True)
    header = create_header(password)
    with open(os.path.join(path, "header.bin"), "wb") as f:
        f.write(header)
    os.makedirs(os.path.join(path, "files"))
    os.makedirs(os.path.join(path, "metadata"))
    os.makedirs(os.path.join(path, "journal"))

def unlock_vault(vault_path, mountpoint, password):
    mount_vault(vault_path, mountpoint, password)

def lock_vault(mountpoint):
    unmount_vault(mountpoint)
