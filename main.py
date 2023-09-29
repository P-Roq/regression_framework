import subprocess, re, importlib, glob

from src import utils as ut
from src import data_loader as dl
from src import data_viewer as viewer
from src import data_transformation as dt
from src import data_splitting as ds
from src import data_visualization as dv
from src import linear_regression as lr
from src import statistical_tests as st
from src import feature_selection as fs
from src import data_checks as dc
from src import statistical_analysis as sa

import pandas as pd
import numpy as np

# Manual change of script for development purposes.
def change_ctrl_script(a_string: str):
    if a_string == 'insurance':
        return 0
    if a_string == 'boston':
        return 1

change = change_ctrl_script('insurance')


# Detect and import the quick set-up script. 
files_names = glob.glob(f'control_scripts/ctrl*.py')
extract_name = re.findall('./(\w+)', files_names[change])[0]
c = importlib.import_module(f'control_scripts.{extract_name}') # 'c' for 'control'

class DataPath:
    DATASET_PATH = f"../{c.main_folder_name}/exported_csv"
    SOURCE_DATA_PATH = f"../{c.main_folder_name}/data/{c.data_file_name}"
    PDF_PATH = f"../{c.main_folder_name}/exported_pdf"
    NOTEBOOK_PATH = f"../{c.main_folder_name}/output.ipynb"

def main() -> None:
    if c.identify_origin_script:
        print(f'Control script: {extract_name}.py\n\n')

    main = dl.read_data(DataPath.SOURCE_DATA_PATH)

    if c.lower_case_columns:
        main = dl.lower_case_cols(main)

    # Converting the data frame int a 2D array to compare with the version after transformations.
    main_initial = main.values 

    print('#### Initial Variables:\n') 
    summary_stats_1 = main.info()
    print('\n')

    if c.print_columns:
        print('\nAll Columns:')
        print('\n', list(main.columns), '\n')

    print('\nData Viewer 1:\n')     
    if hasattr(c, 'data_view_1'):
        full_dic = ut.unfold_dictionary(c.data_view_1, viewer.View_Data.keys)

        viewer.View_Data.view_data(
            df=main,
            rows=full_dic['rows'],
            columns=full_dic['columns'],
        )
    else:
        viewer.View_Data.view_data(main, None, None)
    print('\n\n')

    if c.data_description_1:
        print('Variable Description Before Data Processing:\n')
        print(main.describe(), '\n\n')

    #### Data processing.

    if c.check_na:
        print('Missing Values (NAs) Per Column:')
        na_values = main.isna().sum()
        print(f'\n{na_values}\n\n')

    if hasattr(c, 'replace_values'):
        messages = []
        for dic in c.replace_values:
            full_dic = ut.unfold_dictionary(dic, dt.Replace_Values.keys)
            main, message = dt.Replace_Values.replace_values(
                variable=full_dic['variable'],
                df=main,
                replace=full_dic['replace'],
                value=full_dic['value'],
                transform=full_dic['transform'],
                ddof=full_dic['ddof'],
                )
            if message:
                messages.append(message)
        if messages:
            print('Value replacement report:')
            print(*messages, sep='\n')
            print('\n') 


    if c.remove_na:
        main = main.dropna().reset_index(drop=True)

    if c.check_na or c.remove_na:
        print('Missing values (NAs) After Replacement/Removal:')
        na_values = main.isna().sum()
        print(f'\n{na_values}\n\n')


    if hasattr(c, 'convert_binary_to_dummy'):
        for dic in c.convert_binary_to_dummy:
            main = dt.binary_to_dummy(
                dic['variable'],
                main,
                dic['invert'],
                dic['drop_current']
                )

    if hasattr(c, 'convert_nonbinary_to_dummies'):
        for dic in c.convert_nonbinary_to_dummies:
            full_dic = ut.unfold_dictionary(dic, dt.Nonbinary_To_Dummies.keys)
            main = dt.Nonbinary_To_Dummies.nonbinary_to_dummies(
                full_dic['variable'],
                main,
                full_dic['drop_dummy'],
                full_dic['add_suffix'],
                full_dic['dummies_names'],
                full_dic['drop_current'],
                )

    if hasattr(c, 'convert_to_log'):
        for dic in c.convert_to_log:
            main = dt.log_variable(
                dic['variable'],
                main,
                dic['drop_current']
                )

    if hasattr(c, 'convert_to_categorical'):
        for dic in c.convert_to_categorical:
            main = dt.categorize_variable(
                dic['variable'],
                main,
                dic['drop_current']
                )
            
    if hasattr(c, 'rolling_window'):
        for dic in c.rolling_window:
            full_dic = ut.unfold_dictionary(
                dic, dt.Rolling_Window.keys
                )
            main = dt.Rolling_Window.rolling_window(
                var=full_dic['variable'],
                df=main,
                rows=full_dic['rows'],
                transform=full_dic['transform'],
                one_ahead=full_dic['one_ahead'],
                replace_na=full_dic['replace_na'],
                ddof=full_dic['ddof'],
                drop_current=full_dic['drop_current'],
                )

    # CHANGES SPLIT RELATED START BELOW
    
    if hasattr(c, 'split_data'):
        split = True

        train, validation, test = ds.split_data(
            main,
            c.split_data['rand_state'],
            c.split_data['proportions'],
            shuffle=c.split_data['shuffle'],
            )  
    
        data_sets = {
            'main': main,
            'train': train,
            'validation': validation,
            'test': test,
            }
    else:
        split = False
        # When there isn't a split we use the 'train' key to reference the main data frame.
        data_sets = {'train': main,}
    
    data_sets_names = list(data_sets.keys())

    all_sets_names = ['main', 'train', 'validation', 'test']

    all_data_sets = {
        'processed': data_sets,
        'trim': None,
        'query': None,
    }

    if hasattr(c, 'print_proportions'):
        print('\nData Sets Proportions\n')
        print(ds.print_proportions(data_sets))
        print('\n')

    if hasattr(c, 'standardize_data'):
        standardize_parameters = ut.unfold_dictionary(c.standardize_data, dt.Standardize.keys)
        for key in data_sets:
            data_sets[key] = dt.Standardize.standardize(
                df=data_sets[key],
                vars=standardize_parameters['vars'],
                transform=standardize_parameters['transform'],
                include_binary=standardize_parameters['include_binary'],
                round=standardize_parameters['round'],
            )


    #### TRIMMING
    if hasattr(c, 'trim_container'):
        
        trimmer = dt.Trim_Data()

        # We store for each element in `c.trim_container` the data set(s) trimmed versions.
        trimmed_storage = {i: {} for i in range(len(c.trim_container))}

        i = 0
        for dic in c.trim_container:
            full_dic = ut.unfold_dictionary(dic, dt.Trim_Data.keys)

            to_trim = None

            if (full_dic['df'] is None) or (full_dic['df'] == 'all'):
                to_trim = data_sets_names
            elif (isinstance(full_dic['df'], str)) and (full_dic['df'] in all_sets_names):
                to_trim = [full_dic['df']]
            elif (isinstance(full_dic['df'], (list, tuple))) and (set(full_dic['df']) < set(all_sets_names)):
                to_trim = full_dic['df']
            else:
                raise Exception("Could not find a valid expression for 'df'.")
            
            for df in to_trim:
                trimmed = trimmer.trim_data(
                    df=data_sets[df],
                    variable=full_dic['variable'],
                    boundaries=full_dic['boundaries'],
                    value=full_dic['value'],
                    scaling_factor=full_dic['scaling_factor'],
                    z_score=full_dic['z_score'],
                    ddof=full_dic['ddof'],
                )

                trimmed_storage[i][df] = trimmed

            i += 1    

        # If an element in `c.trim_container` only trims a specific data set, `trimmed_storage` will
        # fill for that element the associated dictionary with references to the untrimmed versions of
        # remaining data sets. E.g if `c.trim_container = [{'df': ['train', 'validation'], '...': '...'}]`, then
        #  `trimmed_storage = {0: {'main': not_trimmed, 'train': trimmed, 'validation': trimmed, 'test': not_trimmed}}`.
        if split:
            for key in trimmed_storage:
                for df in all_sets_names:
                    if df not in trimmed_storage[key].keys():
                        trimmed_storage[key][df] = data_sets[df]

        all_data_sets['trim'] = trimmed_storage                        
        
        if hasattr(c, 'replace_for_trimmed'):
            data_sets = trimmed_storage[c.replace_for_trimmed]
    #---------------------------------------------------------------------

    #### QUERYING (analogous process to trimming)
    if hasattr(c, 'query_container'):
        filter = dt.Filter_Data()

        queried_storage = {i: {} for i in range(len(c.query_container))}

        i = 0
        for dic in c.query_container:
            full_dic = ut.unfold_dictionary(dic, dt.Filter_Data.keys)

            to_query = None

            if (full_dic['df'] is None) or (full_dic['df'] == 'all'):
                to_query = data_sets_names
            elif (isinstance(full_dic['df'], str)) and (full_dic['df'] in all_sets_names):
                to_query = [full_dic['df']]
            elif (isinstance(full_dic['df'], (list, tuple))) and (set(full_dic['df']) < set(all_sets_names)):
                to_query = full_dic['df']
            else:
                raise Exception("Could not find a valid expression for 'df'.")
            
            for df in to_query:
                queried = filter.filter_data(
                    df=data_sets[df],
                    query=full_dic['query'],
                    )
                
                queried_storage[i][df] = queried

            i += 1    

        if split:
            for key in queried_storage:
                for df in all_sets_names:
                    if df not in queried_storage[key].keys():
                        queried_storage[key][df] = data_sets[df]

        all_data_sets['query'] = queried_storage                        

        if hasattr(c, 'replace_for_queried'):
            data_sets = queried_storage[c.replace_for_queried] 
    #---------------------------------------------------------------------

    if hasattr(c, 'summary_after_transformation'):
        if split:
            if not isinstance(c.summary_after_transformation, bool) and\
            (c.summary_after_transformation not in data_sets_names):
                raise Exception(f'`summary_after_transformation` must be either a boolean or a value in {data_sets_names}.')
                                            
            if c.summary_after_transformation is True:
                set_name = 'train'
                print(f'#### Variables After Transformation ({set_name}):\n')
                summary_stats_2 = data_sets['train'].info()

            if c.summary_after_transformation in data_sets_names:
                set_name = c.summary_after_transformation
                print(f'#### Variables After Transformation ({set_name}):\n')
                summary_stats_2 = data_sets[c.summary_after_transformation].info()

        if split is False:
            if not isinstance(c.summary_after_transformation, bool) and\
            (c.summary_after_transformation not in ['main', 'train']):
                raise Exception(f"`summary_after_transformation` must be either a boolean or a value in {['main', 'train']} (there was no data split).")
            
            if (c.summary_after_transformation is True) or (c.summary_after_transformation in ['main', 'train']):
                set_name = 'main'
                print(f'#### Variables After Transformation ({set_name}):\n')
                summary_stats_2 = data_sets['train'].info()

    if hasattr(c, 'data_view_2'):
        full_dic = ut.unfold_dictionary(c.data_view_2, viewer.View_Data.keys)
        if full_dic['df'] is None:
            full_dic['df'] = 'train'
            set_name = 'train'
        if not split:        
            if full_dic['df'] in ['validation', 'test']:
                raise Exception(f"The main data frame hasn't been split, therefore, the {full_dic['df']} subset cannot be selected.")
            if (full_dic['df'] == 'main') or (full_dic['df'] == 'train'):
                full_dic['df'] = 'train'
                set_name = 'main'


        print(f"\n\nData Viewer 2 ({set_name} set):\n")     

        viewer.View_Data.view_data(
            df=data_sets[full_dic['df']],
            rows=full_dic['rows'],
            columns=full_dic['columns'],
        )
    else:    
        if not split:      
            set_name = 'main' 
        else:
            set_name = 'train'

        print(f"\n\nData Viewer 2 ({set_name} set):\n")
        viewer.View_Data.view_data(data_sets['train'], None, None)
    print('\n')

    if hasattr(c, 'data_description_2'):
        print(sa.describe_data(data_sets, c.data_description_2), '\n')


    #### VISUALIZATION

    ## Single scatter plot for variable comparison.
    if hasattr(c, 'scatterplot'):
        scatter = dv.Scatterplot_Comparison()
        full_dic = ut.unfold_dictionary(c.scatterplot, scatter.keys)

        if full_dic['df'] is None:
            full_dic['df'] = 'train'

        if full_dic['index'] is None:
            full_dic['index'] = 'all'

        if split is False and (full_dic['df'] not in ['main', 'train']):
            raise Exception(f"The main data set hasn't been split, therefore, the `df` cannot be set to '{full_dic['df']}'.")

        if (full_dic['container'] == 'trim') and not hasattr(c, 'trim_container'):
            raise Exception("`trim_container` hasn't been found.")
        if (full_dic['container'] == 'query') and not hasattr(c, 'query_container'):
            raise Exception("`query_container` hasn't been found.")
            
        unfolded_all_data_sets = all_data_sets[full_dic['container']]

        if full_dic['index'] == 'all':
            if full_dic['container'] == 'trim':
                full_dic['index'] = list(range(len(c.trim_container)))
            if full_dic['container'] == 'query':
                full_dic['index'] = list(range(len(c.query_container)))

        if hasattr(c, 'trim_container') and (full_dic['container'] == 'trim'):
            if all([False for i in full_dic['index'] if i not in range(len(c.trim_container))]) is False:
                raise Exception('At least one scatterplot index value is outside the `trim_container` length.')
       
        selected_sets = [unfolded_all_data_sets[set][full_dic['df']] for set in unfolded_all_data_sets]
        selected_sets = [selected_sets[i] for i in full_dic['index']]

        if full_dic['container'] == 'trim':
            container = c.trim_container
        if full_dic['container'] == 'query':
            container = [dic[full_dic['container']] for dic in c.query_container]

        if split is False:
            df = 'main'
        else:
            df = full_dic['df']
        
        scatter.scatterplot_comparison(
            df,
            full_dic['y'],
            full_dic['x'],
            selected_sets,
            container,
            full_dic['container'],
            )

    
    if hasattr(c, 'display_panels'):
        panel_comparison = dv.Display_Panels(c.display_panels, all_data_sets, split)
        panel_comparison.type_check
        panel_comparison.check_input_validity
        panel_comparison.append_data
                   
        if hasattr(c, 'histograms'):
            full_dic = ut.unfold_dictionary(c.histograms, dv.Histogram.keys)

            dv.Histogram.histogram_panel(
                var_list=full_dic['features'],
                bins_input=full_dic['bins'],
                density_input=full_dic['density'],
                cumulative_input=full_dic['cumulative'],
                df1=panel_comparison.df_1,
                df2=panel_comparison.df_2_hist,
                )
            
        if hasattr(c, 'boxplots'):        
            dv.boxplot_panel(
                c.boxplots,
                panel_comparison.df_1,
                panel_comparison.df_2_box,
                )

        if hasattr(c, 'scatterplots'):                
            dv.scatterplot_panel(
                var_list=c.scatterplots['features'],
                target_var=c.scatterplots['target'],
                df1=panel_comparison.df_1,
                df2=panel_comparison.df_2_scatter,
                custom_title=c.scatterplots['title'],
                )
            
        if hasattr(c, 'heatmap'):                
            dv.heat_map(c.heatmap, panel_comparison.df_1)

    if (not hasattr(c, 'display_panels')) and\
        (hasattr(c, 'histograms') or hasattr(c, 'boxplots') or hasattr(c, 'scatterplots') or hasattr(c, 'heatmap')):
        raise Exception('For at least one panel to be displayed, `display_panels` must be activated.')
        
    #-------------------------------------------------------------------------------------------

    print('\nChecking Non-numerical Variables:')
    non_numeric = dc.check_if_numeric(data_sets['train'], data_sets['train'].columns, True)
    if non_numeric:
        print('\n    - Non-numeric variables in the main data frame:')
        for col in non_numeric:
            print(f'       - {col}')
        print('\n')
        if c.drop_non_numeric:
            for df in data_sets:
                data_sets[df] = data_sets[df].drop(columns=non_numeric)
            print('    - Non-numeric variables dropped.')
            print('\n')

    if c.correlations:
        if split is False:
            if (c.correlations) or (c.correlations == 'main') or (c.correlations == 'train'):
                corr_set_to_print = data_sets['train']
                set_name = 'main'

        if split:
            if c.correlations is True:
                corr_set_to_print = data_sets['train']
                set_name = 'train'

            if c.correlations in all_sets_names:
                corr_set_to_print = data_sets[c.correlations]
                set_name = c.correlations

        print(f"Pearson's Correlations ({set_name})\n")
        print(sa.correlation_table(corr_set_to_print))


    if hasattr(c, 'x_var_container_vif'):
        print('\n\n## Analysis Of Variance Inflation Factor: \n')
        vif_obj = sa.VIF()
        vif_obj.df = data_sets['train']
        vif_obj.X = c.x_var_container_vif
        vif_obj.store_vif()
        vif_obj.print_vif_container()

    check_fs_algorithms = any(
        [
            hasattr(c, 'univariate_container'),
            hasattr(c, 'recursive_elimination_container'),
            hasattr(c, 'sequential_container'),
            hasattr(c, 'importance_weights_container'),
        ]
    )

    if check_fs_algorithms:
        print('\n#### Feature Selection Algorithms\n')
        selector = fs.Feat_Selector()
        selector.df = data_sets['train']

        # Check if features are numeric when piped directly from the main DataFrame.
        if hasattr(c, 'target_container'):
            all_features = [col for col in data_sets['train'].columns if col not in c.target_container]
        else:
            raise Exception('`target_container` must be set with at least one target name.')
        if hasattr(c, 'initial_features_fs'):
            check_belonging = [True if col in all_features else False for col in c.initial_features_fs]
            if all(check_belonging):
                selector.X = c.initial_features_fs # features manually assigned
            else:
                not_belonging = ', '.join([col for col in c.initial_features_fs if col not in all_features])
                raise Exception(f'These variables: {not_belonging}, are not in included in the features container:\n{all_features}.')
        else:
            selector.X = all_features

        if hasattr(c, 'univariate_container'):
            selector.univariate_container = c.univariate_container
            selector.get_selection_results(selector.univariate_container)
            selector.print_container_results(selector.univariate_container)

        if hasattr(c, 'recursive_elimination_container'):
            selector.recursive_elimination_container = c.recursive_elimination_container
            selector.get_selection_results(selector.recursive_elimination_container)
            selector.print_container_results(selector.recursive_elimination_container)

        if hasattr(c, 'sequential_container'):
            selector.sequential_container = c.sequential_container
            selector.get_selection_results(selector.sequential_container)
            selector.print_container_results(selector.sequential_container)

        if hasattr(c, 'importance_weights_container'):
            selector.importance_weights_container = c.importance_weights_container
            selector.get_selection_results(selector.importance_weights_container)
            selector.print_container_results(selector.importance_weights_container)

        # Check unique combinations of features derived from the feature selection stage.
        vars_feature_selection = selector.collect_unique_results()
        print('\n## Unique Combinations Of Explanatory Variables Derived From The Feature Selection Stage:\n')
        for dic in vars_feature_selection:
            print(f"- Target: '{dic['target']}'")
            print(f"    - {dic['x_vars']}\n")
        print(f'\nTotal: {len(vars_feature_selection)}')


    if c.make_regression:
        print('\n\n#### Regression Results\n\n')

        # Regression analysis for explanatory variables manually specified. 
        run_reg = lr.RunRegressions()
        run_reg.train = train
        run_reg.validation = validation

        if c.plug_feature_selection and (check_fs_algorithms is False):
            raise Exception('No feature selection process took place. To continue without estimating models that resulted from a feature selection process, set `plug_feature_selection = False`.')

        if c.plug_feature_selection:
            for model in vars_feature_selection:
                run_reg.X.append(model['x_vars'])
                run_reg.y.append(model['target'])
                run_reg.detail.append(f"{model['criterion']}")
        
        if hasattr(c, 'manual_model_container'):
            for model in c.manual_model_container:
                run_reg.X.append(model['x_vars'])
                run_reg.y.append(model['target'])
                run_reg.detail.append('manually selected')
        else:
            if ~c.plug_feature_selection:
                if hasattr(c, 'target_container'):
                    X = [col for col in train if col not in c.target_container]
                    y = c.target_container[0]
                    run_reg.X.append(X)
                    run_reg.y.append(y)
                    run_reg.detail.append('default model')
                else:
                    raise Exception('Because there is no `target_container` from which to select a target variable (in the control script), no default model could be estimated.')
    
        run_reg.print_summary()
        run_reg.produce_all_results()
        run_reg.print_all_results(c.residuals_analysis, c.residuals_set)

        if c.error_comparison:
            print('\n## Error Measurement Comparison\n')
            run_reg.compare_error_results()
            print('\n')


    if hasattr(c, 'dataset_name'):
        data_sets['train'].to_csv(f'{DataPath.DATASET_PATH}/{c.dataset_name}')

    if hasattr(c, 'pdf_name'):

        # clean_cache_cmd = f'jupyter nbconvert {DataPath.NOTEBOOK_PATH} --stdout '
        # clean_cache = subprocess.Popen(clean_cache_cmd, shell=True)

        abs_output_path = f"{DataPath.PDF_PATH}/notebook_version_{c.pdf_name}.pdf"
        to_pdf = f"jupyter nbconvert --to pdf --TemplateExporter.exclude_input=True {DataPath.NOTEBOOK_PATH} --output-dir {abs_output_path}"
        # to_pdf = f"jupyter nbconvert --to pdf --no-prompt --TemplateExporter.exclude_input=True {DataPath.NOTEBOOK_PATH} --output-dir {abs_output_path}"
        save_output = subprocess.Popen(to_pdf, shell=True)


    print('\n[End Of Report]')

    return 


  