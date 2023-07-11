import subprocess, re, importlib, glob

from src import data_loader
from src import data_viewer as viewer
from src import data_transformation as dt
from src import data_splitting as ds
from src import data_visualization as dv
from src import linear_regression as lr
from src import statistical_tests as st
from src import feature_selection as fs
from src import data_checks as dc
from src import statistical_analysis as sa

import numpy as np

# Detect and import the quick set-up script. 
extract_name = re.findall('./(\w+)', glob.glob(f'src/ctrl*.py')[0])[0]
c = importlib.import_module(f'src.{extract_name}') # 'c' for control

class DataPath:
    DATASET_PATH = f"../{c.main_folder_name}/exported_csv"
    SOURCE_DATA_PATH = f"../{c.main_folder_name}/data/{c.data_file_name}"
    PDF_PATH = f"../{c.main_folder_name}/exported_pdf"
    NOTEBOOK_PATH = f"../{c.main_folder_name}/output.ipynb"

def main() -> None:
    if c.identify_origin_script:
        print(f'Control script: {extract_name}.py\n\n')

    df = data_loader.read_data(DataPath.SOURCE_DATA_PATH)

    # 2D array to compare with the version after transformations.
    df_initial = df.values 

    print('#### Initial Variables:\n') 
    print(df.info(), '\n')

    if c.print_columns:
        print('\nAll Columns:')
        print('\n', list(df.columns), '\n')

    print('\nData Viewer 1:\n')     
    if hasattr(c, 'df_coordinates_1'):
        viewer.view_data(
            df,
            c.df_coordinates_1['rows'],
            c.df_coordinates_1['columns'],
        )
    else:
        viewer.view_data(df, None, None)
    print('\n\n')

    if c.data_description_1:
        print('Variable Description Before Data Processing:\n')
        print(df.describe(), '\n\n')

    #### Data processing.

    if c.check_na:
        print('Missing Values (NAs) Per Column:')
        na_values = df.isna().sum()
        print(f'\n{na_values}\n\n')

    if hasattr(c, 'replace_na_values'):
        for dic in c.replace_na_values:
            df = dt.replace_na(
                dic['variable'],
                df,
                dic['value'],
                dic['other'],
                dic['ddof'],
                )

    if c.remove_na:
        df = df.dropna().reset_index(drop=True)

    if c.check_na | c.remove_na:
        print('Missing values (NAs) After Replacement/Removal:')
        na_values = df.isna().sum()
        print(f'\n{na_values}\n\n')


    if hasattr(c, 'convert_binary_to_dummy'):
        for dic in c.convert_binary_to_dummy:
            df = dt.binary_to_dummy(
                dic['variable'],
                df,
                dic['invert'],
                dic['drop_current']
                )

    if hasattr(c, 'convert_nonbinary_to_dummies'):
        for dic in c.convert_nonbinary_to_dummies:
            df = dt.nonbinary_to_dummies(
                dic['variable'],
                df,
                dic['drop_dummy'],
                dic['add_suffix'],
                dic['dummies_names'],
                dic['drop_current'],
                )

    if hasattr(c, 'convert_to_log'):
        for dic in c.convert_to_log:
            df = dt.log_variable(
                dic['variable'],
                df,
                dic['drop_current']
                )

    if hasattr(c, 'convert_to_categorical'):
        for dic in c.convert_to_categorical:
            df = dt.categorize_variable(
                dic['variable'],
                df,
                dic['drop_current']
                )

    if hasattr(c, 'trimmer_container'):
        trimmer = dt.Trim_DF()
        for dic in c.trimmer_container:
            dic_none = {key: None for key in dt.Trim_DF.keys if key not in dic.keys()}
            full_dic = {**dic, **dic_none}
            trimmer.inserted_trimmed_df(
                variable=full_dic['variable'],
                df=df,
                boundaries=full_dic['boundaries'],
                value=full_dic['value'],
                scaling_factor=full_dic['scaling_factor'],
                z_score=full_dic['z_score'],
                ddof=full_dic['ddof'],
            )

        if hasattr(c, 'replace_for_trimmed'):
            df = trimmer.trimmed[c.replace_for_trimmed]

    if hasattr(c, 'queries_container'):
        filter_df = dt.Filtered_DF()
        for query in c.queries_container:
            filter_df.insert_filtered_df(query, df)

        if hasattr(c, 'replace_for_queried'):
            df = filter_df.filtered[c.replace_for_queried] 


    if not np.array_equal(df.values, df_initial):
        print('#### Variables After Transformation:\n')
        print(df.info(), '\n')

    print('\nData Viewer 2:\n')     
    if hasattr(c, 'df_coordinates_2'):
        viewer.view_data(
            df,
            c.df_coordinates_2['rows'],
            c.df_coordinates_2['columns'],
        )
    else:    
        viewer.view_data(df, None, None)
    print('\n\n')

    if c.data_description_2:
        print('\nVariable Description After Data Processing:\n')
        print(df.describe(), '\n')


    #### Visualization

    if hasattr(c, 'df_variants_for_scatterplot'):
        # From the queried DFs available in the dictionary `filtered`, pick those to be
        # visually displayed and group them in a smaller dictionary - `query_selection`.
        selected_queried_dfs = [filter_df.filtered[i] for i in c.df_variants_for_scatterplot]
        selected_queries = [c.queries_container[i] for i in c.df_variants_for_scatterplot]
        dv.scatter_compare_filtered(
            c.queries_scatter_variables['y'],
            c.queries_scatter_variables['x'],
            selected_queried_dfs,
            selected_queries,
            )
    
    # This block of code renames as `df2` the trimmed/queried data frame indicated in the dictionary
    # `c.compare_visually` to be compared with the main data frame in the graph panels. Three alias have 
    # been created - `df2_hist`, `df2_box`, `df_scatter`, so that `df2` is used as an argument in the graph 
    # panel functions below, when the right string reference - 'hist', 'box' and/or 'scatter' are set 
    # in `c.compare_visually['panel']`.   
    df2 = None
    df2_hist = None
    df2_box = None
    df2_scatter = None

    if hasattr(c, 'compare_visually'):
        if c.compare_visually['container'] == 'trimmer_container':
            df2 = trimmer.trimmed[c.compare_visually['index']]
        if c.compare_visually['container'] == 'queries_container':
            df2 = filter_df.filtered[c.compare_visually['index']]

        if 'hist' in c.compare_visually['panel']:
            df2_hist = df2
        if 'box' in c.compare_visually['panel']:
            df2_box = df2
        if 'scatter' in c.compare_visually['panel']:
            df2_scatter = df2            

    if hasattr(c, 'hist_cols'):
        dv.histogram_panel(c.hist_cols, df, df2_hist)
    if hasattr(c, 'boxplot_cols'):        
        dv.boxplot_panel(c.boxplot_cols, df, df2_box)
    if hasattr(c, 'scatter_dict'):                
        dv.scatterplot_panel(
            var_list=c.scatter_dict['features'],
            target_var=c.scatter_dict['target'],
            df1=df,
            df2=df2_scatter,
            custom_title=c.scatter_dict['title'],
            )
    if hasattr(c, 'heatmap_cols'):                
        dv.heat_map(c.heatmap_cols, df)

    print('Checking Non-numerical Variables:')
    non_numeric = dc.check_if_numeric(df, df.columns, True)
    if non_numeric:
        print('\n    - Non-numeric variables in the main data frame:')
        for col in non_numeric:
            print(f'       - {col}')
        print('\n')
        if c.drop_non_numeric:
            df = df.drop(columns=non_numeric)
            print('    - Non-numeric variables dropped.')
            print('\n')

    if c.correlations:
        print("Pearson's Correlations\n")
        print(sa.correlation_table(df)) 

    if hasattr(c, 'x_var_container_vif'):
        print('\n\n## Analysis Of Variance Inflation Factor: \n')
        vif_obj = sa.VIF()
        vif_obj.df = df
        vif_obj.X = c.x_var_container_vif
        vif_obj.store_vif()
        vif_obj.print_vif_container()

    check_fs_algorithms = any([
        hasattr(c, 'univariate_container'),
        hasattr(c, 'recursive_elimination_container'),
        hasattr(c, 'sequential_container'),
        hasattr(c, 'importance_weights_container'),
    ])

    if check_fs_algorithms:
        print('\n#### Feature Selection Algorithms\n')
        selector = fs.Feat_Selector()
        selector.df = df

        # Check if features are numeric when piped directly from the main DataFrame.
        all_features = [col for col in df.columns if col not in c.target_container]
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

        train, validation, test = ds.split_data(
            df=df,
            rand_state=c.split_data_dict['rand_state'],
            test_size_=c.split_data_dict['validation_size'],
            validation_size_=c.split_data_dict['validation_size'],
            shuffle_=c.split_data_dict['shuffle'],
            )  
    
        # Regression analysis for explanatory variables manually specified. 
        run_reg = lr.RunRegressions()
        run_reg.train = train
        run_reg.validation = validation

        if c.plug_feature_selection & ~check_fs_algorithms:
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
        
        run_reg.print_summary()
        run_reg.produce_all_results()
        run_reg.print_all_results(c.residuals_analysis, c.residuals_set)

        if c.error_comparison:
            print('\n## Error Measurement Comparison\n')
            run_reg.compare_error_results()
            print('\n')


    if hasattr(c, 'dataset_name'):
        df.to_csv(f'{DataPath.DATASET_PATH}/{c.dataset_name}')

    if hasattr(c, 'pdf_name'):

        # clean_cache_cmd = f'jupyter nbconvert {DataPath.NOTEBOOK_PATH} --stdout '
        # clean_cache = subprocess.Popen(clean_cache_cmd, shell=True)

        abs_output_path = f"{DataPath.PDF_PATH}/notebook_version_{c.pdf_name}.pdf"
        to_pdf = f"jupyter nbconvert --to pdf --TemplateExporter.exclude_input=True {DataPath.NOTEBOOK_PATH} --output-dir {abs_output_path}"
        # to_pdf = f"jupyter nbconvert --to pdf --no-prompt --TemplateExporter.exclude_input=True {DataPath.NOTEBOOK_PATH} --output-dir {abs_output_path}"
        save_output = subprocess.Popen(to_pdf, shell=True)


    print('\n[End Of Report]')

    return 


  