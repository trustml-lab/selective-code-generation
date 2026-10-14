import json

from .util import clopper_pearson

# algorithm 1
def calc_unit_test_number(alpha, epsilon_e, test_limit, test_result_lst, debug=False):

    assert test_limit == len(test_result_lst)

    unit_test_number = 0
    tested_total = 0
    passed_total = 0

    for ele in test_result_lst:

        unit_test_number += 1
        tested_total += 1
        
        if ele:
            passed_total+= 1
        
        lower_bound = clopper_pearson(
            passed_total, 
            tested_total, 
            epsilon_e, 
            two_side=False, 
            use_R = False,
            lower_bound = True
        )

        if debug:
            print(f'total: {tested_total} passed: {passed_total} lower_bound: {lower_bound}')

        if lower_bound > (1 - alpha):
            break

        if tested_total >= test_limit:
            unit_test_number = test_limit

    return unit_test_number
