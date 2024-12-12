import pandas as pd
import numpy as np


# Function to convert fractions to floats
def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


# IMPORT MOTOR MATRIX & FORMAT COLUMNS & FILL NaN's
mm = pd.read_csv('full-ir-log-from-jan-2019.csv',
                 encoding="latin1", thousands=',')
mm = mm.drop(['Order Type', 'Time Ordered', 'Planned Job Number',
              'Inspection Level', 'Monitor', 'Original Ship Date',
              'Original Ship Time', 'Current Ship Date', 'Current Ship Time',
              'Actual Ship Time', 'Tool Type', 'Float Bore', 'LIH Protection?',
              'Delivery Ticket Start #', 'Actual Ship Date',
              'Delivery Ticket End #', 'Returned from location',
              'Engineering Report Required?', 'Engineering Report Number',
              'Damage Type 1', 'Damage Type 2', 'Damage Type 3', 'Incident?',
              'Failure?'], axis=1)
mm.columns = mm.columns.str.strip().str.lower().str.replace(' ', '_') + '_mm'
mm.to_csv('mm.csv')

# CONVERT TO DATETIME IN MOTOR MATRIX
mm['date_ordered_mm'] = pd.to_datetime(mm['date_ordered_mm'], errors='coerce')
mm['actual_ship_date.1_mm'] = pd.to_datetime(mm['actual_ship_date.1_mm'],
                                          errors='coerce')
mm['returned_date_mm'] = pd.to_datetime(mm['returned_date_mm'], errors='coerce')
mm['date_in_hole_mm'] = pd.to_datetime(mm['date_in_hole_mm'], errors='coerce')
mm['date_out_of_hole_mm'] = pd.to_datetime(mm['date_out_of_hole_mm'],
                                        errors='coerce')
mm['tool_size_mm'] = mm['tool_size_mm'].fillna(0).astype('int64')

# mm['ps_stage'] = mm['ps_stage'].map('{0:.2f}'.format)

# IMPORT COMBINED STATOR LOG & FORMAT COLUMNS
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
    'Overall Length': 'object',
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
    'Mud Temp': 'object',
    'Connection Results': 'object',
    'Reline Results': 'object',
    'Data Status': 'object',
    }
csl = pd.read_csv('stator-log-compiler.csv', dtype=dtypes, parse_dates=[4],
                  encoding="latin1", thousands=',',
                  infer_datetime_format='true')
csl = csl.drop(['Tech Initials', 'Stator Fit', 'Overall Length', 'Minor Avg',
                'Rubber Temp During Mesaurement', 'Data Status'], axis=1)
csl.columns = csl.columns.str.strip().str.lower().str.replace(' ', '_') + '_csl'

csl['date_csl'] = pd.to_datetime(csl['date_csl'], errors='coerce')


# IMPORT COMBINED ROTOR LOG & FORMAT COLUMNS

dtypes = {
    'CID': 'object',
    'DTN': 'object',
    'Status': 'object',
    'PR or RSA #': 'object',
    'Tech': 'object',
    'Coating Status': 'object',
    'Config': 'object',
    'Coating Type': 'object',
    'Overall Length': 'float64',
    'Top Conn Insp Results': 'object',
    'Bottom Conn Insp Results': 'object',
    'Mean Dia 1': 'float64',
    'Mean Dia 2': 'float64',
    'Mean Dia 3': 'float64',
    'Mean Dia 4': 'float64',
    'Mean Dia 5': 'float64',
    'Rotor Avg': 'float64',
    'Major OD Avg': 'float64',
    'Coating Evaluation': 'object',
    'Result': 'object',
    'Data Status': 'object',
    }

crl = pd.read_csv('rotor-log-compiler.csv', dtype=dtypes, parse_dates=[4],
                  encoding="latin1", thousands=',',
                  infer_datetime_format='true')
crl = crl.drop(['Tech', 'Data Status'], axis=1)
crl.columns = crl.columns.str.strip().str.lower().str.replace(' ', '_') + '_crl'

crl['date_crl'] = pd.to_datetime(crl['date_crl'], errors='coerce')


# IMPORT PS INFO & FORMAT COLUMNS
psi = pd.read_csv('ps-info.csv',
                  encoding="latin1", thousands=',')
psi = psi.drop(['Mfr', 'Size', 'Tube OD', 'Lobe', 'Stage',
               'Raw Rate of Change', 'Min', 'Go_Min', 'Go_Max', 'Max'],
               axis=1)
psi.columns = psi.columns.str.strip().str.lower().str.replace(' ', '_') + '_psi'
psi = psi.sort_values(by='config_psi')
psi.insert(0, 'config', psi['config_psi'])


# MAKE MM INDEXER
mm_idx = pd.DataFrame()
mm_idx['lobe'] = mm['ps_lobes_mm'].astype('str')
mm_idx['stage'] = mm['ps_stage_mm'].astype('str')
spl = mm_idx['stage'].str.split('.', expand=True)
mm_idx['stage'] = spl[0] + spl[1]
mm_idx['dtn'] = mm['cid/dtn_mm'].str.split('-', expand=True)[1]
mm_idx['returned_date'] = mm['returned_date_mm'] - pd.Timestamp("2018-01-01")
mm_idx['returned_date'] = mm_idx['returned_date'].dt.days.astype('str')
mm_idx['idx'] = (mm_idx['lobe'] + mm_idx['stage'] + mm_idx['dtn']
                 + mm_idx['returned_date'])
mm_idx['idx'] = pd.to_numeric(mm_idx['idx'], errors='coerce')
mm_idx['idx'] = mm_idx['idx'].replace(np.nan, 0, regex=True)
mm['idx'] = mm_idx['idx']
mm = mm.sort_values(by='idx')


csl_idx = pd.DataFrame()
csl_idx['lobestage'] = csl['config_csl'].astype('str')
csl_idx['lobestage'] = csl_idx['lobestage'].str.split('_', expand=True)[0]
csl_idx['lobestage'] = csl_idx['lobestage'].str.replace('.', '')
csl_idx['lobestage'] = csl_idx['lobestage'].str[5:]
csl_idx['dtn'] = csl['dtn_csl'].str.split('-', expand=True)[1]
print(csl['date_csl'])
csl_idx['measured_date'] = csl['date_csl'] - pd.Timestamp("2018-01-01")

csl_idx['measured_date'] = csl_idx['measured_date'].dt.days.astype('str')

csl_idx['idx'] = (csl_idx['lobestage'] + csl_idx['dtn']
                  + csl_idx['measured_date'])
csl_idx['idx'] = pd.to_numeric(csl_idx['idx'], errors='coerce')
csl_idx['idx'] = csl_idx['idx'].replace(np.nan, 0, regex=True)
csl['idx'] = csl_idx['idx']
csl.insert(0, 'idx_csl', csl['idx'])
csl = csl.sort_values(by='idx')

crl_idx = pd.DataFrame()
crl_idx['lobestage'] = crl['config_crl'].astype('str')
crl_idx['lobestage'] = crl_idx['lobestage'].str.split('_', expand=True)[0]
crl_idx['lobestage'] = crl_idx['lobestage'].str.replace('.', '')
crl_idx['lobestage'] = crl_idx['lobestage'].str[5:]
crl_idx['dtn'] = crl['dtn_crl'].str.split('-', expand=True)[1]
crl_idx['measured_date'] = crl['date_crl'] - pd.Timestamp("2018-01-01")
crl_idx['measured_date'] = crl_idx['measured_date'].dt.days.astype('str')
crl_idx['idx'] = (crl_idx['lobestage'] + crl_idx['dtn']
                  + crl_idx['measured_date'])
crl_idx['idx'] = pd.to_numeric(crl_idx['idx'], errors='coerce')
crl_idx['idx'] = crl_idx['idx'].replace(np.nan, 0, regex=True)
crl['idx'] = crl_idx['idx']
crl.insert(0, 'idx_crl', crl['idx'])
crl = crl.sort_values(by='idx')

# MERGE ALL DATAL
merge = pd.merge_asof(mm, csl, on='idx', direction='forward')
merge = pd.merge_asof(merge, crl, on='idx', direction='forward')
merge['config'] = merge['config_csl']
merge['config'] = merge['config'].replace(r'\s+', np.nan, regex=True)
merge['config'] = merge['config'].fillna("not_found")
merge = merge.sort_values(by='config')
merge = pd.merge(merge, psi, on='config', how='left')

# PERFORM CALS
merge['delta_csl'] = merge['idx_csl'] - merge['idx']
merge['delta_crl'] = merge['idx_crl'] - merge['idx']
merge['dh_temp_swell'] = (merge['mud_temp_mm'] - 75) * merge['rate_of_change_psi']
merge['dh_total_swell'] = (np.where(merge['mud_type_mm'] == 'OBM',
                           merge['dh_temp_swell'] + 0.003,
                           merge['dh_temp_swell']))
merge['og_stator_minor'] = merge['rotor_od_psi'] - merge['outgoing_fit_mm']
merge['ic_fit'] = merge['rotor_od_psi'] - merge['minor_avg_at_75f_csl']
merge['og_compression'] = ((merge['outgoing_fit_mm'] + merge['dh_total_swell'])
                        / (merge['tube_id_psi'] - (merge['minor_avg_at_75f_csl']
                           - merge['dh_total_swell'])))
merge['ic_compression'] = ((merge['ic_fit'] + merge['dh_total_swell'])
                           / (merge['tube_id_psi'] - (merge['minor_avg_at_75f_csl']
                           - merge['dh_total_swell'])))
merge['calc_fit_change'] = merge['ic_fit'] - merge['outgoing_fit_mm']
merge['calc_fit_change_per_50hr'] = (merge['calc_fit_change']
                                     / merge['total_c&d_hours_mm']) * 50
merge['base_model'] =  merge['ps_lobes_mm'].astype('str') + " " + merge['ps_stage_mm'].astype('str') + " " + merge['ps_elastomer_mm']
merge['base_model_w_coating'] =  merge['ps_lobes_mm'].astype('str') + " " + merge['ps_stage_mm'].astype('str') + " " + merge['ps_elastomer_mm'] + " " + merge['coating_type_crl']
merge['calc_fit_change'] = merge['calc_fit_change'].round(3)

# merge['stator_related_incident'] =

# WRITE TO FILE
mm_dt = mm.dtypes
mm_dt.to_csv('mm_dt.csv')
mm.to_csv('mm.csv')
csl_dt = csl.dtypes
csl_dt.to_csv('csl_dt.csv')
csl.to_csv('csl.csv')
crl_dt = crl.dtypes
crl_dt.to_csv('crl_dt.csv')
crl.to_csv('crl.csv')
mm_idx_dt = mm_idx.dtypes
mm_idx_dt.to_csv('mm_idx_dt.csv')
mm_idx.to_csv('mm_idx.csv')
csl_idx_dt = csl_idx.dtypes
csl_idx_dt.to_csv('csl_idx_dt.csv')
csl_idx.to_csv('csl_idx.csv')
crl_idx_dt = crl_idx.dtypes
crl_idx_dt.to_csv('crl_idx_dt.csv')
crl_idx.to_csv('crl_idx.csv')
merge_dt = merge.dtypes
merge_dt.to_csv('merge_dt.csv')
merge.to_csv('merge.csv')
psi_dt = psi.dtypes
psi_dt.to_csv('psi_dt.csv')
psi.to_csv('psi.csv')
