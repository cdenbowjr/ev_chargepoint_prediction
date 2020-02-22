#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Scientific computing packages
import numpy as np

#Dataframe related
import pandas as pd

#Statistical Inference
from scipy.stats import norm, expon, poisson, powerlognorm, powernorm, pareto, powerlaw, exponpow

#Data Visualisation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

#Data wrangling and webscraping
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


#Machine Learning functions
from sklearn.preprocessing import PowerTransformer, StandardScaler, MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin

#Dimensionality Reduction algorithms
from sklearn.decomposition import PCA

#Modelling algorithms and model evaluation tools
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import cross_val_score

#Regular expressions and textual editing
import re
from textwrap import wrap
from tabulate import tabulate

#Other packages
import time
import random

#Loading image related packages
import json
import folium
from pandas.io.json import json_normalize
from shapely.geometry import Point,Polygon,LineString,MultiPolygon

#import postcodes_io_api
#api  = postcodes_io_api.Api(debug_http=True)


#Function to Load geojson file and convert to dataframe
def load_geojson(filepath):
    '''Function that loads a geojson file and converts it to a dataframe'''
    with open(filepath) as file:
        data = json.load(file)

    return json_normalize(data=data['features'])


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