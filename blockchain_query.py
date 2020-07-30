import urllib.request
from models import Entry

from peewee import *

urllib.request
s = ''
s += wallet + '|'
url = 'https://blockchain.info/balance?active=' + s
wallet_balances = urllib.request.urlopen(url)
with open('blockchainresponse', 'w') as file:
    file.write(wallet_balances)
https://blockchain.info/balance?active=3Fr1mGhnPAQ9YDf1dzg4B47PkX5TuvFtYv|33QoG5ioV4hseifKT9iaqrmD2eis7DicWA|1CPaziTqeEixPoSFtJxu74uDGbpEAotZom