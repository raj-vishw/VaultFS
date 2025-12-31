# 🔐 Modern Encrypted File Vault
# 🔐 VaultFS

A **zero-knowledge, cross-platform encrypted file vault** inspired by **Cryptomator**, **gocryptfs**, and **VeraCrypt (filesystem mode)**.

This project implements a **modern cryptographic architecture** with per-file encryption, encrypted metadata, and a mountable virtual filesystem, built step by step with security-first principles.

---

## ✨ Features

### 🔑 Zero-Knowledge Architecture

- Password is never stored
    
- Vault contents cannot be decrypted without the password
    

### 🔐 Strong Cryptography

- Argon2id (password-based key derivation)
    
- AES-256-GCM (authenticated encryption)
    
- Strict key separation (Auth / Data / Metadata)
    

### 📂 Per-File & Per-Chunk Encryption

- Fixed-size chunking (cloud-sync friendly)
    
- Corruption isolation (one file ≠ entire vault)
    

### 🕶️ Encrypted Filenames & Metadata

- No plaintext filenames
    
- No plaintext directory structure
    
- No metadata leakage
    

### 🗂️ Mountable Virtual Filesystem

- Linux: FUSE
    
- Windows: WinFsp (design-compatible)
    
- Files decrypted only in memory
    

### 🖥️ Secure Application Layer

- Clean UI
    
- Auto-lock
    
- Session management
    
- Password policy enforcement
    

### 🛡️ Hardened for Real-World Threats

- Secure memory wiping
    
- Encrypted journaling
    
- Atomic writes
    
- Garbage collection
    
- Key rotation support
    
---

📐 Architecture Overview

User Application
     ↓
GUI (HTML/CSS)
     ↓
Backend Service (app.py)
     ↓
Virtual Filesystem (FUSE / WinFsp)
     ↓
Encrypted Vault (Chunks + Metadata)
     ↓
Disk (Fully Encrypted, Zero Knowledge)

---

## 🔑 Cryptographic Model

|Component|Algorithm|
|---|---|
|Password KDF|Argon2id|
|Master Key|256-bit random|
|File Encryption|AES-256-GCM|
|Metadata Encryption|AES-256-GCM|
|Filename Tokens|HMAC-SHA256|
|Integrity|GCM Authentication Tags|

### Key Separation

- **KeyA** → Authentication / audit
    
- **KeyB** → File content encryption
    
- **KeyC** → Metadata & filename encryption
    


## 🚀 Getting Started

### Prerequisites

- Python 3.10+
    
- Linux with FUSE support
    
- pip
    

### Install Dependencies

`sudo apt install fuse pip install flask fusepy cryptography argon2-cffi`

### Run the Application

`python app.py`

Open in your browser:

`http://127.0.0.1:8080`

---

## 🔐 Security Guarantees

- Disk theft resistance
    
- Password brute-force resistance
    
- Metadata confidentiality
    
- Crash-safe writes
    
- Cloud-safe design
    
- Minimized memory exposure
    
---

## 📜 License

MIT License

---

## 🧠 Disclaimer

This project is built for **educational and research purposes**.
While it follows industry best practices, it has not undergone a formal security audit.

Use at your own risk.

---

⭐ Final Note

This project demonstrates a real-world, production-grade approach to encrypted storage.

If you’re reviewing this as a recruiter or security engineer:

        This system was designed end-to-end with correct cryptographic reasoning.
