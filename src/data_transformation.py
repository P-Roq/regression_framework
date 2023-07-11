from typing import Union

import pandas as pd 
import numpy as np 

from scipy.stats import iqr, zscore


class Filtered_DF:
    def __init__(self):
        self.filtered: list = [] 

    def insert_filtered_df(self, query_: str, df: pd.core.frame.DataFrame) -> None:
        filtered = df.query(query_)
        self.filtered.append(filtered)

        return 
    

class Trim_DF:
    keys = ['variable', 'boundaries', 'value', 'scaling_factor', 'z_score', 'ddof']
    def __init__(self):
        self.trimmed: list = []

    def inserted_trimmed_df(
        self,
        variable: str,
        df: pd.core.frame.DataFrame,
        boundaries: str = None,
        value: Union[int, float, tuple] = None,
        scaling_factor: Union[int, float, tuple] = None,
        z_score: Union[str, int, tuple] = None,
        ddof: int = None,
        ) -> pd.core.frame.DataFrame: 


        if value:
            if (scaling_factor is not None) | (z_score is not None) | (ddof is not None):
                raise Exception(f"To properly set the fixed values threshold(s), `scaling_factor`, `z_score`, `ddof`, must be set to None.")

            if isinstance(value, int) | isinstance(value, float):
                lower_threshold, upper_threshold = (value, value)
                
            if isinstance(value, tuple):
                if value[0] > value[1]:
                    raise Exception('The minimum threshold must must be lower than the maximum threshold: `value = (min, max)`.')      
                  
                lower_threshold, upper_threshold = (value[0], value[1]) 
        
        if scaling_factor:

            if (value is not None) | (z_score is not None) | (ddof is not None):
                raise Exception(f"To properly set the IQR threshold(s), `value`, `z_score`, `ddof`, must be set to None.")
            
            if isinstance(scaling_factor, int) | isinstance(scaling_factor, float):
                lower_scaling_factor, upper_scaling_factor = (scaling_factor, scaling_factor)

            if isinstance(scaling_factor, tuple):
                lower_scaling_factor, upper_scaling_factor = (scaling_factor[0], scaling_factor[1])

            q1 = df[variable].describe()['25%']
            q3 = df[variable].describe()['75%']
            iqr_value = iqr(df[variable].values, nan_policy='omit')

            lower_threshold = q1 - lower_scaling_factor * iqr_value
            upper_threshold = q3 + upper_scaling_factor * iqr_value

        if z_score:
            df = df.copy()
            if (value is not None) | (scaling_factor is not None):    
                raise Exception(f"To properly set the z-score threshold(s), `value`, `scaling_factor`, must be set to None.")
            if ddof == None:
                ddof = 1

            var_name_z = f'{variable}_z_score'
            df[var_name_z] = zscore(df[variable].values, ddof=ddof, nan_policy='omit')
        
            variable = var_name_z

            if isinstance(z_score, int) | isinstance(z_score, float):
                lower_threshold, upper_threshold = (z_score, z_score)
            if isinstance(z_score, tuple):
                if z_score[0] > z_score[1]:
                    raise Exception('The minimum threshold must must be lower than the maximum threshold.')        

                lower_threshold, upper_threshold = (z_score[0], z_score[1])
        
        if boundaries == 'lower':
            df = df.query(f'{lower_threshold} <= {variable}')
        if boundaries == 'upper':
            df = df.query(f'{variable} <= {upper_threshold}')
        if boundaries == 'both':
            df = df.query(f'{lower_threshold} <= {variable} <= {upper_threshold}')
        
        if z_score:
            df = df.drop(columns=[var_name_z])

        df = df.reset_index(drop=True)

        self.trimmed.append(df)

        return 


def binary_to_dummy(
    variable: str, 
    df: pd.core.frame.DataFrame,
    invert: bool,
    drop_current: bool
    ) -> pd.core.frame.DataFrame:
    
    encoding = [0, 1]
    if invert:
        encoding = [1, 0] 

    first_value = df[variable].unique()[0]

    df[f'{variable}_{"d"}'] = df[variable].apply(
        lambda x: encoding[0] if x==first_value else encoding[1]
        )
    
    if drop_current:
        df = df.drop(columns=variable)

    return df


def nonbinary_to_dummies(
    variable: str,
    df: pd.core.frame.DataFrame,
    drop_dummy: Union[int, str, None],
    add_suffix: Union[str, None],
    dummies_names: Union[list, None],
    drop_current: bool,
    ) -> pd.core.frame.DataFrame:

    
    dummies = pd.get_dummies(
        data=df[variable],
        columns=[variable]
    )

    if add_suffix:
        for col in dummies.columns:
            dummies = dummies.rename(columns={col: f'{col}_{add_suffix}'})

    if drop_dummy:
        if isinstance(drop_dummy, int):
            dummies = dummies.drop(columns=[dummies.columns[drop_dummy-1]])
        if isinstance(drop_dummy, str):
            dummies = dummies.drop(columns=[drop_dummy])

    if dummies_names:
        nr_dummies = dummies.shape[1]
        if len(dummies_names) == nr_dummies:
            for i, col in enumerate(dummies.columns):
                dummies = dummies.rename(columns={col: dummies_names[i]})
        else:
            raise Exception(f'There values in `dummies_names` must correspond to the number of dummies created: {nr_dummies}.')
    
    df = pd.concat(
        [
            df,
            dummies,
        ],
        axis=1
    )

    if drop_current:
        df = df.drop(columns=[variable])

    return df


def categorize_variable(
    variable: str,
    df,
    drop_current: bool,
    ) -> pd.core.frame.DataFrame:

    df[f'{variable}_cat'] = pd.Categorical(df[variable])

    if drop_current:
        df = df.drop(columns=variable)

    return df
    
    
def log_variable(
        variable: str,
        df: pd.core.frame.DataFrame,
        drop_current: bool
        ) -> pd.core.frame.DataFrame:
    
    df[f'log_{variable}'] = np.log(df[variable])

    if drop_current:
        df = df.drop(columns=[variable])

    return df


def replace_na(
    variable: str,
    df: pd.core.frame.DataFrame,
    value: Union[int, float, str, bool, None] = None,
    other: Union[str, None] = None,
    ddof: Union[int, None] = None,
    ) -> pd.core.frame.DataFrame:


    if value:
        if other:
            raise Exception('If `other` is chosen to replace NAs then `value` must be None, and vice-versa.')
        
    if ddof:
        if other not in ['variance', 'standard_deviation']:
            raise Exception('Degrees of freedom, `ddof`, must only be set when `other` is set as `variance` or `standard_deviation`.')

    try:
        if other == 'minimum':
            value = df[variable].min()
        if other == 'maximum':
            value = df[variable].min()
        if other == 'mode':
            value = df[variable].mode()
            if len(value) > 1:
                raise Exception(f'{variable} has multiple modes:\n{value}.')
        if other == 'median':
            value = df[variable].median()
        if other == 'mean':
            value = df[variable].mean()
        if other == 'variance':
            value =  df[variable].var(ddof=ddof,)
        if other == 'standard_deviation':
            value =  df[variable].std(ddof=ddof,)
    except:
        raise Exception(f"The '{other}' could not be found, or calculated, or inserted for '{variable}'.")

    if value:
        df[variable] = df[variable].fillna(value)
    if other:
        df[variable] = df[variable].fillna(value)

    return df
