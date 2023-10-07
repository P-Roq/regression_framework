## To-do list:

    - [Software design] debloat 'main.py' so that the data wrangling/processing and the regression sections can work has decoupled blocks, allowing an easy implementation of future blocks.  
    
    - Incorporate `residuals_set` in `residuals_analysis`.

    - Include a model estimation and MSE/RMSE test set analysis.

    - Update VIF analysis stage so that includes a feature that includes all explanatory variables while excluding secondary targets. 

    - In the error comparison stage, allow or include the R-squared as a measure of model quality.

    - Raise a customized error message every time a regression is trying to be fitted with a non-numeric variable. 

    - Include white test in the residual analysis and allow for the durbin-watson as an optional test (although there is no time series for this particular data set, feature for the generalized version). 

    - Introduce leverage/influence points calculation, e.g. cooks's distance.

    - Include the possibility to generate polynomial and interaction features.

    - Include a data loader feature that reads data from local a local SQLite database. 

    - Allow for a more complex randomization of data sets in order to allow for a k-fold cross validation process, as well as bootstrap randomization.

    - Consider removing the 'print results' functions into their own module instead of having a bloated 'modelling' script.

    - Also, consider moving some of the calculus made in `reg_results` (modeling.py) to statistical_testing.py if it makes sense.

    - Implementation of test(s) and mechanisms to deal with structural breaks in the data.

    - Allow for other types of regression techniques to be estimated besides the standard OLS: Weighted, OLS, Ridge, LASSO. (requires allowing to change the estimator used in the Feature Selection stage.)

    - Include an option to print a regression script based on the arguments chosen. The idea that, in the case the framework does not have the functionalities the user requires in his/hers analysis, he/she can export a closer version as a script and modify/include the functionality without having to write the analysis from the ground up, outside the framework/program. 

    - Inclusion of PCA as part of the feature selection stage. 

    - Consider adding a secondary control file for a deeper customization of some aspects of data visualization.
  
    - [Software design] build classes for all the functions that use the elements in the control script as input, in order to create support functions to check and raise custom error messages if the values inserted do not belong to the types accept. [Use pydantic as an alternative?] 

    - [Best Practice] Revise control hyperparameter names.
    - [Best Practice] Start all functions' names with verbs, e.g. `do_something()`.
    - [Best Practice] Remove encoding from code variables' names.
    - [Best Practice] Replace comments by function and class documentation and complete missing documentation.


## Improvements / implementations (first to last):

    - Fist version of 'parameters.py'/`ctrl.py` module implementation finished 

    - Created 'statistical_tests.py' to simplify the tasks in 'modelling.py'/'linear_regression.py'

    - Added two scatter plot functions to data_visualization.py - `resid_visual_analysis_1` and `resid_visual_analysis_2`, which belong exclusively to the residual analysis section.

    - Re-organized the residual analysis section so that the output is either related to train or to the test set, depending on the hyperparameter `residuals_set`.

    - Included the 'Compare Error Quality' section to the analysis workflow which summarizes the MSE/RMSE values of the stored regressions.

    - VIF analysis included to the workflow: turned it into a class so that multiple versions of the analysis can be performed and printed. 

    - Inclusion of the sections 1 and 2 of variable description in the exploratory data analysis of the workflow.

    - Inclusion of a 'query dataframe' section, activated by the hyperparameter `query_df`; this serves two purposes: i. allows to continue the analysis replacing the current dataframe by a queried version (queried versions can be produced and stored by instantiating the class `Filtered_DF` by setting the `queries_container` and `queried_df` hyperparameters.) ii. It allows to visually explore the relation of any explanatory variable with the target variable via scatter plot.

    - Inclusion of a box plot panel in the 'visualize' section.

    - Inclusion of a printed summary in the beginning of the Regression section, of the regressions to be performed.

    - Extended `split_data()` in order to produce not only a train and a test set but also a validation set. The validation set 'supervises' the train set while the test set serves to evaluate the quality of the model.

    - Combined `x_var_container` and the `target_container` ('ctrl_template.py') into a dictionary.
    
    - `model_dict_container`, to avoid mistakes in pairing the features and target variable for regression purposes.

    - Inclusion of missing values printing for each column, and an inclusion of a hyperparameter `remove_na` that removes all missing values from the main data frame, when activated. It resets the index.

    - Inclusion of a 'data viewer' that allows the user to display slices of the data frame in two moments of the analysis: before data transformation and after. This replaces the previous section of the analysis that printed by default only the first 5 rows of the data frame, both before and after. 

    - Inclusion of a small section in `main.py` between the query visual analysis and the VIF analysis, that identifies the variables in the main data frame that are not in numeric form. The idea is to give the user the opportunity to check if some variables cannot be fitted into a regression since they were't properly transformed. In addition, the hyperparameter `drop_non_numeric` has been added to the control section of the control script; when activated, removes non-numeric variables from the data frame.

    - Changed `DataPathClass` from `main.py` to its own file - `paths.py`. Now the users sets two parameters regarding paths in the control script:
        - `main_folder_name`
        - `data_file_name`
    This way, if there are more than one 'csv' in the `data` folder, the user can easily read the file without having to change the path in other files besides the control script. 
    Similarly, if the user wants to change name of the main folder of create a new project and set the correct paths, it only needs to set `main_folder_name` with the name of the main project folder. 

    - Data processing section completely reformulated, four functions perform the following tasks of transforming and/or replacing variables within the data frame:
        - binary variables into dummies
        - non-binary/constant variables into dummies
        - log variables
        - convert (from object type) variables into categorical  
    To transform any pre-existing variable the user fills a dictionary with the required parameters to be inserted in the respective functions in `main.py`.
    These tasks do not require a boolean activator in the Control Section, instead they are activated if detected. To skip these tasks the user simply removes or omits (by commenting) the associated hyperparameter containers. 

    - Reformulated the removal/replacement of missing values into three parts da can be changed in the control script:
        - Activate `check_na` to count missing values per column.
        - Activate `remove_na` to remove all missing values.
        - Fill a container with dictionaries that pass a number of relevant arguments into the `replace_na` function. If the container is omitted from the script, the program skips the replacement process.   

    Values valid for the `other` argument: 'minimum', 'maximum', 'mode', 'median', 'mean', 'variance', 'standard_deviation'.
        
    Operations allowed per Series/column type (`other` argument):
        - numeric (int, float, complex): min, max, mode, mean, var, std
        - bool: min, max, mode, mean, var, std
        - datetime: min, max, mode, mean 
        - categorical: min, max, mode
        - object: min, max, mode
        - pd.Interval: min, max, mode

    - Improvement in the 'visualization' section: now each of the panels can be individually skipped from the analysis by omitting the associated hyperparameter in the control script.

    - Inclusion of a Pearson correlation data frame that is activated in the control scrip by `correlations`. This is an alternative to the correlation heat map, if the user by some reason, e.g. too many variables to include in the graphic, prefers the traditional display. 

    - Changed the way some sections of the analysis are suppressed, instead of having an boolean 'activator', the processes are suppressed by omission (commenting/uncommenting or deleting). 'Activators' removed:
        - `visualize`
        - `vif_analysis`
        - `feature_selection`
        - `plug_feature_selection`
        - `univariate_selector`
        - `recursive_elimination_selector`
        - `sequential_selector`
        - `importance_weights`
        - `select_model_manually`
        - `query_df`
        - `change_df`
        - `scatter_query_df`
        - `export_dataset` 
        - `store_pdf` / `export_pdf`
    
    - Reformulation of the data frame querying and scatter plot visualization of queried data frames: removed activators, replaced `feat_to_query` and `target_to_query` for `queries_scatter_variables`; renamed to `queries_scatter` to `df_variants_for_scatterplot`; renamed `queried_df` to `replace_for_queried` (full explanation of this section in NOTES.md). The new order of the process is:
        - `queries_container`
        - `df_variants_for_scatterplot`
        - `queries_scatter_variables`
        - `replace_for_queried`

    - Raise exception when `initial_features_fs` (former `initial_x_vars_fs`) contains variables that are not considered explanatory variables (read NOTES.md).

    - Separate `statistical_tests.py` into two more modules, to avoid having a single generic module with objects with different natures. After the reformulation, `statistical_tests.py` only contains hypothesis tests, where, `statistical_analysis` contain other kinds of analysis besides hypothesis tests; `check_data.py` stores objects that relay information on data that is being processed. 

    - `modelling.py` renamed to `linear_regression.py`, to accommodate the future inclusion of other types of regression.

    - Creation of a data set CSV exporter, to take advantage of the modifications and exploration made in the original data set.

    - Along with the past trend, both the exporting of the data set and the PDF  report are activated by creating/uncommenting the variables `dataset_name` and `pdf_name`, respectively, instead of relying on booleans 'activators' (`export_dataset` and `store_pdf`/`export_pdf`).   

    - Addition of a trimmer class that allows the user to: trim the main data frame resorting to either, specific values, z-scores or IQR thresholds; and store the results for further inspection or to replace the main data frame. To replace the main data frame by a trimmed version we set `replace_for_trimmed` with an integer identical to the index of the dictionary in `trimmer_container` from which the resultant data frame was derived from.

    - In the 'Error Measurement Comparison', now the comparison is made between models with the same target. If there are more than two targets, a data frame is build for each group of models that share the same target.

    - Inclusion of a program feature that allows to visually compare the main data frame with one of the alternative data frames create via trimmer or query. The visual comparison can be set for the histogram, box plot, and scatter plot panels (read NOTES.md). 

    - inclusion of boolean `lower_case_columns` in the control section to allow lowercase the data frame columns. 

    - Inclusion of 3 other customizable elements to the histogram panel. `hist_cols` in the control script is replaced by a dictionary, `hist_params`, which allow for 3 optional feature changes that can be applied to either all or specified variables (for more information read NOTES.md):
        - 'bins'
        - 'density'
        - 'cumulative'
    
    - Inclusion of program feature that allows to estimate a default model when `make_regression` is activated but there are no feature selection or manually selected variable containers in the control script. The program tries to define the explanatory variables by excluding the variables in the `target_container` and chooses the first variable (name) in this container as the target; if `target_container` does not exist an exception is raised.

    - **[major change]** data split section moved from right before the main regression analysis to after data processing and before data standardization / re-scaling, with the goal of preventing data leakage: the standardization/re-scaling techniques are applied to each data sub set after split. Slitting the main data set at an earlier stage means that every other transformation, e.g. data trimming, querying, must be applied individually to all data subsets, thus a series of comprehensive modifications must be applied account fo this change. Many of the next implementations will reflect this change.
    
    - Inclusion of an option to standardize all data sets after splitting.   

    - Inclusion of a printable table that summarizes the number of rows and associated proportions in relation to the main data frame by activating `print_proportions` in the control script.

    - Inclusion of a `utils` module in `src` to store support functions for refactoring and other similar purposes.

    - Inclusion of a function in `utils.py` - `unfold_dictionary`, that allows the user to omit parameters in the dictionaries passed in the control script, that are replaced by 'unfolded' versions which replace the each omitted parameter by None, so that these items can be passed into the respective functions. 

    - `data_description_2` (after splitting and pre-processing) now allows to choose to display the summary statistics for the main, train, validation or test sets.

    - [Best Practice] evaluate and replace when possible bitwise operators - '&' and '|' for 'and' and 'or', respectively. 

    - Re-factoring and changing the trim section to accommodate the selection of data subs sets after split.
    
    - Re-factoring and changing the query section to accommodate the selection of data subs sets after split.
    
    - Re-factoring and changing the data view 2 section to accommodate the selection of data subs sets after split.
    
    - Change in summary statistics after transformation from a fixed print to an optional print in the control section of the script with the option to specify the data subset.   

    - Single scatter plot comparison reformulation to accommodate split data sets.

    - Reformulation of the visualization section: histograms, box plots, scatter plots and correlation heat map are now controlled by the hyperparameters in the dictionary `display_panels`: these hyperparameters allow to visually compare data sets by sub set - 'main', 'train', 'validation', 'test', and by transformation - trim or query. 

    - 'Checking Non-numerical Variables' has been revised to accommodate split data sets.

    - The Pearson correlation table given by the control parameter `correlations` has been revised to accommodate split data sets.

    - The Pearson correlation heat map has been revised to accommodate split data sets.


## Current task

- The trimmer function may have to be updated to accommodate the fact that the data may already be standardized (z-scores).

- Allow VIF and Feature selection to be made with train by default but changeable to main or the other subsets.




