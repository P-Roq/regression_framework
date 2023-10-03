main_folder_name = 'regression_framework'
data_file_name = 'insurance.csv'

# Control Section: choose which sections to run.
identify_origin_script = True
lower_case_columns = True
print_columns = False
data_description_1 = True
check_na = False
remove_na = False 
print_proportions = True
data_description_2 = True
summary_after_transformation = True
drop_non_numeric = True
correlations = False
plug_feature_selection = True
make_regression = True
residuals_analysis = True
residuals_set = 'train' #
error_comparison = True

# Choose to store output.
# dataset_name = 'transformed_dataset_1'
# pdf_name = 'new_version'

#------------------------------------------------------------------------

initial_features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
target_container = ['charges', 'log_charges']

# View data.
data_view_1 = {'rows': [0, 5], 'columns': initial_features,}
data_view_2 =  {}



### Data transformation.

# replace_values = [
#     {'variable': , 'value': None, 'transform': 'standard_deviation', 'ddof': 2},
#     ]

# Binary to dummy, 3 keys: `variable`, `invert`, `drop_current`. 
convert_binary_to_dummy = [
    {'variable': 'sex', 'invert': False, 'drop_current': True},
    {'variable': 'smoker', 'invert': False, 'drop_current': True},
    ]

# All keys: ('variable', 'add_suffix', 'drop_dummy', 'dummies_names', 'drop_current')
# convert_nonbinary_to_dummies = [
#     {'variable': 'region', 'drop_dummy': 1, 'drop_current': True},
#     ]

# Convert variables into their logs, 2 keys: `variable`, `drop_current`.
convert_to_log = [
    {'variable': 'charges', 'drop_current': False},
    ] 

# Convert to Categorical type, 2 keys: `variable`, `drop_current`.
convert_to_categorical = [
    {'variable': 'region', 'drop_current': True},
]

#### Split data.

split_data = {
    'rand_state': [5, 5],
    'proportions': (0.6, 0.2,), 
    'shuffle': False,
    }

# standardize_data = {'transform': 'z_score',  'include_binary': ['smoker_d'], 'round': 2} #'include_binary': True,   


#### Data trimming

# trimmer_container = [
#     {'variable': 'bmi', 'boundaries': 'upper', 'value': 45, 'scaling_factor': None, 'z_score': None, 'ddof': None},
#     {'variable': 'charges', 'boundaries': 'upper', 'value': None, 'scaling_factor': None, 'z_score': None, 'ddof': None},
#     ]

#### Data frame queries

# Create variants of the main data frame for further analysis.
query_container = [
    {'df': 'all', 'query': 'smoker_d == 0'},
    {'df': 'all', 'query': 'bmi > 30 & smoker_d == 1'},
    {'df': 'all', 'query': 'bmi > 30 & smoker_d == 1 & sex_d == 1'},
    ]

# query_container = [
#     {'df': 'all', 'query': 'smoker_d == 1'},
#     {'df': 'all', 'query': 'bmi > 30 & smoker_d == 1'},
#     {'df': 'all', 'query': 'bmi > 30 & smoker_d == 1 & sex_d == 1'},
#     ]

# Scatter plot: visually observe the relation between two variables in different 
# data frame variants produced by the values in `queries`. 
# df_variants_for_scatterplot = [0, 1, 2,]

# queries_scatter_variables = {'x': 'age', 'y': 'charges'}

# scatterplot = {'df': 'main', 'container': 'query', 'index': 'all', 'x': 'age', 'y': 'charges'}


# replace_for_trimmed = 3
# replace_for_queried = 0  # change the main data frame for a queried version


#### Visualization panels.

display_panels = {
    'df': ('train', 'train'),
    'container': (None, 'query'), 
    'index': (None, 1),
    'panel': ('scatterplot', 'histogram', 'boxplot'),
    }


histograms = {
    'features': ['age', 'sex_d', 'bmi', 'children', 'smoker_d', 'region_cat', 'charges'],
    'bins': {'age': 5,},
	'density': {'charges': True,},
	'cumulative': {'bmi': True,}
    }

boxplots = ['age', 'bmi', 'children', 'charges']

scatterplots = {
    'target': 'charges',
    'features': ['age', 'sex_d', 'bmi', 'children', 'smoker_d', 'region_cat'],
    'title': None
    } # 'Scatter Plots: Features Vs Target'


heat_map = {
    'df': 'train',
    'variables': ['age', 'sex_d', 'bmi', 'children', 'smoker_d', 'region_cat', 'charges']
    }



#### Regressions preprocessing.

#### VIF analysis.

x_var_container_vif = [
    ['age', 'sex_d'],
    ['age', 'sex_d', 'bmi'],
    ['age', 'sex_d', 'smoker_d'],
    ['age', 'sex_d', 'bmi', 'children', 'smoker_d'],
    ]

## Feature selection.

# # If this list is empty, all the features in the main data set will be included. 
# initial_features_fs = ['age', 'bmi', 'sex_d', 'children', 'smoker_d',]

# 3 keys: `target`, `k_vars` and `criterion`.
univariate_container = [
    {'target': 'charges', 'k_vars': 4, 'criterion': 'f_regression'},
    {'target': 'log_charges', 'k_vars': 4, 'criterion': 'f_regression'},
    ]

# 3 keys: `target`, `k_vars` and `step`.
recursive_elimination_container = [
    {'target': 'charges', 'k_vars': 4, 'step': 1},
    {'target': 'charges', 'k_vars': 4, 'step': 0.5},
    {'target': 'log_charges', 'k_vars': 4, 'step': 1},
    {'target': 'log_charges', 'k_vars': 4, 'step': 0.5},
    ]

# 4 keys: `target`, `k_vars`, `direction` and `tolerance`.
sequential_container = [
        {'target': 'charges', 'k_vars': 4, 'direction': 'forward', 'tolerance': 0.05},
        {'target': 'charges', 'k_vars': 4, 'direction': 'backward', 'tolerance': None},
        {'target': 'log_charges', 'k_vars': 4, 'direction': 'forward', 'tolerance': 0.05},
        {'target': 'log_charges', 'k_vars': 4, 'direction': 'backward', 'tolerance': None},
    ]

# 3 keys: `target`, `k_vars` and `threshold`.
# importance_weights_container = [
#     {'target': 'charges', 'k_vars': 1, 'threshold': '1.5*mean'},
#     ]


## Regression analysis.

# RunRegression hyperparameters.
manual_model_container = [
    {'target': 'charges', 'x_vars': ['age', 'sex_d',],},
    {'target': 'charges', 'x_vars': ['age', 'sex_d', 'bmi',],},
    {'target': 'charges', 'x_vars': ['age', 'sex_d', 'smoker_d',],},
    {'target': 'charges', 'x_vars': ['age', 'sex_d', 'bmi', 'children', 'smoker_d',],},
    ]
