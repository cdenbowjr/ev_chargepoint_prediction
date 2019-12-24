#Import packages
import pandas as pd
import numpy as np

import json
from pandas.io.json import json_normalize

#Open json file with all the MSOA and LSOA coordinates 
msoa_f = open('../../data/raw/geo_spatial/Middle_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BFC_simple.geojson', 'r')
lsoa_f = open('../../data/raw/geo_spatial/lsoa_uk.geojson', 'r')

try:
    msoa_data = json.load(msoa_f)
    lsoa_data = json.load(lsoa_f)

finally:
    msoa_f.close()
    lsoa_f.close()

#Extract coordinates for each MSOA
msoa_json = json_normalize(data=msoa_data['features'])
msoa_json.columns = [x.split(".")[1] if len(x.split("."))==2 else x for x in msoa_json.columns]

#Extract coordinates for each LSOA
lsoa_json = json_normalize(data=lsoa_data['features'])
lsoa_json.columns = [x.split(".")[1] if len(x.split("."))==2 else x for x in lsoa_json.columns]


#Limit the headers to the following below
msoa_json = msoa_json[['msoa11cd','msoa11nm','st_areashape','st_lengthshape']]
lsoa_json = lsoa_json[['lsoa11cd','lsoa11nm','st_areasha','st_lengths']]

#Save file to csv
msoa_json.to_csv("../../data/interim/msoa/area_perimeter_msoa.csv",index=False)
lsoa_json.to_csv("../../data/interim/lsoa/area_perimeter_lsoa.csv",index=False)

print(msoa_json.head())
print(lsoa_json.head())
