import pandas as pd
import numpy as np

# IMPORT MOTOR MATRIX & FORMAT COLUMNS & FILL NaN's
mm = pd.read_csv('motor-matrix.csv',
                 encoding="latin1", thousands=',')
mm = mm.drop(['Time Ordered', 'Original Ship Date', 'Original Ship Time',
              'Current Ship Date', 'Current Ship Time', 'Actual Ship Time',
              'LIH Protection?', 'Actual Ship Date.1', 'Real Ship Date',
              'Returned from location', 'Engineering Report Required?',
              'Engineering Report Number', 'Damage Type 1', 'Damage Type 2',
              'Damage Type 3', 'Incident?', 'Failure?'], axis=1)
mm.columns = mm.columns.str.strip().str.lower().str.replace(' ',
             '_').str.replace('(', '').str.replace(')', '')


# CONVERT TO DATETIME IN MOTOR MATRIX
mm['date_ordered'] = pd.to_datetime(mm['date_ordered'], errors='coerce')
mm['actual_ship_date'] = pd.to_datetime(mm['actual_ship_date'],
                                        errors='coerce')
mm['returned_date'] = pd.to_datetime(mm['returned_date'], errors='coerce')
mm['date_in_hole'] = pd.to_datetime(mm['date_in_hole'], errors='coerce')
mm['date_out_of_hole'] = pd.to_datetime(mm['date_out_of_hole'],
                                        errors='coerce')

# IMPORT HOU STATORS & FORMAT COLUMNS & FILL NaN's
dtypes = {
    'CID': 'object',
    'DTN': 'object',
    'Status': 'object',
    'PR or RSA #': 'object',
    'Tech Initials': 'object',
    'Rubber Status': 'object',
    'Config': 'object',
    'Stator Fit': 'object',
    'Rubber Type': 'object',
    'Overall Length': 'float64',
    'Top Conn Insp Results': 'object',
    'Bottom Conn Insp Results': 'object',
    'Minor ID 1': 'float64',
    'Minor ID 2': 'float64',
    'Minor ID 3': 'float64',
    'Minor ID 4': 'float64',
    'Minor ID 5': 'float64',
    'Minor ID 6': 'float64',
    'Minor Avg': 'float64',
    'Rubber Temp During Mesaurement': 'float64',
    'Minor Avg at 75F': 'float64',
    'Rubber Evaluation': 'object',
    'Secondary Damage': 'object',
    'Bond': 'object',
    'Current Hardness': 'float64',
    'Run Hours': 'float64',
    'RSS Run?': 'object',
    'Run Mud Type': 'object',
    'Mud Temp': 'float64',
    'Connection Results': 'object',
    'Reline Results': 'object',
    'Data Status': 'object',
    }
hsl = pd.read_csv('hou-stator-log.csv', dtype=dtypes, parse_dates=[4],
                  encoding="latin1", thousands=',',
                  infer_datetime_format='true')
hsl = hsl.drop(['Tech Initials', 'Stator Fit', 'Overall Length',
                'Data Status'], axis=1)
hsl.columns = hsl.columns.str.strip().str.lower().str.replace(' ',
              '_').str.replace('(', '').str.replace(')', '')


# CONVERT TO DATETIME IN HOU STATOR LOG
'''MAY NOT NEED
hsl['date_ordered'] = pd.to_datetime(hsl['date'], errors='coerce')'''


# IMPORT WTX STATORS & FORMAT COLUMNS & FILL NaN's
msl = pd.read_csv('stator-tracker-mld.csv',
                  encoding="latin1", thousands=',')
msl = msl.drop(['Tech', 'Last Reline Cert Date', 'Stator Fit',
                'Overall Length', 'Data Status'], axis=1)
msl.columns = msl.columns.str.strip().str.lower().str.replace(' ',
              '_').str.replace('(', '').str.replace(')', '')


# CONVERT TO DATETIME IN WTX STATOR LOG
'''MAY NOT NEED
msl['date_ordered'] = pd.to_datetime(msl['date'], errors='coerce')'''


# IMPORT PS INFO & FORMAT COLUMNS
psi = pd.read_csv('ps-info.csv',
                  encoding="latin1", thousands=',')
psi.columns = psi.columns.str.strip().str.lower().str.replace(' ',
              '_').str.replace('(', '').str.replace(')', '')


indexer = mm['returned_date'] - pd.to_datetime('2018-1-1')


# WRITE TO FILE
mm_dt = mm.dtypes
mm_dt.to_csv('mm_dt.csv')
mm.to_csv('mm.csv')
hsl_dt = hsl.dtypes
hsl_dt.to_csv('hsl_dt.csv')
hsl.to_csv('hsl.csv')
msl_dt = msl.dtypes
msl_dt.to_csv('msl_dt.csv')
msl.to_csv('msl.csv')
psi_dt = psi.dtypes
psi_dt.to_csv('psi_dt.csv')
psi.to_csv('psi.csv')


# TO CONVERT FRACTIONS
def convert(s):
    try:
        return float(s)
    except ValueError:
        num, denom = s.split('/')
        return float(num) / float(denom)
