import os
import time
import hashlib
import binascii
from ellipticcurve.privateKey import PrivateKey
from models import Entry

from peewee import *
from itertools import chain, islice
# import multiprocessing


class Bounty():
    """ Holds a list of wanted wallets """
    def __init__(self):
        """ Open and read contents of data containing rows of P2PKH wallet ids """
        self.wallet_ids = [i.strip() for i in open('data').readlines()]

    def update(self, wallet):
        """ add a new P2PKH wallet """
        self.wallet_ids.append(wallet)

    def include(self, wallets):
        """ add list of P2PKH wallets """
        self.wallet_ids + wallets


class Crypt():
    """     Yields tuples of private keys and wallet ids continuously. Steps Overview:
    PrivateKey:         EDCC6224FEE390A57C76C13A9BECC9502A6F3B1BF6F72B6ED11B83A0F0E3E9FC
    PublicKey:          04F3DF70315E569BBF9FB427DA65E60CE2E3660EA83EC8A8523DA4DE6901F7988E9E460CD594F27C9F6007A277820F3C1D8BB8485E1FCA38F37BCF9DC1A2DFA2A0
    +sha256:            B4AE3A0D|CF1AAD584327FDB0974BBCBE3E19C2A6A2F9A29D7303C3A0D526910F
    +ripemd160:         C0CBEC6E4B3F537A68F64F65B68998158E211B92
    network byte:       00C0CBEC6E4B3F537A68F64F65B68998158E211B92
    +8bytes sha256:     00C0CBEC6E4B3F537A68F64F65B68998158E211B92|B4AE3A0D
    base58ccheck:       1JaR2gwbg2vFvgHvshaL61HmCitaCGaBgQ      """


    def generate_private_key(self):
        """ Generate random 32-byte hexidecimal integer
            TODO test: 256-bit / 64 char number in range 0-9 A-F """

        return binascii.hexlify(os.urandom(32)).decode('utf-8').upper()


    def private_key_to_public_key(self, private_key):
        """ Derive public key from private key by passing it through sha256 functionn (SECP256k1 ECDSA).
            Time-consuming step - TODO: look into multiprocessing this step """

        pk = PrivateKey().fromString(bytes.fromhex(private_key))
        return '04' + pk.publicKey().toString().hex().upper()


    def public_key_to_address(self, public_key):
        """ Accept a public key and convert it to its resepective P2PKH wallet address """

        var = hashlib.new('ripemd160')
        encoding = binascii.unhexlify(public_key.encode())
        var.update(hashlib.sha256(encoding).digest())
        var_encoded = ('00' + var.hexdigest()).encode()

        output = []
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

        digest = hashlib.sha256(binascii.unhexlify(var_encoded)).digest()
        var_hex = '00' + var.hexdigest() + hashlib.sha256(digest).hexdigest()[0:8]
        count = [char != '0' for char in var_hex].index(True) // 2
        n = int(var_hex, 16)
        while n > 0:
            n, remainder = divmod(n, 58)
            output.append(alphabet[remainder])
        for i in range(count): output.append(alphabet[0])

        return ''.join(output[::-1])


    def gen(self):
        """ Generate private keys and wallets"""

        while True:

            private_key = self.generate_private_key()
            public_key = self.private_key_to_public_key(private_key)
            wallet = self.public_key_to_address(public_key)

            yield (wallet, private_key)

    def chunks(self, size=100):
        iterator = iter(self.gen())
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))



def main():

    database = SqliteDatabase('database.db')
    database.connect()
    with database:
        database.create_tables([Entry])
    database.close()

    for data in Crypt().chunks():
        with database.atomic():
            Entry.insert_many(data, fields=[Entry.wallet, Entry.private_key]).execute()




if __name__ == '__main__':
    main()

    # import multiprocessing

    # for cpu in range(multiprocessing.cpu_count()):
    #     multiprocessing.Process(target = main).start()

