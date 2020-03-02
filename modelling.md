# Modelling & Evaluation

| Model                | Training | Testing | Cross_Val | Tuned Cross_Val |
| -------------------- | -------- | ------- | --------- | --------------- |
| Logistic Regression  | 0.733    | 0.725   | 0.714     | 0.718           |
| Linear SVM           | 0.734    | 0.720   | 0.715     | 0.717           |
| Random Forest        | 0.929    | 0.709   | 0.713     | 0.715           |
| Decision Tree        | 0.682    | 0.685   | 0.675     | 0.687           |
| Gaussian Naive Bayes | 0.686    | 0.692   | 0.686     | 0.686           |
| K Nearest Neighbours | 0.781    | 0.684   | 0.670     | 0.682           |
| Radial Based SVM     |          |         |           |                 |
| Neural Network       | 0.803    | 0.717   | 0.671     |                 |
| Ada Boost Ensemble   | 0.748    | 0.706   | 0.711     |                 |



<table>
    <col width="65%">
  	<col width="35%">
    <tr>
        <td rowspan="2"><img src="./reports/figures/modelling/logistic_regression_confusion_matrix_altered.jpg"></td>
        <td><img src="./reports/figures/modelling/logistic_regression_roc_curves.jpg" width="75%"></td>
    </tr>
    <tr>
        <td><img src="./reports/figures/modelling/logistic_regression_pr_curves.jpg" width="75%"></td>
    </tr>
</table>









### The Code

[Click here for the Python Code](/notebooks/3.0-ced-modelling.ipynb)

### Navigator

<table>
    <th align='left'>Previous</th>
    <th align='right'>Next</th>
    <tr>
    	<td align='left'><a href="eda2.md#eda"><< Exploratory Data Analysis II</a></td>
    	<td align='right'><a href="analysis.md#eda">Analysis >></a></td>
    </tr>
</table>

