import pandas as pd 
import numpy as np 
import re

from sklearn.linear_model import LinearRegression as lr
from sklearn.feature_selection import SelectKBest, RFE, SequentialFeatureSelector, SelectFromModel
from sklearn.feature_selection import chi2, f_classif, f_regression

from typing import Union

class Feat_Selector:
    def __init__(self):
        self.df: pd.core.frame.DataFrame = None
        self.X: list = None 
        self.univariate_container: list = None
        self.recursive_elimination_container: list = None
        self.sequential_container: list = None
        self.importance_weights_container: list = None

        self.univariate_results_container: list = []
        self.recursive_elimination_results_container: list = []
        self.sequential_results_container: list = []
        self.importance_weights_results_container: list = []


    #### Selection algorithms.

    def select_k_best(
        self,
        target: str,
        k_vars: int,
        criterion: str,
        ) -> list:

        if isinstance(k_vars, int):
            if (k_vars <= 0) | (k_vars >= len(self.X)):
                raise ValueError('Error: the number of features to select, `k_vars`, must be higher than 0 and lower than initial number of variables contained in `selector_x_vars`.')

        if criterion == 'chi2':
            criterion = chi2

        elif criterion == 'f_classif':
            criterion = f_classif
            # Check whether there are constant vars/columns in the data set. 
            constant_explanatory_variables = []
            for col in self.df[self.X].columns:
                if len(self.df[col].unique()) == 1:
                    constant_explanatory_variables.append(col)
            if len(constant_explanatory_variables) > 0:
                print('Warning - One or more explanatory variables are constant (only have one value). Consider removing them:')
                print(f"    - {', '.join(constant_explanatory_variables)}")
        
        elif criterion == 'f_regression':
            criterion = f_regression

        else:
            raise ValueError('Error: the criterion must be on of following: "f_classif", "f_regression", "chi2".')

        X_selection = (
            SelectKBest(score_func=criterion, k=k_vars)
            .fit(self.df[self.X], self.df[target])
        )

        X_selection_list = X_selection.get_feature_names_out().tolist()

        model_dict = {'target': target, 'x_vars': X_selection_list}

        self.univariate_results_container.append(model_dict)

        return 


    def recursive_elimination(
        self,
        target: str,
        k_vars: int, 
        step: Union[int, float],
        ) -> list:

        if isinstance(k_vars, int):
            if (k_vars <= 0) | (k_vars >= len(self.X)):
                raise ValueError('Error: the number of features to select, `k_vars`, must be higher than 0 and lower than initial number of variables contained in `selector_x_vars`.')


        X_selection = (
            RFE(estimator=lr(), n_features_to_select=k_vars, step=step)
            .fit(self.df[self.X], self.df[target])
        )

        X_selection_list = X_selection.get_feature_names_out().tolist()

        model_dict = {'target': target, 'x_vars': X_selection_list}

        self.recursive_elimination_results_container.append(model_dict)

        return 



    def sequential_selection(
        self,
        target: str,
        k_vars: Union[int, str], 
        direction: str,
        tolerance: Union[float, None],
        ) -> list:

        if isinstance(k_vars, int):
            if (k_vars <= 0) | (k_vars >= len(self.X)):
                raise ValueError('Error: the number of features to select, `k_vars`, must be higher than 0 and lower than initial number of variables contained in `selector_x_vars`.')

        if direction not in ['forward', 'backward']:
            raise ValueError('Error: the sequential direction of the selection algorithm must be either "forward" or "backward".')

        X_selection = (
            SequentialFeatureSelector(
                estimator=lr(),
                n_features_to_select=k_vars,
                direction=direction,
                tol=tolerance
            )
            .fit(self.df[self.X], self.df[target])
        )

        X_selection_list = X_selection.get_feature_names_out().tolist()

        model_dict = {'target': target, 'x_vars': X_selection_list}

        self.sequential_results_container.append(model_dict)

        return 



    def importance_weights(
        self,
        target: str,
        k_vars: Union[int, callable, None],
        threshold: Union[str, float, None],
        ) -> list:

        if isinstance(k_vars, int):
            if (k_vars <= 0) | (k_vars >= len(self.X)):
                raise ValueError('Error: the number of features to select, `k_vars`, must be higher than 0 and lower than initial number of variables contained in `selector_x_vars`.')


        X_selection = (
            SelectFromModel(
                estimator=lr(),
                threshold=threshold,
                max_features=k_vars,
            )
            .fit(self.df[self.X], self.df[target])
        )

        X_selection_list = X_selection.get_feature_names_out().tolist()

        model_dict = {'target': target, 'x_vars': X_selection_list}

        self.importance_weights_results_container.append(model_dict)

        return 


    #### Get results.
    def get_selection_results(self, container: list) -> None:
        for i, dic in enumerate(container):
            if container == self.univariate_container:
                self.select_k_best(dic['target'], dic['k_vars'], dic['criterion'])
            if container == self.recursive_elimination_container:
                self.recursive_elimination(dic['target'], dic['k_vars'], dic['step'])
            if container == self.sequential_container:
                self.sequential_selection(dic['target'], dic['k_vars'], dic['direction'], dic['tolerance'])
            if container == self.importance_weights_container:
                self.importance_weights(dic['target'], dic['k_vars'], dic['threshold'])

        return
    

    #### Result printer.
    def print_container_results(self, container: list) -> None:

        if container == self.univariate_container:
            print('## Univariate Selection (Select k Best):\n')
        if container == self.recursive_elimination_container:
            print('## Recursive Elimination Selection:\n')
        if container == self.sequential_container:
            print('## Sequential Selection:\n')
        if container == self.importance_weights_container:
            print('## Importance Weights Selection (Select From Model):\n')

        for i, dic in enumerate(container):
            print(f'Container index: {i+1}\n')
            print(f'Parameters: {dic}\n')
            print('Variables selected:\n')
            if container == self.univariate_container:
                X_selection_list = self.univariate_results_container[i]['x_vars']
            if container == self.recursive_elimination_container:
                X_selection_list = self.recursive_elimination_results_container[i]['x_vars'] 
            if container == self.sequential_container:
                X_selection_list = self.sequential_results_container[i]['x_vars'] 
            if container == self.importance_weights_container:
                X_selection_list = self.importance_weights_results_container[i]['x_vars'] 

            for var in X_selection_list:
                print(f"        - '{var}'")

            if i == len(container) - 1:
                print('\n--------------------------------------------------------------------------------\n')
            else: 
                print('\n------------------------------------\n')   


        return


    def collect_unique_results(self):
        """This function fills a list with dictionaries of unique combinations of explanatory 
        variables originated during the feature selection stage. Because different algorithms/selection strategies
        can arrive at the same combinations, the 'criterion' item stores the selection strategies that
        that arrived at the same 'x_vars' combination.  
        """

        df_all_results = pd.DataFrame(columns=['target', 'x_vars', 'criterion'])
        unique_results  = []

        results_containers = [
            self.univariate_results_container,
            self.recursive_elimination_results_container,
            self.sequential_results_container,
            self.importance_weights_results_container,
        ]

        tags = ['univariate', 'recursive', 'sequential', 'importance weights']

        # Fill in `df_all_results` with all the results in the 4 results containers.
        # Each row has 3 columns: 'target', 'x_vars', 'criterion'. 
        for i1, container in enumerate(results_containers):
            for i2, dic in enumerate(container):
                row = pd.DataFrame(
                    {
                        'target': dic['target'],
                        'x_vars': ', '.join(dic['x_vars']),
                        'criterion': tags[i1],
                    },
                    index=[0]
                )
                
                df_all_results = pd.concat([df_all_results, row], axis=0).reset_index(drop=True)
        
        # Collect unique `x_var` combinations in the form of dictionaries to be stored in `unique_results`.
        # Start to collect unique combinations without criterion (because this value can vary, we add later). 
        for i in range(df_all_results.shape[0]):
            dic = {
                'target': df_all_results.loc[i, 'target'],
                'x_vars': df_all_results.loc[i, 'x_vars'],
                'criterion': []
                }
            
            if dic not in unique_results:
                unique_results.append(dic)

        # Resorting again to `df_all_results` to collect the criterion/criteria associated to each
        # unique combination of `x_vars` and store it in `dic['criterion']` for each dictionary.
        for i, dic in enumerate(unique_results):
            for i in range(df_all_results.shape[0]):
                if {'target': dic['target'], 'x_vars': dic['x_vars']} == {'target': df_all_results.loc[i, 'target'], 'x_vars': df_all_results.loc[i, 'x_vars'],}:
                    if df_all_results.loc[i, 'criterion'] not in dic['criterion']:
                        dic['criterion'].append(df_all_results.loc[i, 'criterion'])

        # Convert back `x_vars` from a string to a list of strings while converting `dic['criterion']`
        # to a string. 
        for dic in unique_results:
            dic['x_vars'] = re.split(', ', dic['x_vars']) 
            dic['criterion'] = ', '.join(dic['criterion'])


        return  unique_results