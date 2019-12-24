import os
import pandas as pd


#Declaring path for trip ends excel files for every MSOA
search_path = "../../data/raw/transport"

#Creating list of folders
list_of_folders = [x for x in os.listdir(search_path)]

list_of_excel_tabs = {"Walk":"walk","Cycle":"cycle","Car Driver":"cardriver",
                      "Car Passenger":"carpassenger","BusCoach":"buscoach","RailUnderground":"rail"}


for folder in list_of_folders:
    travel_data = [folder for folder in os.listdir(search_path+'/'+folder) if "car_own" not in folder]
    car_own_data = [folder for folder in os.listdir(search_path+'/'+folder) if "car_own" in folder]
    
    for travel,car_own in zip(travel_data,car_own_data):
        final_df = pd.DataFrame()
        print(search_path+"/"+folder+"/"+travel)

        #Extracting trip ends for 2018 from each MSOA

        for num, traveltype in enumerate(list_of_excel_tabs.items()):
            df = pd.read_excel(search_path+"/"+folder+"/"+travel,sheet_name=traveltype[0],header=None)

            start_row = df[df.iloc[:,0] == "Base Year"].index[0]+3
            end_row = df[df.iloc[:,0] == "Future Year"].index[0]-1

            df = df.iloc[start_row:end_row,:]

            travel_headers = ["msoa11cd", "msoa11nm", "to_work","from_work","to_empbus","from_empbus","to_school","from_school",
                          "to_shopping", "from_shopping","to_personbus","from_personbus","to_social","from_social","to_friends",
                          "from_friends","to_holiday", "from_holiday","to_work_nhb","from_work_nhb","to_empbus_nhb",
                          "from_empbus_nhb","to_school_nhb","from_school_nhb","to_shopping_nhb", "from_shopping_nhb","to_personbus_nhb","from_personbus_nhb",
                          "to_social_nhb","from_social_nhb","to_holiday_nhb","from_holiday_nhb"]

            df.columns = travel_headers
            df.set_index(["msoa11cd","msoa11nm"],inplace=True)

            df.columns = df.columns.map(lambda x : traveltype[1]+"_"+x)

            if num == 0:
                final_df = df

            else:
                final_df = pd.merge(final_df,df,on=['msoa11cd','msoa11nm'])


        print(search_path+"/"+folder+"/"+car_own)
        
        df2 = pd.read_excel(search_path+"/"+folder+"/"+car_own,sheet_name="Car Ownership",header=None)

        start_row = df2[df2.iloc[:,0] == "Base Year"].index[0]+2
        end_row = df2[df2.iloc[:,0] == "Future Year"].index[0]-2

        df2 = df2.iloc[start_row:end_row,:]

        own_headers = ["msoa11cd", "msoa11nm", "no_car","one_car","two_car","three+_car","total_cars"]

        df2.columns = own_headers
        df2.set_index(["msoa11cd","msoa11nm"],inplace=True)
        
        df2['region'] = folder

        
        prime_df = pd.merge(final_df,df2,on=['msoa11cd','msoa11nm'])
        
        prime_df.to_csv("../../data/interim/msoa/trip_ends/"+travel[:-4]+"csv")


#print(final_df.head())