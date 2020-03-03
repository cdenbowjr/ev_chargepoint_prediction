# Scientific computing packages
import numpy as np

# Dataframe related
import pandas as pd

# Statistical Inference
from scipy.stats import norm

# Data Visualisation# Geo-spatial Functions
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import json
import folium

from shapely.geometry import Polygon

# Machine Learning functions
from sklearn.preprocessing import PowerTransformer, StandardScaler, MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin


# Regular expressions and textual editing
import requests
import re
from textwrap import wrap
from tabulate import tabulate

# Data dictionary
try:
    from src.data.data_dictionary import EV_britain
except:
    print("hello")

class TransportAggregate(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass#self.columns = columns

    def fit(self, X, y=None):
        return self


    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        new_columns = []
        old_columns = []
        Y = X.copy()
        for x in range(0,Y.shape[1],2):
            two_variables = Y.iloc[:,x:x+2].columns
            old_columns.extend(two_variables)
            mode = two_variables[0].split("_")[0]
            if two_variables[0].split("_")[-1] == 'nhb':

                activity = "_".join([two_variables[0].split("_")[-2],two_variables[0].split("_")[-1]])
            else:
                activity = two_variables[0].split("_")[-1]

            new_columns.append(f'{mode}_{activity}')
            Y[f'{mode}_{activity}'] = Y.iloc[:,x:x+2].sum(axis=1)

        Y = Y.drop(old_columns,axis=1)

        old_columns = []
        for x in range(0,Y.shape[1]-8):
            first = Y.iloc[:,x].name
            second = Y.iloc[:,x+8].name
            if first.split("_")[0]==second.split("_")[0]:
                Y[first] = Y[first]+Y[second]
                old_columns.append(second)
                #print(first,second)

        Y = Y.drop(old_columns,axis=1)

        X = Y

        return X

# Function to Load geojson file and convert to dataframe

def load_geojson(filepath):
    '''Function that loads a geojson file and converts it to a dataframe'''
    try:
        with open(filepath) as file:
            data = json.load(file)

        return pd.json_normalize(data=data['features'])

    except:
        data = requests.get(filepath).json()
        return pd.json_normalize(data=data['features'])

# Defining function to convert dataframe back to geojson
def df_to_geojson(df, properties):
    '''Function that converts dataframe to geojson format'''
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        if row['geometry.type'] == "Polygon":
            feature = {'type': 'Feature',
                       'properties': {},
                       'geometry': {'type': 'Polygon', 'coordinates': []}}
        else:
            feature = {'type': 'Feature',
                       'properties': {},
                       'geometry': {'type': 'MultiPolygon', 'coordinates': []}}
        feature['geometry']['coordinates'] = row["geometry.coordinates"]

        for prop in properties:
            feature['properties'][re.search(r"properties.(\w.*)", prop).group(1)] = row[prop]
        geojson['features'].append(feature)
    return geojson


# Function to extract centroids from polygons and multipolygons
def centroid_calc(x):
    '''Function that extracts the centroids from a polygon or multipolygon'''
    if x['geometry.type'] == "Polygon":
        lat = Polygon(x['geometry.coordinates'][0]).centroid.xy[1][0]
        long = Polygon(x['geometry.coordinates'][0]).centroid.xy[0][0]
        return lat, long
    else:

        lat = Polygon(x['geometry.coordinates'][0][0]).centroid.xy[1][0]
        long = Polygon(x['geometry.coordinates'][0][0]).centroid.xy[0][0]

        return lat, long

# Function to plot histograms with text

def plot_hist_box(variable, dataframe, datadict,
                  shape=norm,
                  rug=False,
                  width=10,
                  length=3,
                  fontsize=10):
    '''This function simply plots a histogram and barplot of the variable assigned to it'''

    fig, ax = plt.subplots(1, 2, figsize=(width, length))
    sns.boxplot(x=variable, data=dataframe, orient='h', ax=ax[1])
    sns.distplot(a=dataframe[variable],
                 ax=ax[0],
                 fit=shape,
                 rug=rug,
                 hist_kws=dict(ec='k'),
                 kde=False)
    # ax[0].text(s=(EV_britain().description[variable]),x=0,y=-0.3,wrap=True,ha='left',transform=ax[0].transAxes)
    fig.suptitle(
        'Distribution of %s\n %s' %
        (variable, "\n".join(wrap(datadict.description[variable]))),
        fontsize=fontsize,
        va='bottom',
    )
    plt.savefig("../reports/figures/" + variable + "_hist_bar.jpg",
                dpi=144,
                quality=100,
                bbox_inches='tight')
    plt.show()


def print_statistics(variable, df):
    '''Basic function just prints mean, median skew, kurtosis and standard deviation'''

    skew = df[variable].skew()
    kurtosis = df[variable].kurtosis()
    the_mean = df[variable].mean()
    the_median = df[variable].median()
    the_std = df[variable].std()

    print(f"Variable name: {df[variable].name}", end="\n")
    print(f"Mean: {the_mean:.3f} ", end="\n")
    print(f"Median: {the_median:.3f} ", end="\n")
    print(f"StdDev: {the_std:.3f} ", end="\n")
    print(f"Skew: {skew:.3f} ", end="\n")
    print(f"Kurtosis:{kurtosis:.3f}")


# Creating histogram plotting function for original individual feature


def plot_original_hist(variable, df):

    fig, ax = plt.subplots(figsize=(5, 5))
    df[variable].hist(bins=30, color=cm.winter(0.7), ec='k', ax=ax)
    ax.set_xlabel(f"{variable}", fontsize=20)
    ax.set_ylabel("frequency", fontsize=20)
    ax.grid(False)
    plt.savefig("../reports/figures/histograms/" + variable +
                "_hist_original.jpg",
                dpi=800,
                transparent=False,
                edgecolor='k',
                facecolor='w',
                pad_inches=0.1,
                bbox_inches='tight')
    return display()


def plot_transformed_hist(variable, df):

    fig, ax = plt.subplots(figsize=(5, 5))
    df[variable].hist(bins=30, color=cm.winter(0.7), ec='k', ax=ax)
    ax.set_xlabel(f"{variable}", fontsize=20)
    ax.set_ylabel("frequency", fontsize=20)
    ax.grid(False)
    plt.savefig("../reports/figures/histograms/" + variable +
                "_hist_transform.jpg",
                dpi=800,
                transparent=False,
                edgecolor='k',
                facecolor='w',
                pad_inches=0.1,
                bbox_inches='tight')
    return display()


# Function to table the skew in distributions based on specific criteria
def statistic_table(df, start, end, criteria):
    '''Function returns a statistic table by entering a start variable, end variable and skew criteria'''
    stats_table = pd.DataFrame()
    var_skew = df.loc[:, start:end].skew().round(3)
    var_mean = df.loc[:, start:end].mean().round(3)
    var_kurt = df.loc[:, start:end].kurtosis().round(3)
    stats_table = pd.concat([stats_table, var_skew > criteria])
    stats_table = pd.concat([stats_table, var_skew], axis=1)
    stats_table = pd.concat([stats_table, var_kurt], axis=1)
    stats_table = pd.concat([stats_table, var_mean], axis=1)
    stats_table.columns = ['skewed?', 'skew', 'kurtosis', 'mean']
    stats_table = stats_table.sort_values(by='skew', ascending=False)
    return stats_table


def markdown_table(df, start, end, criteria):
    '''This prints out a markdown table by entering variables from a dataframe'''
    table = statistic_table(df,start, end, criteria)

    print(
        tabulate(table,
                 headers=['variable', 'skewed?', 'skew', 'kurtosis', 'mean'],
                 tablefmt="github"))


# Writing a function to display transformed features in a dataframe(Box Plot + Interactive Histogram)

def make_markdown_table(df,varlist1, varlist2, n):
    '''Function returns markdown table once given features and targets and the number of correlated variables'''

    data = search_corr(df,varlist1, varlist2, n).iloc[:, -3:]
    headers = data.columns
    print(tabulate(data, headers=headers, tablefmt="github"))


def get_features(df,start,
                 end,
                 power=False,
                 log=False,
                 stand=False,
                 aggreg=False,
                 remove=[]):
    '''Function performs transformation of variables in a dataframe (logarithmic, power, aggregation, standardisation'''
    features = df.loc[:, start:end]
    features = features.drop(remove, axis=1)
    features_col = features.columns

    if aggreg == True:
        features = TransportAggregate().fit_transform(features)
        features_col = features.columns

    if log == True:
        features = features.apply(lambda x: np.log1p(x))
        features = pd.DataFrame(features, columns=features_col)

    if power == True and np.any(features <= 0) == True:

        features = PowerTransformer('yeo-johnson').fit_transform(features)
        features = pd.DataFrame(features, columns=features_col)

    elif power == True and np.any(features <= 0) == False:
        # print(PowerTransformer('box-cox').fit(features).lambdas_)
        features = PowerTransformer('box-cox').fit_transform(features)
        features = pd.DataFrame(features, columns=features_col)

    if stand == 1:
        features = StandardScaler().fit_transform(features)
        features = pd.DataFrame(features, columns=features_col)
    elif stand == 2:
        features = MinMaxScaler().fit_transform(features)
        features = pd.DataFrame(features, columns=features_col)

    else:
        stand == 0
        pass

    return features


# Writing a function to plot transformed features in a Box Plot


def transform_and_plot(df,start,
                       end,
                       power=False,
                       log=False,
                       stand=False,
                       aggreg=False,
                       remove=[],
                       ax=None):

    if remove is None:
        remove = []
    features = get_features(df,start, end, power, log, stand, aggreg, remove)
    sns.set_style(style='white')

    # plt.savefig("../reports/figures/boxplots/"+file)

    return sns.boxplot(data=features,
                       orient='h',
                       notch=False,
                       ax=ax,
                       palette='winter')


def search_corr(df, features, targets, n):
    '''Function returns the top (n) number of highest correlated variables with the target'''
    features_df = df.loc[:, features]
    targets_df = df.loc[:, targets]
    matrix = pd.concat([features_df, targets_df], axis=1).corr()
    sort_list = matrix[targets].apply(lambda x: abs(x)).sort_values(
        by=targets[0], ascending=False).iloc[3:3 + n, :].index
    return matrix.loc[sort_list, :].round(3)


def just_plot(df, axis_loc,variable_list, target_list, vmin=-1, vmax=1):
    '''Function plots truncated heatmap with target variables'''
    list1 = variable_list
    list2 = target_list
    matrix = pd.concat([df.loc[:, list1], df.loc[:, list2]],
                       axis=1).corr()
    mask = np.zeros_like(matrix, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    return sns.heatmap(round(matrix, 2), mask=mask, annot=True, cmap='winter',vmin=vmin,vmax=vmax,ax=axis_loc)


def centroid_calc(x):
    '''Function to extract centroids from polygons and multipolygons'''
    if x['geometry.type'] == "Polygon":
        lat = Polygon(x['geometry.coordinates'][0]).centroid.xy[1][0]
        long = Polygon(x['geometry.coordinates'][0]).centroid.xy[0][0]
        return lat, long
    else:

        lat = Polygon(x['geometry.coordinates'][0][0]).centroid.xy[1][0]
        long = Polygon(x['geometry.coordinates'][0][0]).centroid.xy[0][0]

        return lat, long


def plot_area(merged_df, feature_var,lat=1,long=1, *args):
    try:
        search_area = merged_df[merged_df['properties.msoa11nm'].str.contains(
            '|'.join(args))]
        search_area_json = df_to_geojson(search_area, [
            'properties.msoa11cd', 'properties.msoa11nm',
            'properties.objectid', 'properties.st_areashape',
            'properties.st_lengthshape'
        ])

        with open('search.geojson', 'w') as json_file:
            json.dump(search_area_json, json_file)

        start_lat = search_area.apply(centroid_calc,
                                      axis=1).apply(lambda x: x[0]).mean()
        start_lon = search_area.apply(centroid_calc,
                                      axis=1).apply(lambda x: x[1]).mean()

        area_map = folium.Map(location=(start_lat, start_lon), zoom_start=11)
        legendname = EV_britain().description[feature_var]

        # try:
        #     legendname = EV_britain().description[feature_var]
        #     #print("this is the try")
        #
        # except:
        #     legendname = EV_britain().description[feature_var]
        #     #print("this is the except")

        area_map.choropleth(
            geo_data='search.geojson',
            data=search_area,
            columns=["properties.msoa11cd", feature_var],
            key_on='feature.properties.msoa11cd',
            fill_color='Spectral_r',
            highlight=True,
            name="areas",
            legend_name=legendname)

        folium.Marker(location=(lat,long)).add_to(area_map)

        folium.LayerControl().add_to(area_map)
        area_map.save("search.html")

    except:

        print("This is not a council area in London")


def pcd_dict(df):
    return {pcd: msoa for pcd, msoa in zip(df.pcds, df.msoa11cd)}