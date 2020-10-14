Code and data accompanying "Worst-Case Analysis for Randomly Collected Data" appearing at NeurIPS 2020.

To reproduce the experiments from the paper, run the jupyter notebooks snowball.ipynb, selective_prediction.ipynb, and importance_sampling.ipynb.
The experiments were run on a 2018 MacBook Pro.

Dependencies:
    python3
    jupyter
    numpy
    cvxpy
    mosek
    matplotlib
    scikit-learn


Code:

rcwc.py
-This file contains the methods for the main algorithm (corresponding to Algorithm 1 in the paper) and for evaluation.

snowball.ipynb
-Notebook for generating instances of the snowball sampling described in the paper.
-Rerun with different assignments to the variable "k" in order to compute results with different sample sizes.

selective_prediction.ipynb
-Notebook for generating instances of the selective prediction setting.

importance_sampling.ipynb
-Notebook for generating instances of the importance sampling setting.


Data:

In the "data" folder, we have saved the key outputs of the experiments, e.g. the weights of the semilinear estimator given by Algorithm 1.

For the snowball sampling data, there is a separate subfolder for each value of "k" (sample size).
Within each folder are the matrices A, b, and a_rcwc with the rows of these matrices referring to the variables A_i, b_i, and a_i, respectively.

For the selective prediction data, there is a separate file containing the weights for each value of "k" (here, referring to k = lg n).
The rows of these weight files refers to the variables a_i in Algorithm 1.

For the importance sampling data, the semilinear weights for RCWC are in the file a_rcwc.


Results:

(1) SNOWBALL SAMPLING:
(a) Expected Squared Error on Spatially Correlated Values
+---------------+---------------+---------------+
|Size of Sample |Sample Mean    |Our Algorithm  |
+---------------+---------------+---------------+
|10             |0.153          |0.035          |
|15             |0.115          |0.037          |
|20             |0.097          |0.036          |
|25             |0.082          |0.032          |
|30             |0.063          |0.024          |
|35             |0.038          |0.013          |
|40             |0.017          |0.006          |
+---------------+---------------+---------------+

(b) Expected Squared Error on Worst-Case Values
+---------------+---------------+---------------+
|Size of Sample |Sample Mean    |Our Algorithm  |
+---------------+---------------+---------------+
|10             |1.602          |0.329          |
|15             |1.079          |0.234          |
|20             |0.882          |0.181          |
|25             |0.690          |0.135          |
|30             |0.459          |0.080          |
|35             |0.253          |0.034          |
|40             |0.102          |0.014          |
+---------------+---------------+---------------+

(2) SELECTIVE PREDICTION (Expected Squared Error on Worst-Case Values)
+---------------+---------------------+---------------+
|n              |Selective Prediction |Our Algorithm  |
+---------------+---------------------+---------------+
|4              |2.667                |1.000          |
|8              |1.924                |0.844          |
|16             |1.488                |0.696          |
|32             |1.208                |0.583          |
|64             |1.015                |0.435          |
+---------------+---------------------+---------------+

(3) IMPORTANCE SAMPLING (Expected Squared Error by Type of Data)
+-----------------------+--------+------------------------+-----------------------+-----------+
|Method                 |Trivial |Intergroup Variance     |Intragroup Variance    |Worst-Case |
+-----------------------+--------+------------------------+-----------------------+-----------+
|Sample Mean            |0.000   |0.486                   |0.042                  |0.486      |
|Inv. Prop. Reweighting |0.100   |0.100                   |0.100                  |0.101      |
|Subgroup Estimation    |0.018   |0.018                   |0.121                  |0.122      |
|Our Algorithm          |0.051   |0.053                   |0.052                  |0.053      |
+-----------------------+--------+------------------------+-----------------------+-----------+
