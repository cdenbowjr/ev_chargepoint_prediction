import pandas as pd
import os

total_travel = pd.concat([pd.read_csv('../../data/interim/msoa/trip_ends/'+x) for x in os.listdir('../../data/interim/msoa/trip_ends/') if 'csv' in x])
total_travel = total_travel.reset_index(drop=True)

total_travel.to_csv('../../data/interim/msoa/trip_ends_msoa.csv',index=False)