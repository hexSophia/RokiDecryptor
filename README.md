# RokiDecryptor

RokiDecryptor is a Proof-of-Concept (PoC) repository showcasing a set of tools for data encryption, decryption, and network-based administrative operations. This project combines AutoIt and Python to demonstrate cryptographic operations, password management, and remote execution functionalities in a local network environment.

## Features

### Encryptor.au3
- Command-line utility to perform AES-256 encryption and decryption.
- Uses AutoIt's `Crypt` library for secure data operations.
- Supports encrypting and decrypting data with a provided key.

### Decrypter.py
- Python script for managing encrypted credentials stored in a configuration file (`Roki.setting`).
- Encrypts and decrypts sensitive information using the `Encryptor.au3` script.
- Allows updating and managing credentials securely.

### SendTag.py
- Python-based network administration script.
- Features:
  - Scans the local network for reachable IPs.
  - Tests remote administrative access using provided credentials.
  - Supports file transfer to remote systems using `robocopy`.
  - Enables remote command execution using PsExec.

## Installation

### Prerequisites
- Windows operating system
- AutoIt installed for compiling and running `.au3` scripts
- Python 3.x installed
- Required Python packages:
  - `subprocess`
  - `configparser`
  - `netifaces`
  - `concurrent.futures`
- PsExec (part of Sysinternals) downloaded and placed in the project directory

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/hexSophia/RokiDecryptor.git
   cd RokiDecryptor
   ```
2. Install required Python packages:
   ```bash
   pip install netifaces
   ```
3. Configure the `Roki.setting` file to include encrypted credentials.
4. Compile `Encryptor.au3` to an executable using AutoIt.

## Usage

### Encryptor.au3
```bash
Encryptor.exe [encrypt|decrypt] <data> <key>
```
Example:
```bash
Encryptor.exe encrypt "my_secret_data" "my_key"
```

### Decrypter.py
Run the script to manage encrypted credentials:
```bash
python decrypter.py
```
Follow the prompts to encrypt or decrypt sensitive information.

### SendTag.py
Run the script for network administration tasks:
```bash
python SendTag.py
```
Features:
- Enter administrator password when prompted.
- Scan the local network for reachable and connectable IPs.
- Use the specified tags to trigger administrative actions or execute remote commands.

## Available Tags
- Shutdown
- Reboot
- QWRB
- ape
- atmp
- achd
- WRB
- mtmp
- mdmadmshow
- mdmhide
- mdmRemoteExe
- mdmRemoteUpdate
- mdmRemoteUpdateTest
- CopyRokiSetting
- Openfw
- Closefw
- MakeMacList
- addVeyon
- addVeyon2
- addVeyonN
- addVeyonN2

## Disclaimer
This project is intended for educational and testing purposes only. Use it responsibly and ensure compliance with local laws and regulations.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
