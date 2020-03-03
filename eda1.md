# Exploratory Data Analysis (EDA) - Target Variable

###### Predicting Electric Vehicle Charge points locations in Britain

<img src = "/reports/figures/EV_charging_station_dist.jpg" alt = "ev_distribution_england" width=75%/><br>*Spatial EV charge point distribution for England*

____

## Approach

The EDA approach will be to investigate the following:
1. The target variable (EV charge points) - how it is distributed across England spatially and by location category.
2. The feature variables - how the data is distributed (normal, skewed etc)
3. Outliers within the feature variables - whether they exist, whether they can be removed or transformed
4. The Correlation between the feature variables and the target variable



#### What category of place will I find EV charging stations in England according to Google? How many charge points will there be?

`Majority of EV charging stations are located in establishments. About 1 in 5 are located in street parking or a residential premise. There are close to 20,000 registered EV charge points in England based on the data`

<img src="/reports/figures/EV_charging_stations_breakdown.jpg" width=50% /><br>*Figure 1 - EV charging stations by Google Maps API categorisation*

<u>Summary</u>

> - **6,216 EV charging stations** are distributed across England (equivalent to **19,582 EV charge points**)
> - **78.4% of EV charging stations** are located in **establishments**
> - The remaining **20.6% of EV charging stations** are located in **street parking** and on **residential premises**<br>

------

#### What kind of establishment are the EV charge stations located in?

`EV charging stations are located mainly in retail, restaurant and hotel lodging establishments. Car parks, public transportation and hotels have close to an average of 4 charge points for every charging station`

<img src="/reports/figures/EV_charging_stations_est.jpg" width=50%/><img src="/reports/figures/EV_charge_points_est.jpg" width=50%/><br> *Figure 2 - Breakdown of EV charging stations in establishments (left); EV charge points per charging station (right)*



*Table 1 - Top 6 establishment categories for charging stations*

| Establishment category             | % of charging stations | Average number of charge points |
| ---------------------------------- | ---------------------- | ------------------------------- |
| Retail/Stores                      | 27                     | 3.2                             |
| Restaurants, Bars & Cafes          | 24.5                   | 3.1                             |
| Lodgings and Hotels                | 19                     | 2.3                             |
| Public/Private Parking             | 13.8                   | 3.8                             |
| Car Dealership, Repair or Car Wash | 11.2                   | 2.4                             |
| Supermarket, grocery or pharmacy   | 9.2                    | 3.7                             |



*Table 2 - Top 6 establishment categories for highest average number of charge points per charging station*

| Establishment category           | Average number of charge points |
| -------------------------------- | ------------------------------- |
| Public/Private Parking           | 3.8                             |
| Public Transportation            | 3.8                             |
| Supermarket, grocery or pharmacy | 3.7                             |
| Gas Stations                     | 3.4                             |
| Banks                            | 3.3                             |
| Retail/Stores                    | 3.2                             |

------

#### How are charge points distributed across England?

`Just over 50% of areas in the country have no EV charge point`

*Table 3 - Charge point frequency table*

| Number of charge points | Number of MSOAs | % of MSOAs |
| :---------------------: | :-------------: | :--------: |
|            0            |      3781       |    55.7    |
|           1-5           |      1936       |    28.5    |
|          6-10           |       648       |    9.5     |
|          11-15          |       199       |    2.9     |
|          16-20          |       93        |    1.4     |
|           20+           |       134       |    2.0     |
|          Total          |      6791       |    100     |



<img src="/reports/figures/charge_point_hist.jpg" width=75%/> <br>*Figure 3 - Numerical EV Charge point distribution for England*

____

### The Code

[Click here for the Python Code](/notebooks/1.0-ced-chargepoint-analysis.ipynb)

____

### Navigator

<table>
    <th align='left'>Previous</th>
    <th align='right'>Next</th>
    <tr>
    	<td align='left'><a href="data.md#data--methodology"><< Data & Methodology</a>	</td>
    	<td align='right'><a href="eda2.md#exploratory-data-analysis-eda---feature-variables">Exploratory Data Analysis II >></a></td>
    </tr>
</table>

[Back to Beginning](https://github.com/cdenbowjr/ev_chargepoint_prediction#predicting-electric-vehicle-charge-points-locations-in-britain)