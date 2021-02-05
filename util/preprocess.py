import os
import pandas as pd
import datetime
print(os.listdir('data'))


years = ['2018', '2019', '2020']
for c in years:
    print(c)
    df = pd.read_csv('data/'+'BNBUSDT_'+c+'.csv')
    df = df[['Open time', 'Open']]
    df = df.rename(columns={'Open time': 'Time', 'Open': 'Price'})

    for i, e in enumerate(['Year', 'Month', 'Day', 'Hour', 'Minute']):
        df[e] = df['Time'].apply(
            lambda x: datetime.datetime.fromtimestamp(x/1000.0).timetuple()[:5][i])
 
    df = df.drop(columns=['Time'])
    df = df[df['Year'] == int(c)]
    print(len(df))
    df.to_csv('processed_data/BNBUSTD_'+c+'_Processed.csv')
