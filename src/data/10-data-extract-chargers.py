#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import requests
import matplotlib.pyplot as plt
df = pd.read_json("../../data/raw/json/chargepoints_all.json",orient = dict,typ='series')


# In[2]:
#Extracting address information
address_info = pd.DataFrame.from_dict(df.AddressInfo,orient='index')
address_info.columns = ['Address_ID', 'Address_Title', 'AddressLine1', 'AddressLine2', 'Town',
       'StateOrProvince', 'Postcode', 'CountryID', 'Country', 'Latitude',
       'Longitude', 'ContactTelephone1', 'ContactTelephone2', 'ContactEmail',
       'AccessComments', 'RelatedURL', 'Distance', 'DistanceUnit']

#Extracting charger status information
status_type = pd.DataFrame.from_dict(df.StatusType).T
status_type.columns = ['IsOperational', 'IsUserSelectable', 'Status_ID', 'Status_Title']

#Extracting date the charger was registered in database
date_created = pd.DataFrame.from_dict(df.DateCreated,orient='index',dtype='datetime64[ns]',columns=['date_created'])

#Extracting number of chargepoints
connections = pd.DataFrame.from_dict(df.Connections,orient='index')
connections = connections.applymap(lambda x: x['Quantity'] if type(x)==dict else x).sum(axis=1)

#Ensuring that any chargepoint that says there is not charge point has at least 1
connections = connections.map(lambda x : 1 if x == 0 else x)

connections = pd.DataFrame(data=connections,columns=['charge_points'])

#num_points = pd.DataFrame.from_dict(df.NumberOfPoints,orient='index',dtype=int,columns=['num_of_points'])

#Extracting operator information
operator_info = pd.DataFrame.from_dict(df.OperatorInfo).T
operator_info.columns =['WebsiteURL', 'Comments', 'PhonePrimaryContact',
       'PhoneSecondaryContact', 'IsPrivateIndividual', 'AddressInfo',
       'BookingURL', 'ContactEmail', 'FaultReportEmail', 'IsRestrictedEdit',
       'Operator_ID', 'Operator_Title']

#Extracting User type information
usage_type = pd.DataFrame.from_dict(df.UsageType).T
usage_type.columns =['IsPayAtLocation', 'IsMembershipRequired', 'IsAccessKeyRequired', 'Usage_ID',
       'Usage_Title']

#Extracting general information
general = pd.DataFrame.from_dict(df.GeneralComments,orient='index',columns=['general_comments'])


# In[3]:
charge_points = pd.concat([address_info,connections,date_created,operator_info,status_type,usage_type,general],axis=1)


# In[4]:
#Removing duplicate record
charge_points = charge_points.loc[charge_points[['Address_ID']].drop_duplicates(keep='first').index,:]

#Removing disconnected chargepoints
charge_points = charge_points[charge_points.Status_ID != 200]

#Removing spaces in postcodes
charge_points.Postcode = charge_points.Postcode.apply(lambda x : x.strip() if type(x) == str else x)
charge_points.Postcode = charge_points.Postcode.apply(lambda x : " ".join([x[:-3].strip().upper(),x[-3:].strip().upper()]) if type(x) == str else x)

wales = ['Wales','Powys','Pembrokeshire','Gwynedd','Ceredigion']
scotland = ['Aberdeenshire','Scotland','Fife','South Lanarkshire','Highland','Dumfries and Galloway',
            'Midlothian','East Lothian','Perthshire','Ayrshire','Scottish Borders','North Lanarkshire',
           'East Renfrewshire','Wishaw']
n_ireland = ['Northern Ireland','County Antrim']

#Removing chargepoints in Scotland, Wales or Northern Ireland
charge_points = charge_points[(charge_points.Latitude <= 55.833582)&(charge_points.Longitude >=-5.831797)]


for area in scotland:
    charge_points = charge_points[charge_points.StateOrProvince != area]

for area in wales:
    charge_points = charge_points[charge_points.StateOrProvince != area]
    
for area in n_ireland:
    charge_points = charge_points[charge_points.StateOrProvince != area]

    
charge_points.loc['846','Postcode'] = 'CV2 4BF'
charge_points.loc['888','Postcode'] = 'OX11 0QX'
charge_points.loc['150','Postcode'] = 'E8 1FH'

postcode_replace = ['306', '462', '1198', '1342', '1390', '1499', '1601', '1607', '1814', '1895', '2013', '2210', '2214',
                    '2236', '2237', '2238', '2252', '2262', '2281', '2330', '2466', '2575', '2844', '3064', '3095', '3309',
                    '3345', '3493', '3767', '3881', '4264', '4488', '4498', '4942', '5056', '5059', '5128', '5410', '5736',
                    '5779', '6182', '6185', '6197', '6582', '7465', '7590', '7781', '7811', '7814', '7817']

missing_post = pd.read_excel('../../data/interim/find_postcodes.xlsx',index_col=0,usecols=[0,1,2,3,4,5])
missing_post = missing_post.google_address.apply(lambda x : " ".join(x[-10:].split(" ")[-2:]) if len(x[-10:].split(" "))>1 else x)[3:]
missing_post.index = charge_points.loc[postcode_replace,:]['Postcode'].index 

for row,col in charge_points.iterrows():
    for index,z in zip(missing_post.index,missing_post):
        if row == index:
            charge_points.loc[row,'Postcode']=z  
            
charge_points.loc['1895','Postcode'] = 'OX26 1TE'
charge_points.loc['1198','Postcode'] = 'PO15 7FN'
charge_points.loc['2466','Postcode'] = 'LE4 1BS'
charge_points.loc['7817','Postcode'] = 'DH5 9EN'


# In[5]:
#Merging post codes
postcode_data = pd.read_csv("../../data/interim/lsoa_msoa.csv")
postcode_data = postcode_data[['lsoa11cd','lsoa11nm','msoa11cd','msoa11nm','ladcd','ladnm','pcds','region','oa11cd']].drop_duplicates(keep='first').reset_index(drop=True)

charge_points_map = pd.merge(postcode_data,charge_points,how = 'right',right_on='Postcode',left_on = 'pcds')


# In[7]:
charge_points_map = charge_points_map[(charge_points_map.pcds.notna())&(charge_points_map.region == 'England')]
charge_points_map.to_csv("../../data/interim/chargepoints_full.csv",index=False)

# In[8]:
charge_points_lsoa = charge_points_map.groupby(['lsoa11cd','lsoa11nm','msoa11cd','msoa11nm','ladcd','ladnm','region']).agg({'charge_points':sum})
charge_points_lsoa.to_csv("../../data/interim/lsoa/chargepoints_lsoa.csv",index=True)

# In[10]:
charge_points_msoa = charge_points_map.groupby(['msoa11cd','msoa11nm','ladcd','ladnm','region']).agg({'charge_points':sum})
charge_points_msoa.to_csv("../../data/interim/msoa/chargepoints_msoa.csv",index=True)
