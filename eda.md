# Exploratory Data Analysis (EDA)

###### Predicting Electric Vehicle Charge points locations in Britain

<img src = "/reports/figures/EV_charging_station_dist.jpg" alt = "ev_distribution_england" width=75%/>

------



## Definitions

**EV charge point/charging unit** – a single upstand or wall-mounted structure offering one or more socket outlets or tethered plugs suitable for charging EVs.

**EV charging station** – a physical site with at least one charge point installed suitable for charging at least two EVs. A station usually (but not always) has other physical structures accompanying the charge point(s) such as an energy supply enclosure (feeder pillar), weather shelter, signage, protection barriers for the equipment.

**Middle Layer Super Output Area (MSOA)** - A government tracked area that has a minimum population size of 5,000 and a maximum population size of 15,000

| **Geography** | **Minimum population** | **Maximum population** | **Minimum number of households** | **Maximum number of households** |
| ------------- | ---------------------- | ---------------------- | -------------------------------- | -------------------------------- |
| LSOA          | 1,000                  | 3,000                  | 400                              | 1,200                            |
| MSOA          | 5,000                  | 15,000                 | 2,000                            | 6,000                            |

## Approach

The EDA approach will be to investigate the following:
1. The target variable (EV charge points) - how it is distributed across England spatially and by location category.
2. The feature variables - how the data is distributed (normal, skewed etc)
3. Outliers within the feature variables - whether they exist, whether they can be removed or transformed
4. The Correlation between the feature variables and the target variable



## Initial Results & Descriptive Analysis

#### What type of places will I find EV charging stations in England? How many charge points will there be?

`Overall EV charge points and subsequent charging stations are predominately located in retail, restaurant and hotel lodging establishments. There close to 20,000 registered EV charge points in England based on the data`

<img src="/reports/figures/EV_charging_stations_breakdown.jpg" width=50% />

*Overview*

- There were **6,216 EV charging stations** distributed across England which were equivalent to **19,582 EV charge points**
- **78.4% of EV charging stations** were located in **establishments**
- The remaining **20.6% of EV charging stations** were located in **street parking** and on **residential premises**

<img src="/reports/figures/EV_charging_stations_est.jpg" width=50%/><img src="/reports/figures/EV_charge_points_est.jpg" width=50%/>

*For charging stations associated with establishments:*

- **27%** were linked to **retail/store** activity
- **24.5%** were linked to a **restaurant, bar or cafe**
- **19%** were linked to **lodgings or hotels**
- **13.8%** were linked to **public and private parking**
- **11.2%** were linked to a **car dealership, car repair shop or a car wash**
- **9.2%** were linked to a **supermarket, grocery or pharmacy**



Average number of EV charge points per charging station*

- **4 charge points** on average associated with **parking, public transport and supermarkets**
- **2 charge points** on average associated with **religious and government entities, car dealerships and hotel lodgings**
- Every other location had about 3 charge points per charging station



## EV charge point distribution per MSOA

- There are **6,791 MSOAs** distributed across England
- **3,012** of these areas have at least 1 EV charge point (representing **44.4%**)
- The remaining **3,779** areas have no EV charge point (representing **55.6%**)<br>

<iframe src="http://www.google.com"></iframe>

|                                                              |                                                          |                        |
| ------------------------------------------------------------ | -------------------------------------------------------- | ---------------------- |
| <a href="business_problem.md#the-business-problem">The Business Problem</a> | <a href="eda.md#eda">Exploratory Data Analysis (EDA)</a> | Analysis               |
| <a href="data.md#data--methodology">Data & Methodology</a>   | Modelling & Evaluation                                   | Findings & Conclusions |

[Back to Beginning](https://github.com/cdenbowjr/ev_chargepoint_prediction#predicting-electric-vehicle-charge-points-locations-in-britain)