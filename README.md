## crypto-vault

### Overview

crypto-vault is a simple password storage and management tool focused on providing basic cryptographic operations. It can help you securely store sensitive information such as passwords, secrets, and other sensitive data.

### Installation

To install crypto-vault, you will need Python 3.6 or later and the following dependencies:

- cryptography
- argparse
- logging

You can install these dependencies using pip:

```
pip install cryptography argparse logging
```

Once the dependencies are installed, you can install crypto-vault from PyPI:

```
pip install crypto-vault
```

### Usage

To use crypto-vault, simply run the following command:

```
crypto-vault
```

This will open the interactive command-line interface (CLI) for crypto-vault. From the CLI, you can perform the following operations:

- **Encrypt a file:** Encrypt a file using AES-256 encryption.
- **Decrypt a file:** Decrypt a file that was previously encrypted using crypto-vault.
- **View encrypted files:** List the encrypted files that are stored in the current directory.
- **Delete encrypted files:** Delete an encrypted file from the current directory.

For more information on how to use crypto-vault, please refer to the usage examples below.

### Usage Examples

**Encrypt a file:**

```
crypto-vault encrypt file.txt
```

**Decrypt a file:**

```
crypto-vault decrypt file.txt.enc
```

**View encrypted files:**

```
crypto-vault ls
```

**Delete encrypted files:**

```
crypto-vault rm file.txt.enc
```

### Security Warnings

crypto-vault is a simple password storage and management tool and should not be used to store highly sensitive information. It is important to note that the security of your data depends on the strength of your password. Please choose a strong password that is not easily guessable.

### License

crypto-vault is licensed under the GNU General Public License v3.0 to CY83R-3X71NC710N.