import pandas as pd
#Extract MSOA data for each LSOA
lsoa2msoa = pd.read_csv("../../data/raw/geo_spatial/PCD_OA_LSOA_MSOA_LAD_MAY19_UK_LU.csv",encoding = "ISO-8859-1",low_memory=False)

lsoa2msoa['region'] = lsoa2msoa.oa11cd.apply(lambda x: 'Northern Ireland' if 'N' in str(x) 
                                                       else 'Scotland' if 'S' in str(x) 
                                                       else 'Wales' if 'W' in str(x)
                                             
                                             else 'England' if 'E' in str(x)
                                             else 'Other')

lsoa2msoa = lsoa2msoa[['oa11cd','lsoa11cd','lsoa11nm','msoa11nm','msoa11cd','ladcd','ladnm','pcds','region']].drop_duplicates(keep='first')

filters = lsoa2msoa.msoa11cd.apply(lambda x : False if ('S' in str(x)) or ('L' in str(x)) or ('W' in str(x)) or ('N' in str(x)) or ('M' in str(x)) else True)

lsoa2msoa = lsoa2msoa[filters].dropna()

lsoa2msoa.sort_index().to_csv("../../data/interim/lsoa_msoa.csv",index=False)