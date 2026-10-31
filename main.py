import os
import sys
import logging
from cryptography.fernet import Fernet
import argparse


# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("crypto-vault")


# Generate or load encryption key
def load_or_generate_key():
    key_file = "crypto_vault.key"
    if os.path.exists(key_file):
        # The key decrypts every saved password, so a key file that
        # group or other users can read is tightened to owner only
        # before it is used. If tightening fails, say so plainly
        # instead of loading a readable key in silence.
        try:
            mode = os.stat(key_file).st_mode
            if mode & 0o077:
                os.chmod(key_file, 0o600)
                logger.warning(
                    "Encryption key file had group or other permissions set; tightened it to owner only (0600)."
                )
        except OSError as e:
            logger.warning(
                "Encryption key file is readable by group or other users and could not be tightened to 0600: %s. Restrict its permissions by hand.", e
            )
        with open(key_file, "rb") as file:
            key = file.read()
            logger.info("Encryption key loaded.")
    else:
        key = Fernet.generate_key()
        # Create the key file owner only from the start: a plain open
        # leaves it at the process default, which can be group or
        # world readable.
        fd = os.open(key_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as file:
            file.write(key)
            logger.info("New encryption key generated and saved.")
    return key


# Encrypt password
def encrypt_password(key, password):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    logger.info("Password encrypted successfully.")
    return encrypted


# Decrypt password
def decrypt_password(key, encrypted_password):
    try:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_password).decode()
        logger.info("Password decrypted successfully.")
        return decrypted
    except Exception as e:
        logger.error("Decryption failed: %s", e)
        raise


# Save encrypted password to file
def save_password(filename, encrypted_password):
    with open(filename, "wb") as file:
        file.write(encrypted_password)
        logger.info("Encrypted password saved to file: %s", filename)


# Load encrypted password from file
def load_password(filename):
    if not os.path.exists(filename):
        logger.error("Password file does not exist: %s", filename)
        raise FileNotFoundError("Password file not found.")
    with open(filename, "rb") as file:
        encrypted_password = file.read()
        logger.info("Encrypted password loaded from file: %s", filename)
    return encrypted_password


# Setup command line interface
def setup_argparse():
    parser = argparse.ArgumentParser(description="Crypto Vault - Simple password storage and management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt and save a password")
    encrypt_parser.add_argument("password", type=str, help="Password to encrypt")
    encrypt_parser.add_argument("filename", type=str, help="File to save the encrypted password")

    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt and retrieve a password")
    decrypt_parser.add_argument("filename", type=str, help="File containing the encrypted password")

    return parser


# Main function
def main():
    try:
        parser = setup_argparse()
        args = parser.parse_args()

        if args.command == "encrypt":
            key = load_or_generate_key()
            encrypted_password = encrypt_password(key, args.password)
            save_password(args.filename, encrypted_password)
            print("Password encrypted and saved successfully.")

        elif args.command == "decrypt":
            # Load the token before touching the key: the old order ran
            # load_or_generate_key first, so a decrypt of a missing file
            # in a fresh directory still created a crypto_vault.key as
            # a side effect of a run that only failed.
            encrypted_password = load_password(args.filename)
            key = load_or_generate_key()
            decrypted_password = decrypt_password(key, encrypted_password)
            print("Decrypted password:", decrypted_password)

    except Exception as e:
        logger.error("An error occurred: %s", e)
        sys.exit(1)


# Entry point
if __name__ == "__main__":
    main()