#Import packages
import pandas as pd

#Extract socioeconomic data for each LSOA
imd = pd.read_csv("../../data/raw/socio_econ/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv",low_memory =False)

names = ['lsoa11cd','lsoa11nm','lad13cd','lad13nm','imd_score','imd_rank','imd_decile',
'income_score','income_rank','income_decile','employment_score','employment_rank','employment_decile',
               'education_score','education_rank','education_decile','health_score','health_rank','health_decile','crime_score','crime_rank','crime_decile','housebar_score','housebar_rank','housebar_decile',
               'livenv_score','livenv_rank','livenv_decile','idaci_score', 'idaci_rank','idaci_decile','idaopi_score','idaopi_rank','idaopi_decile','chanyp_score','chanyp_rank','chanyp_decile',
               'adultskills_score','adultskills_rank','adultskills_decile','geo_bar_score','geo_bar_rank','geo_bar_decile','widerbar_score','widerbar_rank','widerbar_decile',
               'indoor_score','indoor_rank','indoor_decile','outdoor_score','outdoor_rank','outdoor_decile','total_pop','under16_pop','16_59_pop',
 'over60_pop','workingage_pop']

#Renaming columns
imd.columns = names

#Ensuring all figures are integers or floats
imd.loc[:,'imd_score':] = imd.loc[:,'imd_score':].applymap(lambda x : eval(x.replace(",","")) if type(x) == str else x)



#Extract MSOA data for each LSOA
lsoa2msoa = pd.read_csv("../../data/raw/geo_spatial/PCD_OA_LSOA_MSOA_LAD_MAY19_UK_LU.csv",encoding = "ISO-8859-1",low_memory=False)

#renaming headers
lsoa2msoa = lsoa2msoa[['lsoa11cd','lsoa11nm','msoa11nm','msoa11cd']].drop_duplicates(keep='first')

#creating indices of multiple deprivationi dataframe
imd = pd.merge(imd,lsoa2msoa,on=['lsoa11cd','lsoa11nm'])

#creating column filter
imd_columns = ['lsoa11cd', 'lsoa11nm',  'msoa11nm', 'msoa11cd','lad13cd', 'lad13nm', 'income_score',
       'income_rank', 'employment_score', 'employment_rank', 'education_score',
       'education_rank', 'health_score', 'health_rank', 'crime_score',
       'crime_rank', 'housebar_score', 'housebar_rank', 'livenv_score',
       'livenv_rank', 'idaci_score', 'idaci_rank', 'idaopi_score',
       'idaopi_rank', 'chanyp_score', 'chanyp_rank', 'adultskills_score',
       'adultskills_rank', 'geo_bar_score', 'geo_bar_rank', 'widerbar_score',
       'widerbar_rank', 'indoor_score', 'indoor_rank', 'outdoor_score',
       'outdoor_rank', 'total_pop', 'under16_pop', '16_59_pop', 'over60_pop',
       'workingage_pop']

#reducing imd dataframe by filtering
imd = imd[imd_columns]

#Saving to csv file
imd.to_csv("../../data/interim/lsoa/imd_lsoa.csv",index=False)

#Creating imd_msoa aggregations
imd = imd.set_index(['lsoa11cd', 'lsoa11nm',  'msoa11nm', 'msoa11cd','lad13cd', 'lad13nm'])

imd1 = imd.groupby(['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm']).agg('mean').iloc[:,0:30:2]
imd2 = imd.groupby(['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm']).agg('sum').iloc[:,1:30:2]
imd3 = imd.groupby(['msoa11nm', 'msoa11cd','lad13cd', 'lad13nm']).agg('sum').iloc[:,30:]

imd_msoa = pd.concat([imd1,imd2,imd3],axis=1).reset_index()

#Saving to csv file
imd_msoa.to_csv("../../data/interim/msoa/imd_msoa.csv",index=False)

print(imd_msoa.head())