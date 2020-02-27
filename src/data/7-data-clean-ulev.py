import pandas as pd
import numpy as np

#Loading data files containing transportation features
travel = pd.read_csv("../../data/interim/msoa/trip_ends_msoa.csv")
travel.msoa11nm = travel.msoa11nm.apply(lambda x: x.replace("`","'"))



ulev = pd.read_excel("../../data/raw/ev_registration/veh0132.xlsx",header=1,skiprows=5)


lad2msoa = pd.read_csv("../../data/interim/lsoa_msoa.csv")
lad2msoa = lad2msoa.drop(['lsoa11cd','lsoa11nm','pcds','region','oa11cd'],axis=1)
lad2msoa = lad2msoa.drop_duplicates()
lad2msoa = lad2msoa.set_index(['msoa11cd','msoa11nm'])


travel = travel.set_index(['msoa11cd','msoa11nm'])
travel = pd.merge(lad2msoa,travel,left_index=True,right_index=True)

ulev.columns = [x.replace(" ","_").lower() for x in ulev.columns]
ulev.columns = [x.replace('ons_la_code','lad13cd').lower() for x in ulev.columns]
ulev = ulev.drop('region/local_authority',axis=1).dropna()

ulev = ulev[ulev.lad13cd.str.contains(r"^E0").apply(lambda x : False if type(x) == float else x)]
ulev = ulev.loc[:,:'2011_q4'].set_index(['lad13cd'])


#Electric Vehicle owner likely to have 2 or more cars
two_car = travel.reset_index().groupby(['ladcd']).agg({'total_cars':sum}).reset_index()
two_car.columns = ['ladcd', 'two_car_tot']


travel = pd.merge(travel.reset_index(),two_car,on='ladcd')
travel['two_car_frac'] = travel.total_cars/travel.two_car_tot

travel = pd.merge(travel,ulev,left_on='ladcd',right_on ='lad13cd')
travel.loc[:,'2019_q2':'2011_q4'] = travel.loc[:,'2019_q2':'2011_q4'].applymap(lambda x : 4 if x == 'c' else x)
travel.loc[:,'2019_q2':'2011_q4'] = travel.loc[:,'2019_q2':'2011_q4'].multiply(travel.loc[:,'two_car_frac'],axis=0)
travel.columns = [x.replace("ladcd","lad13cd").replace("ladnm","lad13nm") for x in travel.columns]
travel['growth'] = travel['2019_q2']-travel['2011_q4']
travel['growth'] = travel['growth'].apply(lambda x : 0 if x < 0 else x)


travel.to_csv("../../data/interim/msoa/travel_ulev.csv",index=False)