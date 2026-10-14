# return (fdr, efficiency)
def test_fn(lst, tau):
    total_code = len(lst)

    selective_pass = 0
    selective_fail = 0
    
    positive_code = 0
    negative_code = 0
    
    for ele in lst:
        if ele['scores'] >= tau:
            selective_pass += 1

            if ele['equiv']:
                positive_code += 1
            else:
                negative_code += 1
        else:
            selective_fail += 1

    assert(selective_pass == (positive_code + negative_code))
    assert(total_code == (selective_pass + selective_fail))

    if selective_pass == 0:
        return 0, selective_pass/total_code
    return negative_code/selective_pass, selective_pass/total_code

def test_fn_em(lst, tau):
    total_code = len(lst)

    selective_pass = 0
    selective_fail = 0
    
    positive_code = 0
    negative_code = 0
    
    for ele in lst:
        if ele['scores'] >= tau:
            selective_pass += 1

            if ele['alpha_equiv']:
                positive_code += 1
            else:
                negative_code += 1
        else:
            selective_fail += 1

    assert(selective_pass == (positive_code + negative_code))
    assert(total_code == (selective_pass + selective_fail))

    if selective_pass == 0:
        return 0, selective_pass/total_code
    return negative_code/selective_pass, selective_pass/total_code


def extract_test_list(train_sublist, test_list):
    info = {(item['index'], item['split']) for item in train_sublist}

    test_sublist = [item for item in test_list if ((item['index'], item['split']) in info)]

    # assert(len(train_sublist) == len(test_sublist))
    return test_sublist


def test_pass_1(pass_k_lst, tau_s):

    total_tested = 0
    total_passed = 0

    for ele in pass_k_lst:
        if ele['scores'] >= tau_s:
            total_tested += 1

            if ele['pass_k']:
                total_passed += 1

    if total_tested == 0:
        return 0.0

    return total_passed/total_tested
