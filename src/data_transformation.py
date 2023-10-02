from typing import Union, Iterable

import re
import pandas as pd 
import numpy as np 

from pandas.api.types import is_numeric_dtype

from scipy.stats import iqr, zscore
from sklearn.preprocessing import maxabs_scale
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import normalize
from sklearn.preprocessing import scale

class Filter_Data:
    keys = ['df', 'query']

    def filter_data(
            self,
            df: pd.core.frame.DataFrame,
            query: str,
            ) -> pd.core.frame.DataFrame: 

        filtered = df.query(query)

        return filtered.reset_index(drop=True)

class Trim_Data:
    keys = ['df', 'variable', 'boundaries', 'value', 'scaling_factor', 'z_score', 'ddof']

    def trim_data(
        self,
        df: pd.core.frame.DataFrame,
        variable: str,
        boundaries: str = None,
        value: Union[int, float, tuple] = None,
        scaling_factor: Union[int, float, tuple] = None,
        z_score: Union[str, int, tuple] = None,
        ddof: int = None,
        ) -> pd.core.frame.DataFrame: 


        if value:
            if (scaling_factor is not None) or (z_score is not None) or (ddof is not None):
                raise Exception(f"To properly set the fixed values threshold(s), `scaling_factor`, `z_score`, `ddof`, must be set to None.")

            if isinstance(value, (int, float, complex)):
                lower_threshold, upper_threshold = (value, value)
                
            if isinstance(value, tuple):
                if value[0] > value[1]:
                    raise Exception('The minimum threshold must must be lower than the maximum threshold: `value = (min, max)`.')      
                  
                lower_threshold, upper_threshold = (value[0], value[1]) 
        
        if scaling_factor:

            if (value is not None) or (z_score is not None) or (ddof is not None):
                raise Exception(f"To properly set the IQR threshold(s), `value`, `z_score`, `ddof`, must be set to None.")
            
            if isinstance(scaling_factor, (int, float, complex)):
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
            if (value is not None) or (scaling_factor is not None):    
                raise Exception(f"To properly set the z-score threshold(s), `value`, `scaling_factor`, must be set to None.")
            if ddof is None:
                ddof = 1

            var_name_z = f'{variable}_z_score'
            df[var_name_z] = zscore(df[variable].values, ddof=ddof, nan_policy='omit')
        
            variable = var_name_z

            if isinstance(z_score, (int, float, complex)):
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

        return df.reset_index(drop=True)


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


class Nonbinary_To_Dummies:
    keys = ['variable', 'add_suffix', 'drop_dummy', 'dummies_names', 'drop_current']

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

class Percentage_Change:
    keys = ['variable', 'rows', 'replace_na', 'drop_current', 'differences_only']

    def percentage_change(
            var: str,
            df: pd.core.frame.DataFrame,
            rows: Union[int, None] = None,
            replace_na = None,
            drop_current: bool = False,
            differences_only: bool = False,
            ):
        
        if rows is None:
            rows = 1
        
        if differences_only:
            new_var_name = f'{var}_diff_{rows}'
        else:
            new_var_name = f'{var}_pct_{rows}'

        if new_var_name in df.columns:
            df = df.drop(columns=new_var_name)

        df.insert(
            loc=list(df.columns).index(var)+1,
            column=new_var_name,
            value=df[var].pct_change(rows),
        )

        if replace_na is None:
            df[new_var_name] = df[new_var_name].fillna(0)
        else:
            df[new_var_name] = df[new_var_name].fillna(replace_na)

        if drop_current:
            df = df.drop(columns=var)

        return df


class Rolling_Window:
    keys = ['variable', 'rows', 'transform', 'one_ahead', 'replace_na', 'ddof', 'drop_current']

    def rolling_window(
        var: str,
        df: pd.core.frame.DataFrame,
        rows: int,
        transform: str = None,
        one_ahead: bool = False,
        replace_na: Union[str, int, float, complex] = None,
        ddof: int = None,
        drop_current: bool = False,
        ):

        transformations = ['mean', 'sum', 'minimum', 'maximum', 'variance', 'standard_deviation',]

        if (transform in ['variance', 'standard_deviation']) and (ddof is None):
            ddof = 0
        if (transform not in ['variance', 'standard_deviation']) and (ddof):
            raise Exception("Degrees of freedom have been specified but `transform` has not.")
        
        new_var_name = f'{var}_roll_{rows}' 

        if transform is None:
            rolled = df[var].rolling(window=rows).mean()
        else:
            if transform in transformations:
                if transform == 'mean':
                    rolled = df[var].rolling(window=rows).mean()
                if transform == 'sum':
                    rolled = df[var].rolling(window=rows).sum()
                if transform == 'minimum':
                    rolled = df[var].rolling(window=rows).min()
                if transform == 'maximum':
                    rolled = df[var].rolling(window=rows).max()    
                if transform == 'variance':
                    rolled = df[var].rolling(window=rows).var(ddof)
                if transform == 'standard_deviation':
                    rolled = df[var].rolling(window=rows).std(ddof)
            else:
                raise Exception("`transform` only takes one of the following strings: 'mean', 'sum', 'minimum', 'maximum', 'variance' and 'standard_deviation'.")

        df.insert(
            loc=list(df.columns).index(var)+1,
            column=new_var_name,
            value=rolled,
        )
        
        if one_ahead:
            df[new_var_name] = df[new_var_name].shift(1)

        if replace_na is None:
            df[new_var_name] = df[new_var_name].fillna(0)
        else:
            df[new_var_name] = df[new_var_name].fillna(replace_na)

        if drop_current:
            df = df.drop(columns=var)

        return df


class Replace_Values:
    keys = ['variable', 'replace', 'value', 'transform', 'ddof',]

    def replace_values(
        variable: str,
        df: pd.core.frame.DataFrame,
        replace: Union[object, int, float, complex, bool, str, list, tuple] = 'missing_values', 
        value: Union[int, float, complex, str, bool, None] = None,
        transform: Union[str, None] = None,
        ddof: Union[int, None] = None,
        ) -> pd.core.frame.DataFrame:

        message = None

        if value and transform:
            raise Exception('If `transform` is chosen to replace NAs then `value` must be None, and vice-versa.')
        
        transformations = [
                'minimum',
                'maximum',
                'mode',
                'median',
                'mean',
                'variance',
                'standard_deviation',
                ]
            
        if transform:            
            if transform not in ['variance', 'standard_deviation']:
                if ddof:
                    raise Exception('Degrees of freedom, `ddof`, must only be set when `transform` is set as `variance` or `standard_deviation`.')
            else:
                if ddof is None:
                    ddof = 1

            if transform in transformations:
                if transform == 'minimum':
                    value = df[variable].min()
                if transform == 'maximum':
                    value = df[variable].min()
                if transform == 'mode':
                    value = df[variable].mode()
                    if len(value) > 1:
                        raise Exception(f'{variable} has multiple modes:\n{value}.')
                if transform == 'median':
                    value = df[variable].median()
                if transform == 'mean':
                    value = df[variable].mean()
                if transform == 'variance':
                    value =  df[variable].var(ddof=ddof,)
                if transform == 'standard_deviation':
                    value =  df[variable].std(ddof=ddof,)

            elif (re.fullmatch('quantile=(0or1).\d+', transform)) or (re.fullmatch('quantile=(0or1)', transform)):
                q = float(transform[9:])
                if 0 <= q <= 1:
                    value = df[variable].quantile(q)
                else:
                    raise Exception("Values passed should be floats within [0, 1]")
            else:
                raise Exception(f"The '{transform}' could not be found, or calculated, or inserted for '{variable}'.")

        if replace == 'missing_values':
            count_na = df[variable].isna().sum()
            if count_na == 0:
                message = f'- No replacements were made in {variable} since no missing values were found in it.'
            else:
                df[variable] = df[variable].fillna(value)

        elif isinstance(replace, (list, tuple, set)):
            not_replaced = [value for value in replace if value not in set(df[variable].unique())]
            if len(not_replaced) == len(replace):
                message = f"- No replacements took place since none of the values in `replace` could be found in {variable}."
            
            if 0 < len(not_replaced) < len(replace):
                not_replaced = [str(i) for i in not_replaced]
                message = f"- The following values: {', '.join(not_replaced)}, could not be found in {variable}."

            df[variable] = df[variable].apply(lambda x: value if x in replace else x)

        elif isinstance(replace, (int, float, complex, str)):
            check_replaced = replace in set(df[variable].unique())
            if ~check_replaced:
                message = f"- No replacement took place since the value in `replace`: {replace}, could not be found in {variable}."
            
            df[variable] = df[variable].apply(lambda x: value if x == replace else x)
        
        return (df, message,)


class Standardize:
    keys = ['vars', 'transform', 'include_binary', 'round']

    def standardize(
            df: pd.core.frame.DataFrame,
            vars: 'list[str]' = None,
            transform: Union[str, None] = None,
            include_binary: Union[bool, 'list[str]'] = None,
            round: int = None,
            ) -> pd.core.frame.DataFrame:
        
        df = df.copy()

        numerical = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]    

        if vars:
            vars = [col for col in vars if pd.api.types.is_numeric_dtype(df[col])]

        if include_binary:
            if isinstance(include_binary, bool):
                if vars: 
                    to_standardize = vars
                else:    
                    to_standardize = numerical
            if isinstance(include_binary, list):
                if vars: 
                    raise Exception('Listing the binary variables to standardize only works when the parameter `vars` is omitted; otherwise, specify in `vars` what binary variables should also be included.')

                else:    
                    all_binary = [col for col in numerical if list(df[col].unique()) == [0, 1]]
                    binary_to_exclude = [col for col in all_binary if col not in include_binary]
                    to_standardize = [col for col in numerical if col not in binary_to_exclude]
        else:
            if vars: 
                to_standardize = [col for col in vars if list(df[col].unique()) != [0, 1]]
            else:
                to_standardize = [col for col in numerical if list(df[col].unique()) != [0, 1]]

        std_types = ['max_abs', 'min_max', 'z_score']

        if transform:
            if transform in std_types: 
                if transform == 'min_max':
                    df[to_standardize] = minmax_scale(df[to_standardize])
                if transform == 'max_absolute':
                    df[to_standardize] = maxabs_scale(df[to_standardize])
                if transform == 'z_score':
                    df[to_standardize] = scale(df[to_standardize])
            else:
                raise Exception(f'Only one of the following standardization/re-scaling methods can be used: {", ".join(std_types)}')

        else:   
            df[to_standardize] = minmax_scale(df[to_standardize])

        if round:
            df[to_standardize] = df[to_standardize].round(round)

        return df

