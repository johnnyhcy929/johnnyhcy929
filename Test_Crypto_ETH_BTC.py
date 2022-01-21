try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
#API key :c0c2fbedb6fdca83b90657ea293ed4f1
import pandas as pd
import json
import ssl
from datetime import datetime
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context
def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

Currency = ['ETHUSD','BTCUSD']
data = []

for Currency in Currency:
    url = ("https://financialmodelingprep.com/api/v3/historical-chart/1hour/"+Currency+"?apikey=c0c2fbedb6fdca83b90657ea293ed4f1")
    data.append(get_jsonparsed_data(url))
    print(data)

Currency = ['ETHUSD','BTCUSD']
price_data_dict = dict(zip(Currency,data))

ETHUSD = pd.DataFrame(price_data_dict['ETHUSD'])
ETHUSD['date'] = pd.to_datetime(ETHUSD['date'],format = '%Y-%m-%d %H:%M:%S')
ETHUSD=ETHUSD.sort_values(by=['date']).set_index('date')

BTCUSD = pd.DataFrame(price_data_dict['BTCUSD'])
BTCUSD['date'] = pd.to_datetime(BTCUSD['date'],format = '%Y-%m-%d %H:%M:%S')
BTCUSD=BTCUSD.sort_values(by=['date']).set_index('date')


print(ETHUSD)
print(BTCUSD)

df_test = pd.merge(BTCUSD['close'],ETHUSD['close'], left_index=True, right_index=True)
df_test.columns = ['BTCUSD_close','ETHUSD_close']

print(df_test)
print(df_test.describe())