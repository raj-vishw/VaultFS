import sys, os
from crypto.header import unlock_header
from crypto.keys import derive_subkeys
from vault.tokens import path_to_token
from vault.chunks import encrypt_file_chunks
from vault.metadata import load_metadata, save_metadata
from vault.layout import file_dir

vault = sys.argv[1]
filepath = sys.argv[2]
relpath = sys.argv[3]

password = input("Vault password: ")

header = open(os.path.join(vault, "header.bin"), "rb").read()
master = unlock_header(password, header)
keys = derive_subkeys(master)

token = path_to_token(keys["KeyC"], relpath)
outdir = file_dir(vault, token)

chunks = encrypt_file_chunks(keys["KeyB"], filepath, outdir)

meta_path = os.path.join(vault, "metadata", "metadata.enc")
meta = load_metadata(meta_path, keys["KeyC"])

meta["files"][relpath] = {
    "token": token,
    "chunks": chunks,
    "size": os.path.getsize(filepath)
}

save_metadata(meta_path, keys["KeyC"], meta)

print("✔ File added to vault")
