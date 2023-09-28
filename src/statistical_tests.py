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

def normality_tests(residuals: pd.core.series.Series) -> pd.core.frame.DataFrame:
    
    normality_tests = pd.DataFrame(
        {
            'Statistic': [
                shapiro_test(residuals)[0],
                dagostino_test(residuals)[0],
                kol_smir_test(residuals, 'norm')[0],
                jarque_bera_test(residuals)[0],
            ],
            'p-value': [
                shapiro_test(residuals)[1],
                dagostino_test(residuals)[1],
                kol_smir_test(residuals, 'norm')[1],
                jarque_bera_test(residuals)[1],
            ],
        },
        index = ['Shapiro-Wilk', "D'Agostino's", 'Kolmogorov-Smirnov', "Jarque-Bera"],  
    )
    
    normality_tests.index.name = 'test'

    return normality_tests.round(4)
