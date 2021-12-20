# Predicting Electric Vehicle Charging Station locations in Britain

<img src="https://i.cbc.ca/1.4415731.1511448387!/fileImage/httpImage/image.jpg_gen/derivatives/16x9_780/electric-vehicle-charged.jpg"/>

------

## Summary

**This project entailed building a machine learning classification model for predicting the presence of EV charging stations in a location based on socio-economic, transportation and geo-spatial characteristics acquired from public and government data.**

The model was then used to further explored areas of potential for new EV charge point installations using the unsupervised KMeans algorithms to cluster areas with favorable characteristics from the classification model. 

Raw data was preprocessed in order to ultimately train and test a Logistic Regression classifier and statistical testing of feature coefficients were done to confirm the factors that increased or decreased the likelihood of EV charge point installation. 

[click for the EDA app](https://evchargeapp-v2.uc.r.appspot.com/)

------

## Findings

Statistical results showed that the probability of an EV charge point being located in an area:

***Increases***

1. As the 2018:
   - absolute non-domestic electricity consumption in the area increases
   - median domestic electricity consumption in the area increases
   - ratio of domestic electricity consumption and non-domestic electricity consumption in the area increases
2. As the Ultra low emission vehicles (ULEVs) licensed at the end of 2017 Q3 and the end of 2019 Q1 in the area increases
3. As the average weekday number of journeys done:
   - by driving to/from employers business increases
   - by rail to/from shopping increases
   - by bus/coach to/from holidays increases
4. As physical accessibility of housing and local services gets harder

****

***Decreases***

1. As the 2018:
   - ratio of median domestic electricity consumption and median 2018 non-domestic electricity consumption in the area increases
   - mean domestic electricity consumption in the area increases
2. As the Ultra low emission vehicles (ULEVs) licensed at the end of 2015 Q2 in the area increases
3. As the average weekday number of journeys done:
   - by rail to/from work increases
   - by cycling to/from holidays increases
4. If the area is classified as a metropolitan area
5. As the lack of attainment and skills of adults in the local population increases
6. As the quality of housing (indoors) decreases

____

### Definitions

**EV charge point/charging unit** – a single upstand or wall-mounted structure offering one or more socket outlets or tethered plugs suitable for charging EVs.

**EV charging station** – a physical site with at least one charge point installed suitable for charging at least two EVs. A station usually (but not always) has other physical structures accompanying the charge point(s) such as an energy supply enclosure (feeder pillar), weather shelter, signage, protection barriers for the equipment.

**Middle Layer Super Output Area (MSOA)** - A government tracked area that has a minimum population size of 5,000 and a maximum population size of 15,000

| **Geography** | **Minimum population** | **Maximum population** | **Minimum number of households** | **Maximum number of households** |
| ------------- | ---------------------- | ---------------------- | -------------------------------- | -------------------------------- |
| LSOA          | 1,000                  | 3,000                  | 400                              | 1,200                            |
| MSOA          | 5,000                  | 15,000                 | 2,000                            | 6,000                            |

___

### Navigator

<table>
    <th align='left'>Previous</th>
    <th align='right'>Next</th>
    <tr>
    	<td align='left' width='50%'>Summary</td>
    	<td align='right' width="50%"><a href="business_problem.md#the-business-problem">The Business Problem >></a></td>
    </tr>
</table>
____

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
