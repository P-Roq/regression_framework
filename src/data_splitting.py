import pandas as pd

from sklearn.model_selection import train_test_split as split

# Split data.
def split_data(df: pd.core.frame.DataFrame, rand_state: int, validation_size_: float, test_size_: float, shuffle_: bool) -> tuple:
    train, other = split(df, random_state=rand_state, test_size=test_size_, shuffle=shuffle_)

    validation, test = split(other, test_size=validation_size_, shuffle=False)

    return train, validation, test