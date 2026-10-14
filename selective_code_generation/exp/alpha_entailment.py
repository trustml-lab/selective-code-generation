import json
import math
import random

from scipy import stats
from .util import clopper_pearson

def alpha_entailment(alpha, epsilon_e, unit_test_number, test_result_lst, debug = False):
    
    assert len(test_result_lst) >= unit_test_number

    test_lst = test_result_lst[:unit_test_number]
    
    passed_total = sum(test_lst)
    tested_total = unit_test_number

    if debug:
        print(f'total: {tested_total} passed: {passed_total}')

    lower_bound = clopper_pearson(
        passed_total,
        tested_total,
        epsilon_e, 
        two_side=False,
        use_R=False,
        lower_bound=True
    )

    if debug:
        print(f'lower bound: {lower_bound}')

    if lower_bound > (1 - alpha):
        return True
    else:
        return False
