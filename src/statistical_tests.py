from typing import Union

from scipy.stats import shapiro as shapiro_test
from scipy.stats import normaltest as dagostino_test 
from scipy.stats import kstest as kol_smir_test 
from scipy.stats import jarque_bera as jarque_bera_test

from pandas.api.types import is_numeric_dtype

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

import pandas as pd
import numpy as np

def normality_tests(residuals):

    normality_tests = {
        'Shapiro-Wilk': shapiro_test(residuals),
        "D'Agostino's": dagostino_test(residuals),
        'Kolmogorov-Smirnov': kol_smir_test(residuals, 'norm'),
        "Jarque-Bera": jarque_bera_test(residuals),
    }

    for key in normality_tests:
        stat = round(normality_tests[key][0], 4)
        p_value = round(normality_tests[key][1], 4)

        print(f"Test: {key}")
        print(f'    - Statistic: {stat}, p-value: {p_value}')

    return
