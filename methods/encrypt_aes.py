#!/usr/bin/python
import sys
import os
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes

def encrypt_file(input_file, output_file, key_file):
    # Generate a random 256-bit key
    key = get_random_bytes(32)

    # Save the key to a file
    with open(key_file, 'wb') as kf:
        kf.write(key)

    # Generate a random 96-bit nonce
    nonce = get_random_bytes(12)

    # Create the cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    # Encrypt the input file and write the output to the output file
    with open(input_file, 'rb') as ifile, open(output_file, 'wb') as ofile:
        # Write the nonce to the output file so it can be used for decryption
        ofile.write(nonce)

        # Encrypt the file in chunks to conserve memory
        chunk_size = 4096
        while True:
            chunk = ifile.read(chunk_size)
            if len(chunk) == 0:
                break
            encrypted_chunk = cipher.encrypt(chunk)
            ofile.write(encrypted_chunk)

        # Finalize the encryption and generate the authentication tag
        tag = cipher.digest()

        # Write the authentication tag to the output file
        ofile.write(tag)

    print(f'Encrypted {input_file} to {output_file} using key in {key_file}.')



def decrypt_file(input_file, output_file, key_file):
    # Read the key from the key file
    with open(key_file, 'rb') as kf:
        key = kf.read()

    # Read the nonce from the input file
    with open(input_file, 'rb') as ifile:
        nonce = ifile.read(12)

        # Create the cipher object
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        # Decrypt the file and write the output to the output file
        with open(output_file, 'wb') as ofile:
            chunk_size = 4096
            while True:
                chunk = ifile.read(chunk_size)
                if len(chunk) == 0:
                    break
                ofile.write(cipher.decrypt(chunk))

            # Verify the authentication tag
            tag = ifile.read()
            try:
                cipher.verify(tag)
            except ValueError:
                raise ValueError('Authentication tag failed - file may have been tampered with')

    print(f'Decrypted {input_file} to {output_file} using key in {key_file}.')


# Check the command line arguments
if len(sys.argv) != 5:
    print('Usage: python encrypt_decrypt.py <encrypt/decrypt> <input file> <output file> <key file>')
    sys.exit(1)

# Dispatch to the appropriate function based on the first argument
if sys.argv[1] == 'encrypt':
    encrypt_file(sys.argv[2], sys.argv[3], sys.argv[4])
elif sys.argv[1] == 'decrypt':
    decrypt_file(sys.argv[2], sys.argv[3], sys.argv[4])
else:
    print('Invalid command. Use "encrypt" or "decrypt".')
    sys.exit(1)
