from typing import Union, Iterable

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split as split

def split_data(
    df: pd.core.frame.DataFrame,
    rand_state: Union[int, tuple, list],
    proportions: Union[float, Iterable],
    shuffle: Union[bool, int] = True,
    ) -> tuple:

    if isinstance(rand_state, int):
        rand_state_1, rand_state_2 = (rand_state, rand_state)
    elif isinstance(rand_state, (tuple, list)) and len(rand_state)==2:
        rand_state_1 = rand_state[0]
        rand_state_2 = rand_state[1]

    if (shuffle is True) or (shuffle == 1):
        shuffle_1, shuffle_2 = (True, None)
    elif shuffle == 2:   
        shuffle_1, shuffle_2 = (True, True)
    elif (shuffle is False) or (shuffle == 0):
        shuffle_1, shuffle_2 = (None, None)
    elif (
        (isinstance(shuffle, bool)) 
        or shuffle not in [0, 1, 2]
        ):
        raise Exception('`shuffle` only takes booleans (shuffle once or no shuffle), `1` (shuffle once) or `2` (shuffle twice).')

    if isinstance(proportions, float):
        train_size = proportions

    if isinstance(proportions, Iterable):
        if (len(proportions) > 2) or (len(proportions) == 0):
            raise Exception('If an iterable is passed (tuple or list), it can only store one float value - train size, or two float values - train and validation sizes (from which the test size is inferred).')

        if len(proportions) == 2:
            if sum(proportions) < 1:
                train_size = proportions[0]
                validation_size = proportions[1] / (1 - proportions[0])
            if sum(proportions) > 1:
                raise Exception('If proportions are specified for train and validation sets, such values should add up to 1.')
            if (sum(proportions) == 1):
                train_size = proportions[0]

        if (len(proportions) == 1):
            train_size = proportions[0]


    train, validation = split(
        df,
        random_state=rand_state_1,
        train_size=train_size,
        shuffle=shuffle_1,
        )
    
    if (
        isinstance(proportions, float)
        or all([isinstance(proportions, Iterable), (sum(proportions) == 1)])
        or all([isinstance(proportions, Iterable), (len(proportions) == 1)])
    ):
        test = pd.DataFrame()

        return (
            train.reset_index(drop=True),
            validation.reset_index(drop=True),
            test,
        )
    
    else:
        # The previous `validation` will be splitted further into a validation and test sets.
        validation, test = split(
            validation,
            train_size=validation_size,
            random_state=rand_state_2,
            shuffle=shuffle_2,
            )

        return (
            train.reset_index(drop=True),
            validation.reset_index(drop=True),
            test.reset_index(drop=True),
        )


def print_proportions(data_sets: dict) -> pd.core.frame.DataFrame:

    if len(data_sets) == 1:
        data_sets = {'main': data_sets['train']}

    proportions = np.array([data_sets[key].shape[0] / data_sets['main'].shape[0] for key in data_sets]).round(4)
    rows_length = [data_sets[key].shape[0] for key in data_sets]

    proportions_ds = pd.DataFrame(
        {
            'Absolute': rows_length,
            'Proportion': proportions,
        },
        index=data_sets.keys()
    )

    return proportions_ds