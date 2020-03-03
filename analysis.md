# Analysis & Statistical Inference

![](/reports/figures/analysis/coefficient_comparison.jpg)

Based on the top 20 coefficients with the highest absolute value the following inferences can be drawn

____

### Logistic Regression

The probability of an EV charge point being located in an area:

***Increases***

1. As the average weekday number of journeys done by driving to/from employers business increases
2. As the average weekday number of journeys done by rail to/from shopping increases
3. As the average weekday number of journeys done by bus/coach to/from holidays increases

***Decreases***

1. As the average distance of a car park from the centre of the MSOA increases
2. As the lack of attainment and skills in the local population relating to adult skills increases
3. As the deprivation of adult skills set increases

____

### Linear Support Vector Machines (SVM)

The probability of an EV charge point being located in an area:

***Increases***

1. As the 2018 non-domestic electricity consumption increases
2. As the number of car parks within the area increases
3. As the average weekday number of journeys done by driving to/from employers business increases

***Decreases***

1. As the average weekday number of journeys done by rail to/from work increases
2. As the number of non-domestic electricity meters within the area increases



### Statistical Analysis

A regularised logistic regression model was run using the statsmodel packages leading to results and inferences below:

|          **variable** | **coef** | **std err** |  **z** | **P>[z]** | **0.025** | **0.975** |
| --------------------: | -------: | ----------: | -----: | --------: | --------: | --------: |
|          metropolitan |  -0.5459 |       0.082 | -6.656 |         0 |    -0.707 |    -0.385 |
|     adultskills_score |  -0.4896 |       0.118 | -4.132 |         0 |    -0.722 |    -0.257 |
|               2017_q3 |   1.8683 |       0.652 |  2.864 |     0.004 |      0.59 |     3.147 |
|     residential_ratio |   3.4951 |       1.231 |  2.839 |     0.005 |     1.082 |     5.908 |
|          indoor_score |  -0.1509 |       0.054 | -2.779 |     0.005 |    -0.257 |    -0.044 |
|        elec_d_con_mdn |   1.4876 |       0.551 |  2.699 |     0.007 |     0.407 |     2.568 |
|             rail_work |  -0.6978 |       0.259 | -2.699 |     0.007 |    -1.204 |    -0.191 |
|      cardriver_empbus |   1.0182 |       0.378 |  2.696 |     0.007 |     0.278 |     1.758 |
|         rail_shopping |   0.7446 |       0.274 |  2.719 |     0.007 |     0.208 |     1.281 |
| residential_mdn_ratio |  -2.4575 |       1.012 | -2.429 |     0.015 |     -4.44 |    -0.475 |
|           elec_nd_con |  11.9535 |       4.962 |  2.409 |     0.016 |     2.227 |     21.68 |
|         geo_bar_score |   0.1562 |       0.068 |    2.3 |     0.021 |     0.023 |     0.289 |
|      buscoach_holiday |   0.5403 |       0.238 |  2.274 |     0.023 |     0.075 |     1.006 |
|               2015_q2 |  -0.7837 |       0.352 | -2.228 |     0.026 |    -1.473 |    -0.094 |
|       elec_d_con_mean |  -0.6476 |       0.302 | -2.143 |     0.032 |     -1.24 |    -0.055 |
|               2019_q1 |   1.5625 |       0.744 |  2.099 |     0.036 |     0.103 |     3.022 |
|         cycle_holiday |  -0.6321 |       0.321 | -1.968 |     0.049 |    -1.262 |    -0.003 |

![](/reports/figures/analysis/statsmodel_coefficient.jpg)

The probability of an EV charge point being located in an area:

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



### The Code

[Click here for the Python Code](/notebooks/4.0-ced-analysis.ipynb)

### Navigator

<table>
    <th align='left'>Previous</th>
    <th align='right'>Next</th>
    <tr>
    	<td align='left'><a href="modelling.md"><< Modelling</a></td>
    	<td align='right'><a href="README.md#predicting-electric-vehicle-charging-station-locations-in-britain">Summary >></a></td>
    </tr>
</table>

[Back to Beginning](https://github.com/cdenbowjr/ev_chargepoint_prediction#predicting-electric-vehicle-charge-points-locations-in-britain)