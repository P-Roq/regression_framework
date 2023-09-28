from typing import Union

from pandas.api.types import is_numeric_dtype

import pandas as pd
import numpy as np


def check_if_numeric(
        df: pd.core.frame.DataFrame,
        columns: Union[list, None],
        show_not_numeric: bool
    ):

    if columns is None:
        columns = df.columns

    is_numeric = [is_numeric_dtype(df[col]) for col in columns]

    if (all(is_numeric) is False) and (show_not_numeric is True):
        non_numeric = []
        for i, value in enumerate(is_numeric):
            if is_numeric[i] is False:
                non_numeric.append(columns[i])

        return non_numeric

    return None