# Notes on the mechanisms of the program

## Setting up the 'control' script

The app will try to identify a script with that expression and load the module (if more than one script, the one loaded is the first to be extracted using the `glob` function). The ideal workflow is to copy-paste one script from the folder 'quick_setups' into the 'src' file; as mentioned, the script should start with the expression 'parameter' and preferably, there should be only one script of that type located in 'src'. 


## Trim data frames

The user can create several versions of the data frame by trimming the data by different methods. For that, a class has been created - `Trim_DF`, that has a function - `insert_trimmed_df()`, for trimming and storing the resultant data frames into the attribute `trimmed`.

The function `insert_trimmed_df()` allows the user to trim the data frame using 3 different methods that are defined by the parameter(s) used:
    - `value` sets fixed thresholds values.
    - `iqr` sets inter-quartile range (IQR) thresholds via scaling factors ( absolute values).
    - `z_score` sets z_scores has thresholds. The variable chosen is converted into a Series of z-scores which will be used to trim the data frame. After that the latter Series is dropped. The additional parameter `ddof` can be used to choose the delta degrees of freedom when calculating the standard deviation for the z-scores.

    The function identifies which thresholds to use/calculate when only one of the past parameters is in use (to the exception of `ddof` that can only be set along `z-score`), while the others are set to None. If more than one is not None, an exception is raised.

    - `value`, `iqr` and `z_score` can be a single value, integer or float, to set a single threshold, or a tuple with a lower and upper thresholds, in this order. 

    - To chose a single or both thresholds, the user sets `boundaries` to either:
        - `lower`
        - `upper`
        - or `both`

    If a single boundary is chosen but a tuple is set as an argument, e.g.  `boundaries=upper` and `iqr=(1.5, 2)`. Then the function fetches the second value `2` to defined the upper threshold and ignores the other value. An analogous behavior happens `boundaries=lower`.  

    To replace the main data frame by a trimmed version we set `replace_for_trimmed` with an integer identical to the index of the dictionary in `trimmer_container` from which the resultant data frame was derived from.


## Data frame queries

How this section works:
    - `queries_container`, which is located in the control script, is a list that stores queries in the form of strings, that will be processed in the class `Filtered_DF`, as to store the data frames that result from the querying. These task has two purposes:

        - Visualize the relation between two variable, e.g. target and a feature, via scatterplot, while differentiating the markers' color by data frame variant. We can select which data frame variants to observe by filling out `df_variants_for_scatterplot` with index values associated with `queries_container` (the values in `queries_container` have the same index as the container that stores the data frame variants).The former container is a subset of the latter, i.e. `df_variants_for_scatterplot` only takes values contained in `queries_container`. `queries_scatter_variables` is the dictionary that contains which variables to plot.

        - From the resulting data frame variants we can replace the main data frame that we'll be using to conduct the rest of the analysis by a resulting variant. We point to the desired data frame by choosing the correspondent query of origin stored in `query`.


## Visually Compare data frames 

To visually compare graphs on the main and alternative data frames the user can fill out the dictionary `compare_visually`, with the following keys:
    - 'container': alternative data frames can be produced via either trimming or querying, thus this key takes either 'queries_container' or 'trimmer_container' as valid values.
    - 'index': points to the index of the previous container, which fetches the resultant data frame.
    - 'panel': the comparison can be made for any of the following three graphs, co-currently or not, in the histogram, box plot and scatter plot panels.  


## Feature selection

An option that allows to include a semi-automated feature selection process into the analysis workflow. In this version all the algorithms use a standard OlS estimator. There are 4 different types of algorithms to choose from:

    - Univariate 
    - Recursive elimination
    - Sequential/step-wise 
    - Importance weights

The selection processes allowed in the analysis are reduced versions of the classes in Scikit-learn. They were meant to allow for a more functional and fast approach to the feature selection implementation, yet, with the cost of less flexibility and depth. 


When setting the initial features to start the selection process the user can fill the `initial_features_fs` list. If omitted, the program replaces this list by a list of features - `all_features`, which are all the variables available except those in the `target_container`. If there are variables specified in `initial_features_fs` which are not included in `all_features`, an exception error is raised.

The feature selection process is activated when the program detects at least one of the containers, which store the dictionaries containing the input parameters necessary to conduct the feature selection process(es). For each type of selection algorithm there is a container that stores as many dictionaries/processes as desired:

    - `univariate_container`
    - `recursive_elimination_container`
    - `sequential_container`
    - `importance_weights_container` 

Dictionaries have specific parameters according to the type of container/algorithm they belong to:

- Univariate:
    - target: str, 
    - k_vars: int,
    - criterion: callable (str)

- Recursive elimination:
    - target: str, 
    - k_vars: int,
    - step: str, float

- Sequential/step-wise:
    - target: str, 
    - k_vars: int,
    - direction: 'forward' or 'backward' (str),
    - tolerance: float

- Importance weights:
    - target: str, 
    - k_vars: int,
    - threshold: str, float


After the all the whole process has ran, the program prints:
    - For each specified selection process within each container:
        - Container index
        - Parameters (the dictionary used to define the selection process)
        - Features selected via the selection process

    - A summary of the unique combinations of features selected irrespectively of the type of algorithm specified, but discriminating between models with different target variables.

    - Finally, in the next stage of the analysis - Regression Results, the unique combinations found earlier with the selection processes will be estimated once again in order to be further analyzed. In the 'Summary' it is automatically specified which selection strategies originated each specific feature combination. A specific combination may be derived from more than one selection process. For this process to take place it is necessary to activate the `plug_feature_selection` parameter in the set-up script.


References:
    - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html#sklearn.feature_selection.SelectKBest

    - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html#sklearn.feature_selection.RFE

    - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html#sklearn.feature_selection.SequentialFeatureSelector

    -https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFromModel.html#sklearn.feature_selection.SelectFromModel