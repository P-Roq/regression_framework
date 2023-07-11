from typing import Union

from pandas.api.types import is_numeric_dtype

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

import pandas as pd
import numpy as np


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