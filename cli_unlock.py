import sys
from crypto.header import unlock_header
from crypto.keys import derive_subkeys
from crypto.crypto_utils import aes_gcm_decrypt
from vault.vault_format import read_vault
from vault.unpack import unpack_archive

vault_file = sys.argv[1]
output_dir = sys.argv[2]

password = input("Vault password: ")

header, nonce, ct, tag = read_vault(vault_file)
master_key = unlock_header(password, header)
keys = derive_subkeys(master_key)

archive = aes_gcm_decrypt(keys["KeyB"], nonce, ct, tag)
unpack_archive(archive, output_dir)

print("✔ Vault unlocked into:", output_dir)
