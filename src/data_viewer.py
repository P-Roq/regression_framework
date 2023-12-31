from typing import Union
import pandas as pd
import numpy as np


class View_Data:
    keys = ['df', 'rows', 'columns']

    def view_data(
        df: pd.core.frame.DataFrame,
        rows: Union[str, list, None],
        columns: Union[str, list, None],
        ) -> pd.core.frame.DataFrame:

        
        if columns is None:
            columns = df.columns
        if rows is None:
            rows = [0, 9]

        if df.shape[0] < 10:
            df = df.loc[:, columns]
        else:
            df = df.loc[
                [i for i in range(rows[0], rows[1]+1)],
                columns
            ]

        print(df.to_string()) 

        return 
