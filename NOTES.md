# Notes on the mechanisms of the program

## Setting up the 'control' script

To be identified and used by the program, the control script should be placed in the 'control_scripts' folder and the name of the file must start with the expression 'ctrl', e.g. 'ctrl_script_1.py'. If more than one control script is present the program uses the first to appear in the alphabetic order. 


## View Data

 The associated hyperparameters that allow to choose which columns and row slice to be printed are `data_view_1` and `data_view_2`. If the hyperparameters are not detected or omitted, the viewer displays all the columns and the first 10 rows. `data_view_1` displays always data from the main data set (data before splitting) while `data_view_2` shows data related to the train set by default (or main if no data splitting tool place), but it can be changed to either the main, validation or tests sets by setting 'df' accordingly.


## Replace any Value or non-available / missing values (NaN)

To replace values or missing values for either a specific value or a proxy value of choice. `replace_values` takes an undetermined number of replacements (as of now this happens for the main data frame), each one represented by a dictionary with the following parameters:
    - `variable`: chose the variable/column where to apply the change.

    - `replace`: the specific value to be replaced, or the string 'missing_values' to replace NaN values.

    - `value`: the value to replace the original value.

    - `transform`: replace a value by summary statistic provided one of the following strings: 'minimum', 'maximum', 'mode', 'median', 'variance', 'standard_deviation'.

        - A custom string form to replace missing values by quantiles other than the median. To do that the user sets the parameter `transform` to `quantile=[float, str]`, where the numeric value must be within the [0, 1] range; e.g. selecting the 3rd quartile: `quantile=0.75`.

    - `ddof`: delta degrees of freedoms can be set for variance and standard deviation calculations. If omitted while 'variance' or 'standard_deviation' has been set in `transform` its default value is 0.  

If some of the values passe in 'replace' are could not be found on the original series, a warning line is printed in the output. If a type of transformation is used beyond the options specified earlier raises an exception.   

## Rolling / moving windows

    - `transform` can take one of the following values: 'mean', 'sum', 'minimum', 'maximum', 'variance' or 'standard_deviation'.

    - `one_ahead` (`False` by default) is a boolean that, when activated, moves the value derived from the window to the next value. E.g. if `one_ahead=True` for a 5 period rolling window that calculates the mean for a regular array with an index 0-19, the first value will appear at the index value 5, whilst it would start at index 4 (5 periods: 0, 1, 2, 3, 4 indexes) by default.    


## Split Data

Split data into train, validation and test sets or just train and validation test sets. The splitting is done after the data processing and before the visualization section to allow the user the possibility to query, trim and visualize the initial data frame or one of its resultant versions from the splitting process; as well as to decide whether it wants to conduct the VIF analysis and Feature Selection with one of those data frames.

- `rand_state`:
    - Integer:
        - The same value will be used for the two random states used 
        to split the data (train from 'rest' and 'rest' into 'validation' and 'test').
    - Iterable (list or tuple) - if two values are passed:  
        - They must be integers.
        - The first value in the iterable regards the first split (train from 'rest') and the second value regards the second split ('validation' and 'test').

- `proportions`:
    - Iterable (list or tuple) - if two values are passed:
        - if the sum is inferior to 1 then the first value is the train size, the second is the validation size and the omitted (1 - (train size + validation size)) is the test size.
        - if the values add up to 1, then the test size is 0 (the test set is empty).
        - if the iterable only has one value it is assumed that its the train size that has been passed, thus the validation size is given by 1 - train size, and the test set is empty.
    -  Float - if a float is passed instead one of the iterables allowed it behaves in the same way as an iterable which only contains one value (that defines the train size).

- `shuffle` accepts 4 values:
    - `True` (default) - shuffles once when the train set is split from the subset that will be subsequently split into a validation and test sets.
    - `1` - also shuffles once.
    - `2` - shuffles twice; the second time is when the validation and the test sets are split.
    - `False`: No shuffle takes place.


## Standardize or Re-scale Data   

To prevent data leakage, this process is done to every data set available after splitting: main (un-split), train, validation and test sets. 

Note: as of now, when the main data set has been split into subsets the same standardization is applied to the main and all its all sub sets. 

Activated by the dictionary `standardize_data` (control script):
    - `vars` can be used to specify the variables to be modified. If omitted, the change is applied to all numeric variables. 

    - `transform` allows to choose from three options: 
        - `'min_max'` (default when `transform is omitted`)
        - `'max_absolute'`
        - `'z_score'` 

    - `include_binary`can be used to specify whether to modify binary variables or to keep them unmodified. 

    - `round` can be used to choose the number of n-digits precision after the decimal point to apply in the modified arrays.

- When `vars` is not specified:
    - if `include_binary=True`, all variables should be standardized, including binary variables but excluding non-numeric variables.

    - if `include_binary=False` or is omitted (`None`) only numeric non-binary variables are standardized.

    - if `include_binary` is a list with variables that are identifies as binary the function standardizes numeric non-binary and the specified binary variables.


- When `vars` is specified:
    - and `include_binary` is False or omitted, only non-binary variable contained in `vars` will be standardized.
    - if `include_binary=True` all numeric variables in `vars` are standardized.
    - if `include_binary` is a list of strings an exception is raised that adverts that if `vars` specifies the variables to standardized - non-binary and binary alike, then there is no reason to specify them in another list.  


## Trim Data

The user can create several versions of the data frame by trimming the data by different methods. For that, a class has been created - `Trim_Data`, that has a function - `trim_data()`; the `trim_container` stores the dictionaries with the trimming specifications as well as the parameter that specifies which subsets to apply the trimming; this parameter - 'df', can take the following values:
    - `'main'`, `'train'`, `'validation'`, `'test'` to trim an individual data set; If the data is split, this parameter accepts a list or a tuple with that allows to choose more than one of the available data sets, e.g. `['validation', 'test']`.   
    - `'all'` and `None`, tries to apply the trimming to all sets available (if there was no split only the main data frame is trimmed).
    - if omitted, `'df'` replicates the `'all'` behavior. 

To replace the data frame(s) to be further transformed/analyzed by a trimmed version(s) we set `replace_for_trimmed` with an integer identical to the index of the dictionary in `trim_container` from which the resultant data frame was derived from.

The function `trim_data()` allows the user to trim the data frame using 3 different methods that are defined by the parameter(s) used:
    - `value` sets fixed thresholds values.
    - `iqr` sets inter-quartile range (IQR) thresholds via scaling factors (absolute values).
    - `z_score` sets z_scores has thresholds. The variable chosen is converted into a Series of z-scores which will be used to trim the data frame. After that the latter Series is dropped. The additional parameter `ddof` can be used to choose the delta degrees of freedom when calculating the standard deviation for the z-scores.

    The function identifies which thresholds to use/calculate when only one of the past parameters is in use (to the exception of `'ddof'` that can only be set along `z-score`), while the others are set to None. If more than one is not None, an exception is raised.

    - `value`, `iqr` and `z_score` can be a single value, integer or float, to set a single threshold, or a tuple with a lower and upper thresholds, in this order. 

    - To chose a single or both thresholds, the user sets `boundaries` to either:
        - `'lower'`
        - `'upper'`
        - or `'both'`

    If a single boundary is chosen but a tuple is set as an argument, e.g.  `boundaries=upper` and `iqr=(1.5, 2)`. Then the function fetches the second value `2` to defined the upper threshold and ignores the other value. An analogous behavior happens `boundaries=lower`.  



## Data Queries

Storing and using queried data frames versions work similarly to the trimming data process:
    - `query_container`, which is located in the control script, is a list that stores dictionaries that contain queries in the form of strings, that will be processed in the class `Filter_Data`, as to queried data frames via the `filter_data()`, function. The user specifies which set of data subsets to query via the `df` parameter. This task has two purposes:

        - Visualize the relation between two variable, e.g. target and a feature, via scatter plot, while differentiating the markers' color by data frame variant. We can select which data frame variants to observe by filling out `df_variants_for_scatterplot` with index values associated with `query_container` (the values in `query_container` have the same index as the container that stores the data frame variants).The former container is a subset of the latter, i.e. `df_variants_for_scatterplot` only takes values contained in `query_container`. `queries_scatter_variables` is the dictionary that contains which variables to plot.

To replace the unqueried data set(s) by queried version(s) the user specifies the index of the desired query version stored in `query_container ` into `replace_for_queried`. 


## Summary statistics after processing and splitting

`data_description_2` now accepts a boolean or one of the following strings: 'main', 'train', 'validation' or 'test'.

If the main data set hasn't been split only `True` and `'main'` can be passed, and they both return the summary statistics for the main data set.

If the main data set has been split, `True` returns the summary statistics for the train data set by default.

In both cases, setting to `False` returns nothing (empty string).


## Scatter plot - comparison of modified versions 

This feature allows to create a variable scatter plot that that takes allows to visually compare different modified versions of the same data set, produced via the trim or query features. 

Parameters:
    - `df`: str, None
        - One of the sets: 'main', 'train', 'validation', 'test'.  
        - If omitted or None is passed, `df: train.`
    - `container`: str
        - One of the containers - 'trim' or 'query', given that the associated container - `trim_container` or `query_container` have been activated.
    - `index`: list[int], None
        - Given a container, which modified versions to choose from, e.g. if `query_container` has 5 dictionaries that produce 5 that modify the specified data set in 5 different ways. If the user wants to compare the 1st and the 4th versions the index will be `[0, 3]`. 
        - If `'all'` is passed, all the versions in the container will be fitted in the scatter plot. 
        - The `'all'` behavior is replicated if `None` or `index` is omitted.
    - `x`: 
        - The variable / column for the X axis of the plot.
    - `y`: 
        - The variable / column for the Y axis of the plot.



## Data Visualization  

To display the graph panels the user first sets up the `display_panels` with the data sets to be used and then the information regarding each panel via the following elements:
    - `histograms`
    - `boxplots`
    - `scatterplots`
<<<<<<< HEAD
    - `heatmap`

=======
>>>>>>> 7402ac569e30b289c905d997dc56e6cc28e8ab9f

    - `df`: tuple[str, str], list[str, str]
        - 
    - `container`: `'trim'`, `'query'`, `None`
        - The  
    - `index`: str
        - if containers were set with either `'trim'` or `'query'`, the index of identifies which data set version to fetch within the chosen container.  
    - `panel`: str, list[str], tuple[str]: 
        - the comparison can be made for any of the following three types of graph, co-currently or not: `'histogram'`, `'boxplot'` and `'scatterplot'` panels.  


## Histogram Panel

`histogram` is the dictionary used to set the histogram panel parameters. It always requires the item 'features', which provides the list of variables from which to build the histograms. Three other optional items can added to affect specified variables/histograms or all of them:
    - 'bins': to change the number of bins for a particular variable include them into a dictionary; the default value is 10 bins, e.g.:
        `histogram = {
            'features': ['var_a', 'var_b', 'var_c'],
            'bins': {'var_a': 8, 'var_b': 5}
            }`

    To set a custom number of bins for every axis use insert a string instead of a dictionary, e.g.:
        `histogram = {
            'features': ['var_a', 'var_b', 'var_c'],
            'bins': 20
            }`

    - 'density': bins represents a probability density instead of absolute values for a specific variable(s), e.g.:
        `histogram = {
            'features': ['var_a', 'var_b', 'var_c'],
            'density': {'var_a': True}
            }`
    
     or all variables, e.g.:
        `histogram = {
            'features': ['var_a', 'var_b', 'var_c'],
            'density': True
            }`

    - 'cumulative': each bin represents the sum of the current bin count plus the previous bin counts; can be switched to a probability density representation if 'density' is activated; if a negative number is placed instead of `True` the direction of accumulation is reversed, e.g.:
        `histogram = {
            'features': ['var_a', 'var_b', 'var_c'],
            'density': {'var_a': True, 'var_c': -1}
            }`
    
     or all variables, e.g.:
        `histogram = {
            'features': ['var_a', 'var_b', 'var_c'],
            'density': True
            }`


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

    - https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html#matplotlib.axes.Axes.hist

    - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html#sklearn.feature_selection.SelectKBest

    - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html#sklearn.feature_selection.RFE

    - https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html#sklearn.feature_selection.SequentialFeatureSelector

    -https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectFromModel.html#sklearn.feature_selection.SelectFromModel