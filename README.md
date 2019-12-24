# Predicting Electric Vehicle Charge points locations in Britain

<img src="https://i.cbc.ca/1.4415731.1511448387!/fileImage/httpImage/image.jpg_gen/derivatives/16x9_780/electric-vehicle-charged.jpg"/>

------

## Summary

**This project entailed the building of a machine learning classification model for predicting EV charge point locations based on socio-economic, transportation and geo-spatial characteristics acquired from public and government data.**

It further explored areas of potential for new EV charge point installations using the unsupervised KMeans algorithm to cluster areas with favorable characteristics. 

Raw data was preprocessed in order to ultimately train and test a Logistic Regression classifier and statistical testing of feature coefficients were done to confirm the factors that increased and decreased the likelihood of EV charge point installation. 

------

Preliminary results showed that the probability of an EV charge point being located in an area:

<u>Increases</u>

1. As the number of journeys people took to conduct employers business by car increases
2. As the number of EV car registrations increased in 2018

<u>Decreases</u>

1. As the quality of housing in that area decreases
2. As the deprivation of adult skills set increases



### Document Navigator

|                                                              |                                 |                        |
| ------------------------------------------------------------ | ------------------------------- | ---------------------- |
| <a href="business_problem.md#the-business-problem">The Business Problem</a> | Exploratory Data Analysis (EDA) | Analysis               |
| <a href="data.md#data--methodology">Data & Methodology</a>   | Modelling & Evaluation          | Findings & Conclusions |



## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
