# Control script path.
main_folder_name = 'regression_framework'
data_file_name = 'boston_housing.csv'

# Control Section: choose which sections to run.
identify_origin_script = True
lower_case_columns = False
print_columns = False
data_description_1 = True
check_na = True
remove_na = True # remove all missing values
print_proportions = True
data_description_2 = False
drop_non_numeric = False
correlations = False
plug_feature_selection = False
make_regression = False
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
df_coordinates_1 = {'rows': [0, 15],}
df_coordinates_2 = {'df': 'validation', 'rows': [0, 10], 'columns': None}

### Data transformation.

# replace_values = [
#     {'variable': 'RAD', 'replace': [1, 12, 14], 'value': 'replaced',},
#     {'variable': 'LSTAT', 'replace': 'missing_values', 'transform': 'quantile=0.75', 'ddof': None,},
#     {'variable': 'NOX', 'replace': 'missing_values', 'transform': 'mean',},
#     {'variable': 'AGE', 'replace': 189, 'value': 'replaced',},
# ]

# rolling_window = [
#     {'variable': 'RM', 'rows': 5, 'drop_current': True},
#     {'variable': 'NOX', 'rows': 3, 'transform': 'standard_deviation', 'ddof': 2},
#     {'variable': 'CRIM', 'rows': 3, 'transform': 'mean', 'replace_na_values': True, 'one_ahead': True},
# ]


# percentage_change = [
#     {'variable': 'RM', 'rows': 5, 'replace_na': True},
#     {'variable': 'NOX', 'replace_na': 4, 'differences_only': True},
# ]


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


#### Split data.

split_data = {
    'rand_state': 5,
    'proportions': (0.6, 0.2,), 
    'shuffle': True,
    }

# standardize_data = {'std_type': 'z_score',  'include_binary': ['smoker_d'], 'round': 2} #'include_binary': True,   


#### Data trimming

trimmer_container = []


#### Data frame queries

# Create variants of the main data frame for further analysis.
# queries_container = [
#     ]

# Scatter plot: visually observe the relation between two variables in different 
# data frame variants produced by the values in `queries`. 
# df_variants_for_scatterplot = [
#     ]

# scatterplot = {'df': 'train', 'container': 'trim', 'index': [],'x': '', 'y': ''}

# replace_for_trimmed = 0
# replace_for_queried = 0  


#### Visualization panels.

# Allowed values in compare_visually['panel']: 'hist', 'box', 'scatter'. 
# compare_visually = {
#     'container': 'queries_container',
#     'index': 0,
#     'panel': ['hist', 'box', 'scatter']
#     }


# hist_params = {
#     'features': [],
#     'bins': {'': 5,},
# 	  'density': {'': True,},
# 	  'cumulative': {'': True,}
#     }

# boxplot_cols = ['age', 'bmi', 'children', 'charges']

# scatterplots = {
#     'target': '',
#     'features': [],
#     'title': None
#     } # 'Scatter Plots: Features Vs Target'

# heatmap_cols = []


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


## Regression analysis.

# RunRegression hyperparameters.
manual_model_container = [
    {'target': 'charges', 'x_vars': ['age', 'sex_d']},
    ]
