import sys
from crypto.header import create_header, unlock_header
from crypto.keys import derive_subkeys
from vault.pack import pack_folder
from vault.vault_format import write_vault

folder = sys.argv[1]
vault_file = sys.argv[2]

password = input("Vault password: ")

header = create_header(password)
master_key = unlock_header(password, header)
keys = derive_subkeys(master_key)

archive = pack_folder(folder)
write_vault(vault_file, header, keys["KeyB"], archive)

print("Vault created:", vault_file)
