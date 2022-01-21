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

url = ("https://financialmodelingprep.com/api/v3/historical-price-full/SPY,ARKK?apikey=c0c2fbedb6fdca83b90657ea293ed4f1")

test_raw_df = get_jsonparsed_data(url)

df = pd.DataFrame(test_raw_df['historicalStockList'])

SPY = pd.DataFrame(df['historical'][0])
ARKK = pd.DataFrame(df['historical'][1])

SPY['date'] = pd.to_datetime(SPY['date'],format = '%Y-%m-%d')
ARKK['date'] = pd.to_datetime(ARKK['date'],format = '%Y-%m-%d')

SPY = SPY[(SPY['date']>'2019-12-01')& (SPY['date']<'2021-05-01')]
ARKK = ARKK[(ARKK['date']>'2019-12-01')& (ARKK['date']<'2021-05-01')]

date_range = SPY['date'].groupby(SPY['date'].dt.strftime('%Y-%m')).max() #find the max date in the month from the current dataset

#SPY
SPY_monthly_data= SPY[SPY['date'].isin(date_range)][['date','adjClose']].sort_values(by ='date').set_index('date')
SPY_monthly_data['pct_change'] = SPY_monthly_data['adjClose'].pct_change()
SPY_monthly_data['cumluative_return'] = np.exp(np.log1p(SPY_monthly_data['pct_change']).cumsum())

#ARKK
ARKK_monthly_data= ARKK[ARKK['date'].isin(date_range)][['date','adjClose']].sort_values(by ='date').set_index('date')
ARKK_monthly_data['pct_change'] = ARKK_monthly_data['adjClose'].pct_change()
ARKK_monthly_data['cumluative_return'] = np.exp(np.log1p(ARKK_monthly_data['pct_change']).cumsum())


print(SPY_monthly_data)
print(ARKK_monthly_data)

fund_amount = 100000
Allocation = [.5,.5]

price_file = pd.merge(SPY_monthly_data['adjClose'], ARKK_monthly_data['adjClose'], left_index=True, right_index=True)
price_file.columns = ['SPY','ARKK']

def allocation(SPY,ARKK):
    price_file['port_SPY'] = price_file['SPY']*SPY
    price_file['port_ARKK'] = price_file['ARKK'] * ARKK
    print(price_file)
