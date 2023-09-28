from typing import Union

def unfold_dictionary(original: dict, keys: Union[list, tuple]) -> dict:
    '''It checks if the original dictionary has all the keys as in `keys`;
    if not, it adds the missing keys with None values.
    '''

    only_nones = {key: None for key in keys if key not in original.keys()}
    full = {**original, **only_nones}

    return full