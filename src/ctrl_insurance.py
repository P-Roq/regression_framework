main_folder_name = 'regression_framework'
data_file_name = 'insurance.csv'

# Control Section: choose which sections to run.
identify_origin_script = True
print_columns = False
data_description_1 = True
check_na = False
remove_na = False # remove all missing values
data_description_2 = True
drop_non_numeric = True
correlations = True
plug_feature_selection = False
make_regression = False
residuals_analysis = False
residuals_set = 'train' # 'train' or 'validation'
error_comparison = False

# Choose to store output.
# dataset_name = 'transformed_dataset_1'
# pdf_name = 'new_version'

#------------------------------------------------------------------------

initial_features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
target_container = ['charges', 'log_charges']

# View data.
# df_coordinates_1 = {'rows': [0, 5], 'columns': initial_features}
# df_coordinates_2 = {'rows': [0, 5], 'columns': None}


### Data transformation.

# replace_na_values = [
#     ]

# Binary to dummy, 3 keys: `variable`, `invert`, `drop_current`. 
convert_binary_to_dummy = [
    {'variable': 'sex', 'invert': False, 'drop_current': True},
    {'variable': 'smoker', 'invert': False, 'drop_current': True},
    ]

# convert_nonbinary_to_dummies = [
#     {'variable': 'region', 'add_suffix': None, 'drop_dummy': 1, 'dummies_names': None, 'drop_current': True},
#     ]

# Convert variables into their logs, 2 keys: `variable`, `drop_current`.
convert_to_log = [
    {'variable': 'charges', 'drop_current': False},
    ] 

# Convert to Categorical type, 2 keys: `variable`, `drop_current`.
convert_to_categorical = [
    {'variable': 'region', 'drop_current': True},
]


#### Data trimming

# trimmer_container = [
#     {'variable': 'bmi', 'boundaries': 'upper', 'value': 45, 'scaling_factor': None, 'z_score': None, 'ddof': None},
#     {'variable': 'charges', 'boundaries': 'upper', 'value': None, 'scaling_factor': None, 'z_score': None, 'ddof': None},
#     ]

trimmer_container = [
    {'variable': 'bmi', 'boundaries': 'upper', 'value': 45},
    {'variable': 'charges', 'boundaries': 'both', 'z_score': (-1, 1)},
    ]


#### Data frame queries

# Create variants of the main data frame for further analysis.
queries_container = [
    'smoker_d == 0',
    'bmi > 30 & smoker_d == 1',
    'bmi > 30 & smoker_d == 1 & sex_d == 1',
    ]

# Scatter plot: visually observe the relation between two variables in different 
# data frame variants produced by the values in `queries`. 
df_variants_for_scatterplot = [0, 1, 2,]

queries_scatter_variables = {'x': 'age', 'y': 'charges'}

# replace_for_trimmed = 0
# replace_for_queried = 0  # change the main data frame for a queried version


#### Visualization panels.

# Allowed values in compare_visually['panel']: 'hist', 'box', 'scatter'. 
compare_visually = {
    'container': 'queries_container',
    'index': 0,
    'panel': ['hist', 'box', 'scatter']
    }


hist_cols = ['age', 'sex_d', 'bmi', 'children', 'smoker_d', 'region_cat', 'charges']
boxplot_cols = ['age', 'bmi', 'children', 'charges']
scatter_dict = {
    'target': 'charges',
    'features': ['age', 'sex_d', 'bmi', 'children', 'smoker_d', 'region_cat'],
    'title': None
    } # 'Scatter Plots: Features Vs Target'
# heatmap_cols = ['age', 'sex_d', 'bmi', 'children', 'smoker_d', 'region_cat', 'charges']


#### Trim values


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
# initial_features_fs = ['age', 'bmi', 'sex_d', 'children', 'smoker_d',]

# 3 keys: `target`, `k_vars` and `criterion`.
univariate_container = [
    {'target': 'charges', 'k_vars': 4, 'criterion': 'f_regression'},
    {'target': 'log_charges', 'k_vars': 4, 'criterion': 'f_regression'},
    ]

# 3 keys: `target`, `k_vars` and `step`.
# recursive_elimination_container = [
#     {'target': 'charges', 'k_vars': 4, 'step': 1},
#     {'target': 'charges', 'k_vars': 4, 'step': 0.5},
#     {'target': 'log_charges', 'k_vars': 4, 'step': 1},
#     {'target': 'log_charges', 'k_vars': 4, 'step': 0.5},
#     ]

# 4 keys: `target`, `k_vars`, `direction` and `tolerance`.
# sequential_container = [
#         {'target': 'charges', 'k_vars': 4, 'direction': 'forward', 'tolerance': 0.05},
#         {'target': 'charges', 'k_vars': 4, 'direction': 'backward', 'tolerance': None},
#         {'target': 'log_charges', 'k_vars': 4, 'direction': 'forward', 'tolerance': 0.05},
#         {'target': 'log_charges', 'k_vars': 4, 'direction': 'backward', 'tolerance': None},
#     ]

# 3 keys: `target`, `k_vars` and `threshold`.
# importance_weights_container = [
#     {'target': 'charges', 'k_vars': 1, 'threshold': '1.5*mean'},
#     ]


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
    {'target': 'charges', 'x_vars': ['age', 'sex_d', 'bmi']},
    {'target': 'charges', 'x_vars': ['age', 'sex_d', 'smoker_d']},
    {'target': 'charges', 'x_vars': ['age', 'sex_d', 'bmi', 'children', 'smoker_d']},
    ]
