import sys, os
from crypto.header import unlock_header
from crypto.keys import derive_subkeys
from vault.metadata import load_metadata
from vault.layout import file_dir
from vault.chunks import decrypt_file_chunks

vault = sys.argv[1]
relpath = sys.argv[2]
outfile = sys.argv[3]

password = input("Vault password: ")

header = open(os.path.join(vault, "header.bin"), "rb").read()
master = unlock_header(password, header)
keys = derive_subkeys(master)

meta = load_metadata(os.path.join(vault, "metadata", "metadata.enc"), keys["KeyC"])
info = meta["files"][relpath]

decrypt_file_chunks(
    keys["KeyB"],
    file_dir(vault, info["token"]),
    outfile
)

print("✔ File extracted")
