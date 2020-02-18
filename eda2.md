# Exploratory Data Analysis (EDA) - Feature Variables

###### Predicting Electric Vehicle Charge points locations in Britain

<img src = "/reports/figures/correlations/socio_econ_correlation.jpg" alt = "ev_distribution_england" width=75%/>

------

## Definitions

**EV charge point/charging unit** – a single upstand or wall-mounted structure offering one or more socket outlets or tethered plugs suitable for charging EVs.

**EV charging station** – a physical site with at least one charge point installed suitable for charging at least two EVs. A station usually (but not always) has other physical structures accompanying the charge point(s) such as an energy supply enclosure (feeder pillar), weather shelter, signage, protection barriers for the equipment.

**Middle Layer Super Output Area (MSOA)** - A government tracked area that has a minimum population size of 5,000 and a maximum population size of 15,000

| **Geography** | **Minimum population** | **Maximum population** | **Minimum number of households** | **Maximum number of households** |
| ------------- | ---------------------- | ---------------------- | -------------------------------- | -------------------------------- |
| LSOA          | 1,000                  | 3,000                  | 400                              | 1,200                            |
| MSOA          | 5,000                  | 15,000                 | 2,000                            | 6,000                            |



### Distributions

It was found that most variables (features and target included) had skewed distributions.

**Do the features in the dataset have considerable variance, are they normally distributed?**

1. Only 4.1% of feature variables (11) approached a normal distribution based on a skew criterion of within $\pm 0.5$ and a kurtosis criterion of $\pm3$.
2. The remaining 95.9% had positively skewed distributions
3. 12.5% of feature variables (34) were positively skewed with reasonable kurtosis
4. The `cycle_from_work_nhb` feature had a distribution most similar to the number of EV chargepoints
5. Most variables therefore had substantial amount of outliers
>*The distribution of feature variables are mostly positively skewed with only 4.1% being normally distributed; Significant outliers in the variables exist*

The variables that had *normal distributions* in the data across all MSOAs were:

***Socio-Economic***<br>
1) `chanyp_score`  - the lack of attainment and skills in the local population relating to children and young people<br>
2) `adultskills_score` - the lack of attainment and skills in the local population relating to adult skills<br>
3) `widerbar_score` - the physical and financial accessibility of housing and local services based on access to housing such as affordability (wider barriers)<br>
4) `geo_bar_score` - the physical and financial accessibility of housing and local services based on physical proximity of local services (geographical barriers)<br>
5) `indoor_score` - the quality of the local environment based on quality of housing (indoors)<br>
6) `outdoor_score` - the quality of the local environment based on  air quality and road traffic accidents (outdoors)<br>
7) `heatlh_score` - the risk of premature death and the impairment of quality of life through poor physical or mental health<br>
8) `crime_score` - the risk of personal and material victimisation at local level<br>

<table>
    <tr>
        <td>
            <img src="../reports/figures/eda_graphs/indoor_score_hist_bar.jpg" style= "height:150px">
        </td>
        <td>
            <img src="../reports/figures/eda_graphs/crime_score_hist_bar.jpg" style= "height:150px">
        </td>
    </tr>
</table>

________________________________
***Transport & Car related***<br>
1) `cardriver_from_friends` - average weekday number of journeys done by driving from visit friends (home-based)<br>
2) `two_car` - number of people who own 2 cars in the MSOA<br>
3) `total_cars` - total number of cars in the MSOA<br>

<table>
    <tr>
        <td>
            <img src="../reports/figures/eda_graphs/cardriver_from_friends_hist_bar.jpg" style= "height:150px">
        </td>
        <td>
            <img src="../reports/figures/eda_graphs/crime_score_hist_bar.jpg" style= "height:150px">
        </td>
    </tr>
</table>