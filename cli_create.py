from crypto.header import create_header

password = input("Set Vault Password")
header = create_header(password)

with open("header.bin", "wb") as f:
    f.write(header)

print("Vault header created")

