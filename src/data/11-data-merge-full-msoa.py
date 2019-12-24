#Import packages
import pandas as pd
import numpy as np

#Loading data files containing socio-economic features
imd = pd.read_csv("../../data/interim/msoa/imd_msoa.csv")

imd = imd[['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm', 'income_score',
       'employment_score', 'education_score', 'health_score', 'crime_score',
       'housebar_score', 'livenv_score', 'idaci_score', 'idaopi_score',
       'chanyp_score', 'adultskills_score', 'geo_bar_score', 'widerbar_score',
       'indoor_score', 'outdoor_score', 'total_pop', 'under16_pop', '16_59_pop',
       'over60_pop', 'workingage_pop']]

income = pd.read_csv("../../data/interim/msoa/income_msoa.csv")


#Loading data files containing transportation features
travel = pd.read_csv("../../data/interim/msoa/travel_ulev.csv")
travel.msoa11nm = travel.msoa11nm.apply(lambda x: x.replace("`","'"))

#Loading data files containing geo-spatial features
area_perimeter = pd.read_csv("../../data/interim/msoa/area_perimeter_msoa.csv")
geo = pd.read_csv("../../data/interim/msoa/geo_spatial_msoa.csv")


#Loading electricity consumption files
electricity = pd.read_csv("../../data/interim/msoa/electricity_msoa.csv")

#Loading data files containing target variable
chargers = pd.read_csv("../../data/interim/msoa/chargepoints_msoa.csv")
chargers = chargers[['msoa11cd','msoa11nm','charge_points']]

#Merging imd with income
imd =imd.set_index(['msoa11cd'])
income = income.set_index(['msoa11cd'])

imd_inc = pd.merge(imd,income,how='inner',left_index=True,right_index=True,copy=True)

imd_inc = imd_inc.drop(['msoa11nm_y','lad13cd_y','lad13nm_y'],axis=1).reset_index()
imd_inc.columns = [x.replace("_x","") for x in imd_inc.columns]

#Merging with trip ends data
imd_travel = pd.merge(imd_inc,travel.drop(['lad13cd','lad13nm'],axis=1),how='inner',on=['msoa11cd','msoa11nm'],copy=True)

#Merging with geo-spatial data
imd_travel_geo = pd.merge(imd_travel,geo,how='left',on=['msoa11cd','msoa11nm'],copy=True)

#Merging with area/perimeter data
imd_travel_geo_area = pd.merge(imd_travel_geo,area_perimeter,how='left',on=['msoa11cd','msoa11nm'],copy=True)
item1 = imd_travel_geo_area.set_index(['msoa11cd','msoa11nm'])

#Merging with electricity data
item2 = electricity.set_index(['msoa11cd','msoa11nm'])
all_features = pd.merge(item1,item2,how='inner',left_index=True,right_index=True,copy=True)

all_features = all_features.drop(['lad13cd_y','lad13nm_y'],axis=1).reset_index()
all_features.columns = [x.replace("_x","") for x in all_features.columns]

#Adding metropolitan zoning
#Introducing additional feature to indicate a metroploitan local authority district
london_lad = ['Barking and Dagenham','Barnet','Bexley','Brent','Bromley','Camden','City of London','Croydon',
'Ealing','Enfield','Greenwich','Hackney','Hammersmith and Fulham','Haringey','Harrow','Havering','Hillingdon',
'Hounslow','Islington','Kensington and Chelsea','Kingston upon Thames','Lambeth','Lewisham','Merton','Newham','Redbridge',
'Richmond upon Thames','Southwark','Sutton','Tower Hamlets','Waltham Forest','Wandsworth','Westminster']

greater_man = ['Manchester','Bolton', 'Bury', 'Oldham', 'Rochdale', 'Salford', 'Stockport', 'Tameside', 'Trafford', 'Wigan']
merseyside = ['Liverpool', 'Knowsley', 'St. Helens', 'Sefton', 'Wirral']
south_york = ['Sheffield', 'Barnsley', 'Doncaster', 'Rotherham']
tyne_wear = ['Newcastle upon Tyne', 'Gateshead', 'South Tyneside', 'North Tyneside', 'Sunderland']
west_mid = ['Birmingham', 'Coventry', 'Dudley', 'Sandwell', 'Solihull', 'Walsall', 'Wolverhampton']
west_york = ['Leeds', 'Bradford', 'Calderdale', 'Kirklees', 'Wakefield']

metro_councils = london_lad+greater_man+merseyside+south_york+tyne_wear+west_mid+west_york

all_features['metropolitan'] = all_features.lad13nm.apply(lambda x : 1 if x in metro_councils else 0)


#Merging with chargepoint data
full = pd.merge(all_features,chargers,how='left',on=['msoa11cd','msoa11nm'],copy=True)

full.fillna(0,inplace=True)

new_cols = list(full.iloc[:,:213].columns)+list(full.iloc[:,214:-2].columns)+list(full.iloc[:,213:214].columns)+list(full.iloc[:,-2:].columns)

full = full[new_cols]

full.to_csv("../../data/interim/msoa/full_dataset_msoa.csv",index=False)