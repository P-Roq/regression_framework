import numpy as np
import pandas as pd

def read_data(path: str) -> pd.core.frame.DataFrame:
    return pd.read_csv(path)


def lower_case_cols(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    df.columns = [col.lower() for col in df.columns]
    return df

# class ColumnsGroups:
    # ALL_COLS = list(df.columns) # features (explanatory vars) and target vars 
    # FEATS = [i for i in df if i not in ['log_charges', 'charges']] # only features



