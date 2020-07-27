import os
import pickle
import hashlib
import binascii
import multiprocessing
from ellipticcurve.privateKey import PrivateKey


def generate_private_key():
    return binascii.hexlify(os.urandom(32)).decode('utf-8').upper()

def private_key_to_public_key(private_key):
    pk = PrivateKey().fromString(bytes.fromhex(private_key))
    return '04' + pk.publicKey().toString().hex().upper()

def public_key_to_address(public_key):
    output = []
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    var = hashlib.new('ripemd160')
    encoding = binascii.unhexlify(public_key.encode())
    var.update(hashlib.sha256(encoding).digest())
    var_encoded = ('00' + var.hexdigest()).encode()
    digest = hashlib.sha256(binascii.unhexlify(var_encoded)).digest()
    var_hex = '00' + var.hexdigest() + hashlib.sha256(digest).hexdigest()[0:8]
    count = [char != '0' for char in var_hex].index(True) // 2
    n = int(var_hex, 16)
    while n > 0:
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    for i in range(count): output.append(alphabet[0])
    return ''.join(output[::-1])

def main():

    file = open('data')
    wallets = [i.strip() for i in file.readlines()]

    i = 0
    while True:
        private_key = generate_private_key()
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)

        print('{} {}'.format(i, address))
        i+=1

        if address in wallets:
            with open(address, 'w') as file:
                file.write('private: {}\npublic: {}'.format(private_key))

            print('winner winner chicken dinner')
            break

if __name__ == '__main__':
    main()