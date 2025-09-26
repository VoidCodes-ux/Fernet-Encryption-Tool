"""
Fernet Batch Encryption Tool
----------------------------
A Python tool for encrypting and decrypting multiple messages at once
using Fernet symmetric encryption (from the cryptography library).

Features:
- Generate and save a secure encryption key
- Encrypt multiple messages in batch mode
- Save encrypted messages to file
- Decrypt all saved messages back to plaintext
- Regenerate key if needed (WARNING: old messages won't decrypt)

Author: Your Name
GitHub: https://github.com/VoidCodes-ux/Fernet-Encryption-Tool
"""

from cryptography.fernet import Fernet
import os

KEY_FILE = "data/secret.key"
STORAGE_FILE = "data/messages.enc"


# ----------------- KEY MANAGEMENT -----------------
def generate_key():
    """Generate and save a new Fernet key."""
    os.makedirs("data", exist_ok=True)
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"[+] New key generated and saved to {KEY_FILE}")
    return key


def load_key():
    """Load an existing key from file."""
    if not os.path.exists(KEY_FILE):
        print("[!] No key found. Generate one first.")
        return None
    with open(KEY_FILE, "rb") as f:
        return f.read()


# ----------------- BATCH ENCRYPTION -----------------
def encrypt_messages(cipher):
    print("\nEnter multiple messages (type 'done' when finished):")
    messages = []
    while True:
        msg = input("> ")
        if msg.lower() == "done":
            break
        messages.append(msg)

    encrypted_messages = [cipher.encrypt(m.encode()).decode() for m in messages]

    os.makedirs("data", exist_ok=True)
    with open(STORAGE_FILE, "w") as f:
        for enc in encrypted_messages:
            f.write(enc + "\n")

    print(f"\n[+] {len(messages)} messages encrypted and saved to {STORAGE_FILE}")
    for i, enc in enumerate(encrypted_messages, 1):
        print(f"{i}) {enc}")


def decrypt_messages(cipher):
    if not os.path.exists(STORAGE_FILE):
        print("[!] No encrypted messages found.")
        return

    with open(STORAGE_FILE, "r") as f:
        encrypted_messages = [line.strip() for line in f if line.strip()]

    decrypted_messages = []
    for enc in encrypted_messages:
        try:
            dec = cipher.decrypt(enc.encode()).decode()
            decrypted_messages.append(dec)
        except Exception:
            decrypted_messages.append("[Decryption failed]")

    print(f"\n🔓 Decrypted {len(decrypted_messages)} messages:")
    for i, dec in enumerate(decrypted_messages, 1):
        print(f"{i}) {dec}")


# ----------------- MAIN MENU -----------------
def main():
    if os.path.exists(KEY_FILE):
        key = load_key()
        print(f"[+] Loaded key from {KEY_FILE}")
    else:
        key = generate_key()

    cipher = Fernet(key)

    while True:
        print("\n--- Fernet Batch Tool ---")
        print("1) Encrypt multiple messages/sayings")
        print("2) Decrypt all saved messages")
        print("3) Generate a new key (WARNING: old data won't decrypt)")
        print("4) Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            encrypt_messages(cipher)
        elif choice == "2":
            decrypt_messages(cipher)
        elif choice == "3":
            key = generate_key()
            cipher = Fernet(key)
        elif choice == "4":
            print("Goodbye 👋")
            break
        else:
            print("[!] Invalid choice. Try again.")


if __name__ == "__main__":
    main()
