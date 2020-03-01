# Scientific computing packages
import numpy as np

#Dataframe related
import pandas as pd

#Statistical Inference
from scipy.stats import norm, expon, poisson, powerlognorm, powernorm, pareto, powerlaw, exponpow

#Data Visualisation
import matplotlib.pyplot as plt
import matplotlib.cm as cm

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
from sklearn.metrics import r2_score,mean_squared_error

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