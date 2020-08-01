import pandas as pd
import numpy as np

# IMPORT & FORMAT COLUMNS & FILL NaN's
df = pd.read_csv('Motor-Matrix.csv',
                 encoding="latin1", thousands=',')
df = df.drop(['Time Ordered', 'Original Ship Date', 'Original Ship Time',
              'Current Ship Date', 'Current Ship Time', 'Actual Ship Time',
              'LIH Protection?', 'Actual Ship Date.1', 'Real Ship Date',
              'Returned from location', 'Engineering Report Required?',
              'Engineering Report Number', 'Damage Type 1', 'Damage Type 2',
              'Damage Type 3', 'Incident?', 'Failure?'], axis=1)
df.columns = df.columns.str.strip().str.lower().str.replace(' ',
             '_').str.replace('(', '').str.replace(')', '')
# df.replace(r'\s+', np.nan, regex=True).replace('', np.nan)


# CONVERT TO DATETIME
df['date_ordered'] = pd.to_datetime(df['date_ordered'], errors='coerce')
df['actual_ship_date'] = pd.to_datetime(df['actual_ship_date'],
                                        errors='coerce')
df['returned_date'] = pd.to_datetime(df['returned_date'], errors='coerce')
df['date_in_hole'] = pd.to_datetime(df['date_in_hole'], errors='coerce')
df['date_out_of_hole'] = pd.to_datetime(df['date_out_of_hole'],
                                        errors='coerce')

indexer = df['returned_date'] - pd.to_datetime('2018-1-1')


# WRITE TO FILE
df_dt = df.dtypes
df_dt.to_csv('df_dt.csv')
print(df_dt)
df.to_csv('df.csv')
print(indexer)


# TO CONVERT FRACTIONS
def convert(s):
    try:
        return float(s)
    except ValueError:
        num, denom = s.split('/')
        return float(num) / float(denom)
