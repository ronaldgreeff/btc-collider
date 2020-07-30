import urllib.request
from models import Entry

from peewee import *

class QueryManager():
    def __init__(self):
        self.base_url = 'https://blockchain.info/balance?active='
        self.max_addresses = 59

    def get_wallets_for_query(self):
        s = ''
        q = Entry.select(Entry.wallet) # limit to n = self.max_addresses
        return q

q = (Entry.select(Entry.wallet))

# s = ''
# s += wallet + '|'
# url = 'https://blockchain.info/balance?active=' + s
# wallet_balances = urllib.request.urlopen(url)
# with open('blockchainresponse', 'w') as file:
#     file.write(wallet_balances)

# https://blockchain.info/balance?active=3Fr1mGhnPAQ9YDf1dzg4B47PkX5TuvFtYv|33QoG5ioV4hseifKT9iaqrmD2eis7DicWA|1CPaziTqeEixPoSFtJxu74uDGbpEAotZom