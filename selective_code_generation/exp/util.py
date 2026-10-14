import random
import math
from scipy import stats

def extract_test_list(test_calibrate_sub_list, test_evaluate_full_list):
    info = {(item['index'], item['split']) for item in test_calibrate_sub_list}

    test_sublist = [item for item in test_evaluate_full_list if ((item['index'], item['split']) in info)]

    assert len(test_calibrate_sub_list) == len(test_sublist)
    return test_sublist

def random_split(lst, split_ratio):
    random.shuffle(lst)
    split_index= int(len(lst) * split_ratio)
    
    train = lst[:split_index]
    test = lst[split_index: ]
    
    return train, test

def clopper_pearson(k, n, alpha, two_side=False, use_R=False, lower_bound=False):
    if two_side:
        if use_R:
            lo = stats.qbeta(alpha/2, int(k), int(n-k+1))[0]
            hi = stats.qbeta(1 - alpha/2, int(k+1), int(n-k))[0]
        else:
            lo = stats.beta.ppf(alpha/2, k, n-k+1)
            hi = stats.beta.ppf(1 - alpha/2, k+1, n-k)
        
            lo = 0.0 if math.isnan(lo) else lo
            hi = 1.0 if math.isnan(hi) else hi
    
        return lo, hi
    else:
        if use_R:
            hi = stats.qbeta(1 - alpha, int(k+1), int(n-k))[0]
        else:
            if lower_bound:
                lo = stats.beta.ppf(alpha, k, n-k+1)
                lo = 0.0 if math.isnan(lo) else lo

                return lo
            else:
                hi = stats.beta.ppf(1 - alpha, k+1, n-k)
                hi = 1.0 if math.isnan(hi) else hi
    
                return hi
        return hi

