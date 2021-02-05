import requests
import datetime
import pandas as pd

market = 'BNBUSDT'
tick_interval = '1m'

for c in ['2018', '2019', '2020']:
    startTime = datetime.datetime.strptime(
        '1.1.' + c + ' 00:00:00', '%d.%m.%Y %H:%M:%S').timestamp() * 1000
    stopTime = datetime.datetime.strptime(
        '31.12.' + c + ' 23:59:59', '%d.%m.%Y %H:%M:%S').timestamp() * 1000
    time_series = []
    while True:
        print(datetime.datetime.fromtimestamp(startTime / 1e3))
        url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval=' + \
            tick_interval + '&startTime=' + str(int(startTime)) + '&limit=1000'
        data = requests.get(url).json()
        if startTime > stopTime:
            break
            time_series += data

        time_series += data
        startTime += 1000 * 60000
    df = pd.DataFrame(time_series, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                            'Quote asset volume', 'Number of trades', 'aker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df.to_csv('data/'+market+"_"+str(c)+'.csv', index=False)
