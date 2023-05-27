import os
import sys
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def generate_ecc_key(output_file):
    # Generate an ECC key pair
    key = ECC.generate(curve='P-256')

    # Write the private key to a file
    with open(key_file, 'w') as f:
        f.write(key.public_key().export_key(format='PEM').decode())

def encrypt_file(input_file, output_file, key_file):
    # Generate an ECC key pair
    key = ECC.generate(curve='P-256')

    # Write the public key to a file
    with open(key_file, 'wb') as f:
        f.write(key.public_key().export_key(format='PEM'))

    # Load the recipient's public key
    recipient_key = ECC.import_key(open(key_file).read())

    # Generate a random symmetric key
    key = os.urandom(32)

    # Create a cipher object using the symmetric key
    cipher = AES.new(key, AES.MODE_CBC)

    # Read the input file
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Pad the plaintext to a multiple of 16 bytes
    plaintext = pad(plaintext, 16)

    # Encrypt the padded plaintext using the symmetric key
    ciphertext = cipher.encrypt(plaintext)

    # Encrypt the symmetric key using ECC
    encrypted_key = recipient_key.encrypt(key)

    # Write the encrypted symmetric key and encrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(cipher.iv)
        f.write(encrypted_key)
        f.write(ciphertext)

def decrypt_file(input_file, output_file, key_file):
    # Load the private key
    key = ECC.import_key(open(key_file).read())

    # Read the input file
    with open(input_file, 'rb') as f:
        iv = f.read(16)
        encrypted_key = f.read()
        ciphertext = f.read()

    # Decrypt the symmetric key using ECC
    key = key.decrypt(encrypted_key)

    # Create a cipher object using the symmetric key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext using the symmetric key
    plaintext = cipher.decrypt(ciphertext)

    # Remove the padding from the plaintext
    plaintext = unpad(plaintext, 16)

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Parse command-line arguments
if len(sys.argv) < 5:
    print("Usage: python ecc.py [encrypt|decrypt] [input file] [output file] [key file]")
    sys.exit(1)

command = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]
key_file = sys.argv[4]

# Encrypt or decrypt the file
if command == 'encrypt':
    encrypt_file(input_file, output_file, key_file)
    print("File encrypted successfully.")
elif command == 'decrypt':
    decrypt_file(input_file, output_file, key_file)
    print("File decrypted successfully.")
else:
    print("Unknown command: " + command)
    sys.exit(1)
