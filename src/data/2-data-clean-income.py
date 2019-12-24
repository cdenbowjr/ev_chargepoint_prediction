#Import packages
import pandas as pd
import numpy as np

#Extract socioeconomic data for each LSOA
income = pd.read_excel("../../data/raw/socio_econ/ons-model-based-income-estimates-msoa.xls",sheet_name="2015-16 (annual income)")

income = income.iloc[:,[0,1,2,3,6,10,14,18]]
income.columns = ['msoa11cd','msoa11nm','lad13cd','lad13nm',
                  'total_inc','total_netinc','total_netb4hsing','total_netafterhsing']
#Saving to csv file
income.to_csv("../../data/interim/msoa/income_msoa.csv",index=False)