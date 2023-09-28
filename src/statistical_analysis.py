from typing import Union

from pandas.api.types import is_numeric_dtype

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

import pandas as pd
import numpy as np


def describe_data(data_sets: dict, subset: Union[bool, str]) -> pd.core.frame.DataFrame:

    if (subset is False):
        return ''

    allowed_subsets = ['main', 'train', 'validation', 'test']

    if (subset not in allowed_subsets) and (isinstance(subset, bool) is False):
        raise Exception("This variable can only be a boolean or one of the following strings:\n 'main', 'train', 'validation' or 'test'.")

    if (len(data_sets) == 1):
        if (subset != 'main') and (isinstance(subset, bool) is False):
            raise Exception("The main data set hasn't been split.")
        if (subset == 'main') or (subset is True):
            subset = 'main'
            description = data_sets['train'].describe()

    if (len(data_sets) > 1):

        if (subset is True) or (subset=='train'):
            subset = 'train'
            description = data_sets[subset].describe()

        if subset == 'main':
            description = data_sets['main'].describe()

        if subset == 'validation':
            description = data_sets['validation'].describe()

        if subset == 'test':
            description = data_sets['test'].describe()

    print(f'\nVariable Description After Data Processing ({subset} set):\n')

    return description

    
def correlation_table(df: pd.core.frame.DataFrame) -> None:

    corr = df.corr(method='pearson', numeric_only=True)

    corr_triangular = (
        pd.DataFrame(
            data=np.triu(corr.values),
            columns=corr.columns,
            index=corr.index)
            .round(3)
            .replace(0, '-', regex=True)
            .replace(1.0, '-', regex=True)
        )

    corr_triangular = (
        corr_triangular
        .drop(columns=[corr_triangular.columns[0]])
        .drop(index=[corr_triangular.index[-1]])
        ) 
    
    inverse_order = [corr_triangular.columns[-i] for i in range(1, corr_triangular.shape[1]+1)]

    corr_triangular = corr_triangular.reindex(columns=inverse_order)

    return corr_triangular


class VIF:
    def __init__(self):
        self.df: pd.core.frame.DataFrame = None
        self.X: list = []
        self.vif_container: list = []

    def get_vif(self, df, feats):

        df = df[feats]

        numerical = df[[col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]]

        X = add_constant(numerical)

        vif_series = (
            pd.Series(
                [variance_inflation_factor(X.values, i) for i in range(X.shape[1])], 
                index=X.columns,
                name='VIF',
                )
                .drop('const')
                .sort_values()
            )
        
        return vif_series

    def store_vif(self):
        for feats in self.X:
            vif_series = self.get_vif(self.df, feats)
            self.vif_container.append(vif_series)

        return

    def print_vif_container(self):
        for i, vif_series in enumerate(self.vif_container):
            print(f'Features group: {i+1}\n')
            print(vif_series)
            print('\n------------------------------------\n')

        return