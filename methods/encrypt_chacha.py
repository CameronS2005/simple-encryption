#!/usr/bin/python
import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def encrypt(input_file, output_file, key_file):
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    key = os.urandom(32)
    cipher = ChaCha20Poly1305(key)

    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    
    with open(output_file, 'wb') as f:
        f.write(ciphertext)

    # write the key to the key file
    with open(key_file, 'wb') as f:
        f.write(key)
    
    # print the key and the contents of the key file
    print('key:', key)
    with open(key_file, 'rb') as f:
        print('key file:', f.read())


def decrypt_file(input_file, output_file, key_file):
    # Read the key from the key file
    with open(key_file, 'rb') as f:
        key = f.read()

    # Create a cipher object using the key
    cipher = ChaCha20Poly1305(key)

    # Read the encrypted data from the input file
    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    # Decrypt the data
    plaintext = cipher.decrypt(nonce=None, ciphertext=ciphertext, associated_data=None)

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(plaintext)



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python file.py [encrypt/decrypt] [input_file] [output_file] [key_file]')
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key_file = sys.argv[4]

    if mode == 'encrypt':
        encrypt(input_file, output_file, key_file)
    elif mode == 'decrypt':
        decrypt(input_file, output_file, key_file)
    else:
        print('Invalid mode. Choose either "encrypt" or "decrypt"')
        sys.exit(1)
