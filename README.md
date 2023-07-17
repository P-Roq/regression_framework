# Project: A Linear Regression Framework Based On Modular Programming
  

## Details

1. The overall purpose of the application:

    - This application pre-configures a linear regression workflow which aims at streamlining several statistical analysis processes, from exploratory data analysis up to predictive quality comparison between estimated models. To achieve this, a control script is set with a pre-defined number of hyperparameters that instructs the program to produce a customized and comprehensive statistical analysis report that can be exported into a PDF document. The main goal of the application is to allow the user to pick any data set and conduct a quick, scalable and customizable analysis that permits to easily visualize, modify and compare data, integrate support machine learning algorithms for feature selection and data randomization, produce multiple regressions and comprehensive batteries of error hypothesis testing, without having to always write the base code from the ground up, while resorting to a simplified, user friendly, set of commands. 


2. How the application can be used to address specific needs or objectives:

    - A problem arises when a researcher wants to try several approaches to the various stages of the analysis before it settles into a final configuration that wishes to interpret and explain -- e.g. changing the variables to be analyzed; determining how many experimental regressions to perform; omit or ignore one or more sections of the analysis, but has no way simple way to quickly produce or reproduce a modified version of the current analysis. This program allows the researcher to perform several exploratory and statistical tasks, by ony changing or omitting control arguments in a single dedicated control script without having to constantly change the core structure of the framework. The framework includes machine learning algorithms that allow for enhancement and automatization of certain aspects of the analysis, such has features selection and model validation techniques.
      

3. The main features and functions of the application:

    - Produce a full or partial linear regression analysis workflow in a Jupyter Notebook.
        - Choose what sections (stages or sub-sections of the analysis) to be performed.
        - Store multiple reports by either storing the control script or by exporting the report into a PDF document.

    - It allows to change a number of arguments at several stages of the data pipeline that modify aspects of:
        - Exploratory data analysis / data visualization.
        - Data processing, transformation and splitting.
        - Regression analysis and sub-component analysis.

    - The control script is a module identified by the initial expression 'ctrl', e.g. 'ctrl_template.py'.  


4. The target audience the application is designed for:

    - The app is targeted to students/researchers/practitioners within the econometrics, data analysis, data science fields. 


5. The value the application provides to users:

    - By having a pre-configured data workflow, researchers can spend more time efficiently exploring a set of essential tools in data analysis and linear regression methodology, without having to constantly re-writing necessary code. 


6. Any potential benefits or advantages to using the application:

    - The benefits of this program are directly related with the use of a modular approach to the structure/framework of the analysis. Some of the benefits:
        - volume of code to be written decreases substantially
        - multiple libraries loaded without the need to specify them or to explicitly use their specific classes, functions, methods, etc
        - the ctrl script uses simplified syntax that is easier to use for users not familiarized with programming languages, instead of using   
        - code reuse:
            - extend sections of the analysis, e.g. multiple regressions
            - make multiple analysis of the same data set
            - use any data set
        - better code organization
            - easier feature implementation 
        - easier troubleshooting
        - time efficiency


7. The cost associated with using the application:

    - The major disadvantage of this app is the loss of flexibility:
        - It follows a pre-configured workflow which doesn't allow to perform an analysis or statistical tests beyond what has been built-in. (although, like aforementioned in point 6, it is easier to add new features to the program due to its organization)
    
        - Similarly, functions may have a reduced scope, e.g. in regards to the Feature Selection section, only 4 of the 11 algorithms available in the Scikit-learn library are evoked by the app.  

        - Less flexibility to customize graphs, e.g. axis scales, bin sizes (histograms), colors, etc. since these are pre-configured as well.   

        - The work flow of the analysis follows a pre-determined order. 

    - The implementation of new app features such as new statistical tests or machine learning support algorithms is more complex than the traditional approach.  



8. The usability and user experience design of the application:

    - The use of the app is supposed to be simple as the user only has to change values in a pre-configured control script and run the program via Jupyter notebook.


10. The ongoing support and maintenance services available for the application

    - There just a few customized error/warning messages built-in, but for most cases, if the control script is not well set (e.g. missing dictionary key, sub-section of the analysis activated when the parent section is deactivated, etc.), errors may arise and the user must be able to at least be able detect if there is some error in the set-up of the control script, or if there is some incompatibility between the data set, or any other error that may transpire. 


## To-do list:

    - Add more customizable features to the histogram panel.

    - Raise a customized error message every time a regression is trying to be fitted with a non-numeric variable. 

    - Implement the option of standardization of data.

    - Include white test in the residual analysis and allow for the durbin-watson as an optional test (although there is no time series for this particular data set, feature for the generalized version). 

    - Introduce leverage/influence points calculation, e.g. cooks's distance.
    
    - Include a mode estimation and MSE/RMSE test set analysis.

    - Allow for a more complex randomization of data sets in order to allow for a k-fold cross validation process, as well as bootstrap randomization.

    - Consider removing the 'print results' functions into their own module instead of having a bloated 'modelling' script.

    - Also, consider moving some of the calculus made in `reg_results` (modeling.py) to statistical_testing.py if it makes sense.

    - Implementation of test(s) and mechanisms to deal with structural breaks in the data.

    - Allow for other types of regression techniques to be estimated besides the standard OLS: Weighted, OLS, Ridge, LASSO. (requires allowing to change the estimator used in the Feature Selection stage.)

    - Include an option to print a regression script based on the arguments chosen. The idea that, in the case the framework does not have the functionalities the user requires in his/hers analysis, he/she can export a closer version as a script and modify/include the functionality without having to write the analysis from the ground up, outside the framework/program. 

    - [Best Practice] Remove encoding from code variables' names.
    - [Best Practice] Replace comments by function and class documentation and complete missing documentation.


## Improvements / implementations (first to last):

    - Fist version of 'parameters.py'/`ctrl.py` module implementation finished 

    - Created 'statistical_tests.py' to simplify the tasks in 'modelling.py'

    - Added two scatter plot functions to data_visualization.py - `resid_visual_analysis_1` and `resid_visual_analysis_2`, which belong exclusively to the residual analysis section.

    - Re-organized the residual analysis section so that the output is either related to train or to the test set, depending on the hyperparameter `residuals_set`.

    - Included the 'Compare Error Quality' section to the analysis workflow which summarizes the MSE/RMSE values of the stored regressions.

    - VIF analysis included to the workflow: turned it into a class so that multiple versions of the analysis can be performed and printed. 

    - Inclusion of the sections 1 and 2 of variable description in the exploratory data analysis of the workflow.

    - Inclusion of a 'query dataframe' section, activated by the hyperparameter `query_df`; this serves two purposes: i. allows to continue the analysis replacing the current dataframe by a queried version (queried versions can be produced and stored by instantiating the class `Filtered_DF` by setting the `queries_container` and `queried_df` hyperparameters.) ii. It allows to visually explore the relation of any explanatory variable with the target variable via scatter plot.

    - Inclusion of a box plot panel in the 'visualize' section.

    - Inclusion of a printed summary in the beginning of the Regression section, of the regressions to be performed.

    - Extended `split_data()` in order to produce not only a train and a test set but also a validation set. The validation set 'supervises' the train set while the test set serves to evaluate the quality of the model.

    - Combined `x_var_container` and the `target_container` ('ctrl_template.py') into a dictionary 
    
    - `model_dict_container`, to avoid mistakes in pairing the features and target variable for regression purposes.

    - Inclusion of missing values printing for each column, and an inclusion of a hyperparameter `remove_na` that removes all missing values from the main data frame, when activated. It resets the index.

    - Inclusion of a 'data viewer' that allows the user to display slices of the data frame in two moments of the analysis: before data transformation and after. The associated hyperparameters that allow to choose which columns and row slice to be printed are `df_coordinates_1` and `df_coordinates_1`. If the hyperparameters are not detected or are omitted, the viewer displays all the columns and the first 10 rows. This replaces the previous section of the analysis that printed by default only the first 5 rows of the data frame, both before and after. 

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

    - Inclusion of a Pearson correlation dataframe that is activated in the control scrip by `correlations`. This is an alternative to the correlation heat map, if the user by some reason, e.g. too many variables to include in the graphic, prefers the traditional display. 

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

    - `modelling.py` renamed to `linear_regression`, to accommodate the future inclusion of other types of regression.

    - Creation of a data set CSV exporter, to take advantage of the modifications and exploration made in the original data set.

    - Along with the past trend, both the exporting of the data set and the PDF  report are activated by creating/uncommenting the variables `dataset_name` and `pdf_name`, respectively, instead of relying on booleans 'activators' (`export_dataset` and `store_pdf`/`export_pdf`).   

    - Addition of a trimmer class that allows the user to: trim the main data frame resorting to either, specific values, z-scores or IQR thresholds; and store the results for further inspection or to replace the main data frame. To replace the main data frame by a trimmed version we set `replace_for_trimmed` with an integer identical to the index of the dictionary in `trimmer_container` from which the resultant data frame was derived from.

    - In the 'Error Measurement Comparison', now the comparison is made between models with the same target. If there are more than two targets, a data frame is build for each group of models that share the same target.

    - Inclusion of a program feature that allows to visually compare the main data frame with one of the alternative data frames create via trimmer or query. The visual comparison can be set for the histogram, box plot, and scatter plot panels (read NOTES.md). 

## Current task

    - Add more customizable features to the histogram panel.