# Control script path.
main_folder_name = 'regression_framework'
data_file_name = 'boston_housing.csv'

# Control Section: choose which sections to run.
identify_origin_script = True
print_columns = False
data_description_1 = True
check_na = True
remove_na = False # remove all missing values
data_description_2 = False
drop_non_numeric = True
correlations = True
plug_feature_selection = True
make_regression = True
residuals_analysis = False
residuals_set = 'train' # 'train' or 'validation'
error_comparison = False

# Choose to store output.
# dataset_name = 'transformed_dataset_1'
# pdf_name = 'new_version'

#------------------------------------------------------------------------

initial_features = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV'] 
target_container = ['MEDV']

# View data.
# df_coordinates_1 = {'rows': [0, 10], 'columns': initial_features}
# df_coordinates_2 = {'rows': [0, 10], 'columns': None}

### Data transformation.

replace_na_values = [
    {'variable': 'CRIM', 'value': None, 'other': 'standard_deviation', 'ddof': 2},
    {'variable': 'ZN', 'value': None, 'other': 'median', 'ddof': None},
    {'variable': 'INDUS', 'value': None, 'other': 'median', 'ddof': None},
    {'variable': 'CHAS', 'value': None, 'other': 'median', 'ddof': None},
    {'variable': 'AGE', 'value': None, 'other': 'median', 'ddof': None},
    {'variable': 'LSTAT', 'value': None, 'other': 'median', 'ddof': None},
]

# Binary to dummy, 3 keys: 'variable', 'invert', 'drop_current'. 
# convert_binary_to_dummy = [
#     {'variable': 'sex', 'invert': False, 'drop_current': True},
#     {'variable': 'smoker', 'invert': False, 'drop_current': True},
#     ]

# convert_nonbinary_to_dummies = [
#     {'variable': 'region', 'add_suffix': None, 'drop_dummy': 1, 'dummies_names': None, 'drop_current': True},
#     ]

# Convert variables into their logs, 2 keys: 'variable', 'drop_current'.
# convert_to_log = [
#     {'variable': 'CRIM', 'drop_current': False}
#     ] 

# Convert to Categorical type, 2 keys: 'variable', 'drop_current'.
# convert_to_categorical = [
#     {'variable': 'region', 'drop_current': True},
# ]


# Create variants of the main data frame for further analysis.
# queries = [
#     ]

# Scatter plot: visually observe the relation between two variables in different 
# data frame variants produced by the values in `queries`. 
# df_variants_for_scatterplot = [
#     ]

# queries_scatter_variables = {'x': 'age', 'y': 'charges'}

# main_df = queries[0]  # change the main data frame for a queried version


#### Visualization.

# hist_cols = initial_features
# boxplot_cols = initial_features
heatmap_cols = initial_features 
# scatter_dict = {
#     'target': target_container[0],
#     'features': initial_features,
#     'title': 'Scatter Plots: Features Vs Target'
#     }


#### VIF analysis.

# x_var_container_vif = [
#     ['age', 'sex_d'],
#     ['age', 'sex_d', 'bmi'],
#     ['age', 'sex_d', 'smoker_d'],
#     ['age', 'sex_d', 'bmi', 'children', 'smoker_d'],
#     ]


#### Regressions preprocessing.

## Feature selection.

# If this list is empty, all the features in the main data set will be included. 
initial_features_fs = ['age', 'bmi', 'sex_d', 'children', 'smoker_d',]

# 3 keys: 'target', 'k_vars' and 'criterion'.
univariate_container = [
    {'target': 'charges', 'k_vars': 4, 'criterion': 'f_regression'},
    {'target': 'log_charges', 'k_vars': 4, 'criterion': 'f_regression'},
    ]

# 3 keys: 'target', 'k_vars' and 'step'.
recursive_elimination_container = [
    {'target': 'charges', 'k_vars': 4, 'step': 1},
    {'target': 'charges', 'k_vars': 4, 'step': 0.5},
    {'target': 'log_charges', 'k_vars': 4, 'step': 1},
    {'target': 'log_charges', 'k_vars': 4, 'step': 0.5},
    ]

# 4 keys: 'target', 'k_vars', 'direction' and 'tolerance'.
sequential_container = [
        {'target': 'charges', 'k_vars': 4, 'direction': 'forward', 'tolerance': 0.05},
        {'target': 'charges', 'k_vars': 4, 'direction': 'backward', 'tolerance': None},
        {'target': 'log_charges', 'k_vars': 4, 'direction': 'forward', 'tolerance': 0.05},
        {'target': 'log_charges', 'k_vars': 4, 'direction': 'backward', 'tolerance': None},
    ]

# 3 keys: 'target', 'k_vars' and 'threshold'.
importance_weights_container = [
    {'target': 'charges', 'k_vars': 1, 'threshold': '1.5*mean'},
    ]


#### Split data.

split_data_dict = {
    'rand_state': 5,
    'validation_size': 0.2, 
    'test_size': 0.2,
    'shuffle': True,
    }


## Regression analysis.
# RunRegression hyperparameters.
manual_model_container = [
    {'target': 'charges', 'x_vars': ['age', 'sex_d']},
    ]
