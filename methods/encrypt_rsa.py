import os
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_rsa_key(output_file):
    # Generate an RSA key pair with 4096 bits
    key = RSA.generate(4096)

    # Write the private key to a file
    with open(output_file, 'wb') as f:
        f.write(key.export_key())

def encrypt_file(input_file, output_file, key_file):
    # Generate an RSA key pair with 4096 bits
    key = RSA.generate(4096)

    # Write the public key to a file
    with open(key_file, 'wb') as f:
        f.write(key.publickey().export_key())

    # Load the public key
    recipient_key = RSA.import_key(open(key_file).read())

    # Generate a session key
    session_key = os.urandom(32)

    # Create a cipher object using the session key
    cipher = PKCS1_OAEP.new(recipient_key)
    ciphertext = cipher.encrypt(session_key)

    # Read the input file
    with open(input_file, 'rb') as f:
        data = f.read()

    # Encrypt the data using the session key
    cipher = PKCS1_OAEP.new(RSA.import_key(key.export_key()))
    encrypted_data = cipher.encrypt(data)

    # Write the encrypted session key and encrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(ciphertext + encrypted_data)

def decrypt_file(input_file, output_file, key_file):
    # Load the private key
    key = RSA.import_key(open(key_file).read())

    # Read the input file
    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    # Split the ciphertext into the encrypted session key and encrypted data
    ciphertext_len = key.size_in_bytes()
    encrypted_session_key = ciphertext[:ciphertext_len]
    encrypted_data = ciphertext[ciphertext_len:]

    # Decrypt the session key
    cipher = PKCS1_OAEP.new(key)
    session_key = cipher.decrypt(encrypted_session_key)

    # Decrypt the data using the session key
    cipher = PKCS1_OAEP.new(RSA.import_key(key.export_key()))
    data = cipher.decrypt(encrypted_data)

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(data)

# Parse command-line arguments
if len(sys.argv) < 5:
    print("Usage: python rsa.py [encrypt|decrypt] [input file] [output file] [key file]")
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
