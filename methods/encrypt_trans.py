#!/usr/bin/python
import sys
import random

def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read().decode('latin1', errors='ignore')

def write_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data.encode('latin1'))

def generate_key(key_length):
    key = list(range(key_length))
    random.shuffle(key)
    return key

def encrypt(input_file, output_file, key_file):
    data = read_file(input_file)
    key = generate_key(len(data))
    key_str = ' '.join(str(k) for k in key)
    write_file(key_file, key_str)
    encrypted_data = ''.join(data[i] for i in key)
    write_file(output_file, encrypted_data)

def decrypt(input_file, output_file, key_file):
    data = read_file(input_file)
    key_str = read_file(key_file)
    key = [int(k) for k in key_str.split()]
    decrypted_data = [''] * len(data)
    for i, k in enumerate(key):
        if k >= len(decrypted_data):
            continue
        decrypted_data[k] = data[i] if i < len(data) else ''
    decrypted_data = ''.join(decrypted_data)
    write_file(output_file, decrypted_data)

def print_usage():
    print('Usage: python substitution_cipher.py <encrypt/decrypt> <input_file> <output_file> <key_file>')

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print_usage()
        sys.exit(1)
    method = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key_file = sys.argv[4]

    if method == 'encrypt':
        encrypt(input_file, output_file, key_file)
    elif method == 'decrypt':
        decrypt(input_file, output_file, key_file)
    else:
        print('Invalid method specified. Use "encrypt" or "decrypt".')
        print_usage()
        sys.exit(1)
