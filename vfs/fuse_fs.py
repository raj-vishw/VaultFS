import os, errno
from fuse import FUSE, Operations
from vault.tokens import path_to_token
from vault.layout import file_dir
from vault.chunks import decrypt_file_chunks, encrypt_file_chunks

class VaultFS(Operations):
    def __init__(self, state):
        self.state = state

    def getattr(self, path, fh=None):
        if path == "/":
            return dict(st_mode=(0o755 | 0o040000), st_nlink=2)

        rel = path.lstrip("/")
        if rel in self.state.meta["files"]:
            info = self.state.meta["files"][rel]
            return dict(
                st_mode=(0o644 | 0o100000),
                st_size=info["size"],
                st_nlink=1
            )

        raise OSError(errno.ENOENT)

    def readdir(self, path, fh):
        yield "."
        yield ".."
        for p in self.state.meta["files"].keys():
            yield p.split("/")[-1]

    def open(self, path, flags):
        return 0

    def read(self, path, size, offset, fh):
        rel = path.lstrip("/")
        info = self.state.meta["files"][rel]

        temp = "/tmp/.vault_read"
        decrypt_file_chunks(
            self.state.keys["KeyB"],
            file_dir(self.state.vault, info["token"]),
            temp
        )

        with open(temp, "rb") as f:
            f.seek(offset)
            data = f.read(size)

        os.unlink(temp)
        return data

    def write(self, path, data, offset, fh):
        rel = path.lstrip("/")

        temp = "/tmp/.vault_write"
        with open(temp, "ab") as f:
            f.seek(offset)
            f.write(data)

        token = path_to_token(self.state.keys["KeyC"], rel)
        outdir = file_dir(self.state.vault, token)

        chunks = encrypt_file_chunks(self.state.keys["KeyB"], temp, outdir)

        self.state.meta["files"][rel] = {
            "token": token,
            "chunks": chunks,
            "size": os.path.getsize(temp)
        }

        os.unlink(temp)
        return len(data)
