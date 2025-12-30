import sys, os
from fuse import FUSE
from crypto.header import unlock_header
from crypto.keys import derive_subkeys
from vault.metadata import load_metadata
from vfs.state import VaultState
from vfs.fuse_fs import VaultFS

vault = sys.argv[1]
mountpoint = sys.argv[2]

password = input("Vault password: ")

header = open(os.path.join(vault, "header.bin"), "rb").read()
master = unlock_header(password, header)
keys = derive_subkeys(master)

meta = load_metadata(os.path.join(vault, "metadata", "metadata.enc"), keys["KeyC"])
state = VaultState(vault, keys, meta)

FUSE(VaultFS(state), mountpoint, foreground=True)
