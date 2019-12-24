#Import packages
import pandas as pd
import numpy as np

#Extract electricity data for each LSOA
elec_d = pd.read_csv("../../data/raw/electricity/MSOA_domestic_electricity_2018.csv")
elec_nd = pd.read_csv("../../data/raw/electricity/MSOA_non-domestic_electricity_2018.csv")

elec_d.columns = ['lad13nm','lad13cd','msoa11nm','msoa11cd','elec_d_con','d_meters','elec_d_con_mean','elec_d_con_mdn']
elec_nd.columns = ['lad13nm','lad13cd','msoa11nm','msoa11cd','elec_nd_con','nd_meters','elec_nd_con_mean','elec_nd_con_mdn']

elec_d = elec_d[['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm','elec_d_con','d_meters','elec_d_con_mean','elec_d_con_mdn']]
elec_nd = elec_nd[['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm','elec_nd_con','nd_meters','elec_nd_con_mean','elec_nd_con_mdn']]

elec_d = elec_d.applymap(lambda x : x.strip() if type(x) != float and type(x) != int else x)
elec_nd = elec_nd.applymap(lambda x : x.strip() if type(x) != float and type(x) != int else x)

elec_d = elec_d.set_index(['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm'])
elec_nd = elec_nd.set_index(['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm'])

elec_d = elec_d.applymap(lambda x : eval(x.replace(",","")) if type(x)==str else x)
elec_nd = elec_nd.applymap(lambda x : eval(x.replace(",","")) if type(x)==str else x)

elec_con = pd.merge(elec_d,elec_nd,how='inner',left_index=True,right_index=True).dropna().reset_index()

elec_con.loc[:,'elec_d_con':'elec_nd_con_mdn'] = elec_con.loc[:,'elec_d_con':'elec_nd_con_mdn'].apply(lambda x : abs(x))

elec_con['residential_ratio'] = elec_con.elec_d_con/elec_con.elec_nd_con
elec_con['residential_meter_ratio'] = elec_con.d_meters/elec_con.nd_meters
elec_con['residential_mdn_ratio'] = elec_con.elec_d_con_mdn/elec_con.elec_nd_con_mdn
elec_con['residential_mean_ratio'] = elec_con.elec_d_con_mean/elec_con.elec_nd_con_mean

#Saving to csv file
elec_con.to_csv("../../data/interim/msoa/electricity_msoa.csv",index=False)