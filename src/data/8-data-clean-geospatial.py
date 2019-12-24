from pandas.io.json import json_normalize
import numpy as np
import pandas as pd
import json
import requests

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

extract_list = ['parks','parking','train_station','gas_station','hotels','supermarkets']

for y in extract_list:
    
    for x in range(0,33):
        if x == 0:
            df = pd.read_json(f"../../data/raw/json/{y}_{x}.json")[['response']].sort_index()

        else:
            df = pd.concat([df,pd.read_json(f"../../data/raw/json/{y}_{x}.json")[['response']].sort_index()])
            
    vars()[y] = df.reset_index(drop=True)
    

geo_spatial = pd.concat([parks,parking,train_station,gas_station,hotels,supermarkets],axis=1)
geo_spatial.columns = extract_list 

geo_spatial = geo_spatial.applymap(lambda x : {'venues':[]} if (x == {} or x == []) else x)


num_parks = pd.Series([len(col['parks']['venues']) for row,col in geo_spatial.iterrows()],name='num_parks')
num_parking = pd.Series([len(col['parking']['venues']) for row,col in geo_spatial.iterrows()],name='num_parking')
num_train_st = pd.Series([len(col['train_station']['venues']) for row,col in geo_spatial.iterrows()],name='num_train_st')
num_gas_st = pd.Series([len(col['gas_station']['venues']) for row,col in geo_spatial.iterrows()],name='num_gas_st')
num_hotels = pd.Series([len(col['hotels']['venues']) for row,col in geo_spatial.iterrows()],name='num_hotels')
num_supermarkets = pd.Series([len(col['supermarkets']['venues']) for row,col in geo_spatial.iterrows()],name='num_supermarkets')

park_distance = pd.Series([np.mean([x['location']['distance'] for x in col['parks']['venues']]) for row,col in geo_spatial.iterrows()],name='park_distance')
parking_distance = pd.Series([np.mean([x['location']['distance'] for x in col['parking']['venues']]) for row,col in geo_spatial.iterrows()],name='parking_distance')
train_st_distance = pd.Series([np.mean([x['location']['distance'] for x in col['train_station']['venues']]) for row,col in geo_spatial.iterrows()],name='train_st_distance')
gas_st_distance = pd.Series([np.mean([x['location']['distance'] for x in col['gas_station']['venues']]) for row,col in geo_spatial.iterrows()],name='gas_st_distance')
hotel_distance = pd.Series([np.mean([x['location']['distance'] for x in col['hotels']['venues']]) for row,col in geo_spatial.iterrows()],name='hotel_distance')
supermarkets_distance = pd.Series([np.mean([x['location']['distance'] for x in col['supermarkets']['venues']]) for row,col in geo_spatial.iterrows()],name='supermarkets_distance')


#Open json file with all the coordinates 
f = open('../../data/raw/geo_spatial/lsoa_uk.geojson', 'r')

try:
    data = json.load(f)

finally:
    f.close()
    
#Extract coordinates for each LSOA
lsoa_json = json_normalize(data=data['features']).iloc[:,:-1]
lsoa_json.columns = [x.split(".")[1] if len(x.split("."))==2 else x for x in lsoa_json.columns]

#Limit the headers to the following below
lsoa_json = lsoa_json[['lsoa11cd','lsoa11nm']]

geospatial_lsoa = pd.concat([lsoa_json[['lsoa11cd','lsoa11nm']],num_parks,park_distance,num_parking,parking_distance,num_train_st,train_st_distance,num_gas_st,gas_st_distance,num_hotels,hotel_distance,num_supermarkets,supermarkets_distance],axis=1).fillna(0)
geospatial_lsoa.to_csv('../../data/interim/lsoa/geo_spatial_lsoa.csv',index=False)


#Extract MSOA data for each LSOA
lsoa2msoa = pd.read_csv("../../data/interim/lsoa_msoa.csv")
lsoa2msoa = lsoa2msoa[['lsoa11cd','lsoa11nm','msoa11nm','msoa11cd']].drop_duplicates(keep='first')

geospatial_msoa = pd.merge(lsoa2msoa,geospatial_lsoa,left_on=['lsoa11cd','lsoa11nm'],right_on=['lsoa11cd','lsoa11nm'])

geo1 = geospatial_msoa.groupby(['msoa11nm','msoa11cd']).agg(sum).iloc[:,[0,2,4,6,8,10]]
geo2 = geospatial_msoa.groupby(['msoa11nm','msoa11cd']).agg('mean').iloc[:,1::2]

geospatial_msoa = pd.concat([geo1,geo2],axis=1).reset_index()

geospatial_msoa.to_csv('../../data/interim/msoa/geo_spatial_msoa.csv',index=False)