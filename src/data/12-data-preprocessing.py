from src.data import preprocessing_functions as ppf

import pandas as pd
from sklearn.pipeline import FeatureUnion,make_pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler,PowerTransformer
from sklearn.impute import SimpleImputer

df = pd.read_csv('../../data/interim/msoa/full_dataset_msoa.csv')

categories = df.loc[:,'msoa11cd':'lad13nm']

part1_droplist = ['education_score','housebar_score','livenv_score','health_score','crime_score','chanyp_score']
part4_droplist = ['two_car_tot','two_car_frac']

#Columns for processing in the pipeline
part1 = df.loc[:,"income_score":"adultskills_score"].drop(part1_droplist,axis=1).columns
part1a = df.loc[:,"health_score":"outdoor_score"].drop(['housebar_score','livenv_score','idaci_score','idaopi_score','adultskills_score'],axis=1).columns
part2 = df.loc[:,"total_pop":"total_netafterhsing"].columns
part3 = df.loc[:,'walk_to_work':'rail_from_holiday_nhb'].columns
part4 = df.loc[:,'no_car':'2011_q4'].drop(part4_droplist,axis=1).columns
part5 = df.loc[:,'num_parks':'supermarkets_distance'].columns
part6 = df.loc[:,'elec_d_con':'residential_mdn_ratio'].columns
part7 = df.loc[:,'charge_points':].columns

preprocess_pipeline = FeatureUnion(n_jobs=-1,transformer_list=[
    ('socio_econ1',make_pipeline(
            ppf.ColumnSelector(part1),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    ),
    ('socio_econ1a',make_pipeline(
            ppf.ColumnSelector(part1a),
            PowerTransformer('yeo-johnson'),
            SimpleImputer(strategy="median"))
    ),
    ('pop_income',make_pipeline(
            ppf.ColumnSelector(part2),
            ppf.FeatureLogTransform(),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    ),
    ('transport',make_pipeline(
            ppf.ColumnSelector(part3),
            ppf.TransportAggregate(),
            ppf.FeatureLogTransform(),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    ),
    ('car_own',make_pipeline(
            ppf.ColumnSelector(part4),
            ppf.FeatureLogTransform(),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    ),
    ('geo_spatial',make_pipeline(
            ppf.ColumnSelector(part5),
            ppf.FeatureLogTransform(),
            PowerTransformer('yeo-johnson'),
            SimpleImputer(strategy="median"))
    ),
    ('electricity',make_pipeline(
            ppf.ColumnSelector(part6),
            ppf.FeatureLogTransform(),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    ),
    ('metro',make_pipeline(
            ppf.ColumnSelector(df[['metropolitan']].columns),
            MinMaxScaler())
    ),
    ('target',make_pipeline(
            ppf.ColumnSelector(df[['charge_points']].columns),
            StandardScaler(with_mean=False,with_std=False))
    )
])

def get_col_names(df):
    socio_econ1 = ppf.ColumnSelector(part1).fit_transform(df).columns
    socio_econ1a = ppf.ColumnSelector(part1a).fit_transform(df).columns
    pop_income = ppf.ColumnSelector(part2).fit_transform(df).columns
    transport = ppf.ColumnSelector(part3).fit_transform(df)
    transport = ppf.TransportAggregate().fit_transform(transport).columns
    car_own = ppf.ColumnSelector(part4).fit_transform(df).columns
    geo_spatial = ppf.ColumnSelector(part5).fit_transform(df).columns
    electricity = ppf.ColumnSelector(part6).fit_transform(df).columns
    metro = ppf.ColumnSelector(df[['metropolitan']].columns).fit_transform(df).columns
    charge_points = ppf.ColumnSelector(df[['charge_points']].columns).fit_transform(df).columns
    return list(socio_econ1)+list(socio_econ1a)+list(pop_income)+list(transport)+list(car_own)+list(geo_spatial)+list(electricity)+list(metro)+list(charge_points)

data = pd.DataFrame(preprocess_pipeline.fit_transform(df),columns=get_col_names(df))

#print(data.head())
# print(part1)
# print(part1a)
# print(part2)
# print(part3)
#print(part4)
# print(part5)
# print(part6)
# print(part7)

categories.join(data).to_csv('../../data/processed/full_processed_data.csv',index=False)

#print(ppf.FeatureLogTransform().fit_transform(ppf.ColumnSelector('two_car_tot').fit_transform(df)))

#print(type(ppf.ColumnSelector('two_car_tot').fit_transform(df)))

pipe = FeatureUnion(n_jobs=-1,transformer_list=[
    ('socio_econ1',make_pipeline(
        ppf.ColumnSelector(part1),
        PowerTransformer('box-cox'),
        SimpleImputer(strategy="median"))
     ),
    ('socio_econ1a',make_pipeline(
            ppf.ColumnSelector(part1a),
            PowerTransformer('yeo-johnson'),
            SimpleImputer(strategy="median"))
    ),
    ('pop_income',make_pipeline(
            ppf.ColumnSelector(part2),
            ppf.FeatureLogTransform(),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    ),
    ('transport',make_pipeline(
            ppf.ColumnSelector(part3),
            ppf.TransportAggregate(),
            ppf.FeatureLogTransform(),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    ),
    ('car_own',make_pipeline(
            ppf.ColumnSelector(part4),
            ppf.FeatureLogTransform(),
            PowerTransformer('box-cox'),
            SimpleImputer(strategy="median"))
    )
])

#print(pipe.fit_transform(df))