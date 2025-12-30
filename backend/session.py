import time

class VaultSession:
    def __init__(self, timeout=300):
        self.start = time.time()
        self.timeout = timeout

    def expired(self):
        return time.time() - self.start > self.timeout

    def refresh(self):
        self.start = time.time()
