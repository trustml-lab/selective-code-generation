from selective_code_generation.exp.alpha_entailment import alpha_entailment
from selective_code_generation.exp.argparse import ArgParser
from selective_code_generation.exp.calibrate import calibrate
from selective_code_generation.exp.index_split import *
from selective_code_generation.exp.calc_unit_test import calc_unit_test_number
from selective_code_generation.exp.util import *
from selective_code_generation.exp.test_fn import *
from tqdm import tqdm

import numpy as np
import json
import os

pass_k_number = 5

def save_result(
    result_path,
    alpha,
    delta_s,
    epsilon_s,
    epsilon_e,
    eval_epsilon,
    calib_limit,
    eval_limit,
    add_epsilon,
    model_name,
    dataset_name,
    fdr,
    eff,
    pass_1
):
    
    os.makedirs(result_path, exist_ok=True)
    data = {
        "fdr": fdr,
        "eff": eff,
        "pass_1": pass_1, 
        "fdr_mean": np.mean(fdr),
        "fdr_std": np.std(fdr),
        "eff_mean": np.mean(eff),
        "eff_std": np.std(eff),
        "pass_1_mean": np.mean(pass_1),
        "pass_1_std": np.std(pass_1)
    }

    file_name = f'result_{model_name}_{dataset_name}_alpha_{alpha}_del_s_{delta_s}_eps_s_{epsilon_s}_eps_e_{epsilon_e}_eps_eval_{eval_epsilon}_calib_lim_{calib_limit}_eval_lim_{eval_limit}_add_eps_{add_epsilon}.json'
    print(file_name)
    file_path =os.path.join(result_path, file_name)

    with open(file_path, 'w+') as f:
        f.seek(0)
        json.dump(data, f, indent=4)

    return


# calibration_list: find x (<= n_1) -> re sample x and determine
# eval_list: find y (<= n_2) -> re sample y and determine

# each element: scores, alpha-entail (alpha entail or not), split, index
# -> optional: whether the given code passes all the test cases
# --> test cases: give as a list (from the original dataset or sample from fuzz.json)

# 620 unit test result
# divide into n_1, n_1, n_2, n_2 samples

def exp(args):

    alpha = args.alpha
    delta_s = args.delta_s
    epsilon_s = args.epsilon_s
    epsilon_e = args.epsilon_e
    eval_epsilon = args.eval_epsilon
    calib_limit = args.calib_limit
    eval_limit = args.eval_limit
    add_epsilon = args.add_epsilon
    
    split_info = return_begin_end_index_split_lst(args.dataset_name)
    print(split_info)

    eval_list = []
    calibrate_list = []

    # debug purpose
    # split_info = [('train', 0, 0)]

    for split_elem in split_info:
        split = split_elem[0]
        begin_index = split_elem[1]
        end_index = split_elem[2]

        ignore_list_path = f"/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem/{args.dataset_name}_{split}.json"

        with open(ignore_list_path, 'r') as f:
            ignore_list = json.load(f)
        
        # change original
        split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution"
        split_path = os.path.join(split_basic_path, args.model_name, args.dataset_name, split)

        # Cpp 
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/language/Cpp"
        # split_path = os.path.join(split_basic_path, split)

        # Perl
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/language/Perl"
        # split_path = os.path.join(split_basic_path, split)

        # Java
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/language/Java"
        # split_path = os.path.join(split_basic_path, split)

        # Javascript
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/language/Javascript"
        # split_path = os.path.join(split_basic_path, split)

        # normalized_prob
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/normalized_prob"
        # split_path = os.path.join(split_basic_path, split)

        # seq_prob
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/seq_prob"
        # split_path = os.path.join(split_basic_path, split)

        # lowest_prob
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/lowest_prob"
        # split_path = os.path.join(split_basic_path, split)

        # verbalized_prob
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/verbalized_prob"
        # split_path = os.path.join(split_basic_path, split)

        # normalized_prob deepseek
        split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/scoring-function-deepseek/normalized_prob"
        split_path = os.path.join(split_basic_path, split)

        # seq_prob deepseek
        # split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution/scoring-function-deepseek/seq_prob"
        # split_path = os.path.join(split_basic_path, split)


        if args.exact_match and args.dataset_name != 'MBPP' and args.dataset_name != 'HUMANEVAL' and args.dataset_name != 'MERCURY':
            solution_idx_dict_path = f"/home/jeongjw/selective-code-generation/scripts/fuzz/solution_index/{args.dataset_name}_{split}.json"
            with open(solution_idx_dict_path, 'r') as f:
                solution_idx_dict = json.load(f)
        else:
            solution_idx_dict = {}


        for i in tqdm(range(begin_index, end_index + 1)):
            index_str = f'{i:04d}'
            problem_path = os.path.join(split_path, index_str)
            execution_result_path = os.path.join(problem_path, "execution_result.json")

            if i in ignore_list:
                continue

            if not os.path.exists(execution_result_path):
                continue

            with open(execution_result_path) as f:
                code_info = json.load(f)

            test_result_lst = code_info['test_result']

            if not args.exact_match:

                if 2*calib_limit + 2*eval_limit >= len(test_result_lst):
                    continue

                sample_number_calc_calib_test = test_result_lst[0: calib_limit]
                alpha_determine_calib_test = test_result_lst[calib_limit: 2*calib_limit] 

                sample_number_calc_eval_test = test_result_lst[2*calib_limit: 2*calib_limit + eval_limit]
                alpha_determine_eval_test = test_result_lst[2*calib_limit + eval_limit: 2*calib_limit + 2*eval_limit]

                pass_k_test = test_result_lst[2*calib_limit + 2*eval_limit: 2*calib_limit + 2*eval_limit + pass_k_number]
                
                if sum(pass_k_test) == pass_k_number:
                    pass_k_pass = True
                else:
                    pass_k_pass = False


                # calculate unit test number
                calibrate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    test_limit = calib_limit,
                    test_result_lst = sample_number_calc_calib_test,
                    debug = False
                )

                evaluate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = eval_epsilon,
                    test_limit = eval_limit,
                    test_result_lst = sample_number_calc_eval_test,
                    debug = False
                )
                

                # sample and determine alpha entailment (lower_bound > 1 - alpha)
                calibrate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = calibrate_unit_test_number,
                    test_result_lst = alpha_determine_calib_test,
                    debug = False
                )

                evaluate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = evaluate_unit_test_number,
                    test_result_lst = alpha_determine_eval_test,
                    debug = False
                )

                # add it to eval_list and calibration_list
                calibrate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": calibrate_alpha_equivalence,
                    "index": i,
                    "split": split,
                    "pass_k": pass_k_pass,
                    "tested_total": calibrate_unit_test_number, 
                    "tested_passed": sum(alpha_determine_calib_test[:calibrate_unit_test_number]) 
                }

                evaluate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": evaluate_alpha_equivalence,
                    "index": i,
                    "split": split,
                    "pass_k": pass_k_pass,
                    "tested_total": evaluate_unit_test_number, 
                    "tested_passed": sum(alpha_determine_eval_test[:evaluate_unit_test_number])
                }

            else:
                
                solution_path = f"/home/jeongjw/selective-code-generation/dataset/{args.dataset_name}/{split}/{index_str}/solutions.json"
                
                if args.dataset_name != 'MBPP' and args.dataset_name != 'HUMANEVAL' and args.dataset_name != 'MERCURY':
                    elem = [item for item in solution_idx_dict if item.get("index") == i][0]
                    solution_idx = elem['solution_idx']
                else:
                    solution_idx = 0

                with open(solution_path, 'r') as f:
                    solution_lst = json.load(f)

                pass_k_test = test_result_lst[: pass_k_number]
                
                if sum(pass_k_test) == pass_k_number:
                    pass_k_pass = True
                else:
                    pass_k_pass = False

                try:
                    canonical_solution = solution_lst[solution_idx]
                except:
                    continue

                if canonical_solution == code_info['code']:
                    equivalence = True
                else:
                    equivalence = False

                if 2*calib_limit + 2*eval_limit >= len(test_result_lst):
                    continue

                sample_number_calc_calib_test = test_result_lst[0: calib_limit]
                alpha_determine_calib_test = test_result_lst[calib_limit: 2*calib_limit] 

                sample_number_calc_eval_test = test_result_lst[2*calib_limit: 2*calib_limit + eval_limit]
                alpha_determine_eval_test = test_result_lst[2*calib_limit + eval_limit: 2*calib_limit + 2*eval_limit]

                pass_k_test = test_result_lst[2*calib_limit + 2*eval_limit: 2*calib_limit + 2*eval_limit + pass_k_number]
                
                if sum(pass_k_test) == pass_k_number:
                    pass_k_pass = True
                else:
                    pass_k_pass = False


                # calculate unit test number
                calibrate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    test_limit = calib_limit,
                    test_result_lst = sample_number_calc_calib_test,
                    debug = False
                )

                evaluate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = eval_epsilon,
                    test_limit = eval_limit,
                    test_result_lst = sample_number_calc_eval_test,
                    debug = False
                )
                

                # sample and determine alpha entailment (lower_bound > 1 - alpha)
                calibrate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = calibrate_unit_test_number,
                    test_result_lst = alpha_determine_calib_test,
                    debug = False
                )

                evaluate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = evaluate_unit_test_number,
                    test_result_lst = alpha_determine_eval_test,
                    debug = False
                )
                
                calibrate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": equivalence,
                    "index": i,
                    "split": split,
                    "pass_k": pass_k_pass, 
                    "alpha_equiv": calibrate_alpha_equivalence
                }

                evaluate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": equivalence,
                    "index": i,
                    "split": split, 
                    "pass_k": pass_k_pass,
                    "alpha_equiv": evaluate_alpha_equivalence
                }

            
            # print(calibrate_dict_elem)
            # print(evaluate_dict_elem)

            calibrate_list.append(calibrate_dict_elem)
            eval_list.append(evaluate_dict_elem)

    assert len(eval_list) == len(calibrate_list)

    fdr_lst = []
    eff_lst = []
    # only call pass_1 if necessary (running time)
    pass_1_lst = []

    
    # experiment code
    for _ in range(50):

        # split train and test set 
        train_list, test_list = random_split(calibrate_list, 0.8)
        # print(f'train_list len: {len(train_list)} test_list len: {len(test_list)}')


        if not args.manual_selection and not args.wo_selective:
            # calibrate and find tau_s
            tau_s = calibrate(
                calibrate_list = train_list,
                epsilon = epsilon_s,
                delta = delta_s,
                epsilon_e = epsilon_e,
                add_epsilon_s = add_epsilon,
                debug =False
            )

        elif args.manual_selection and not args.wo_selective:
            ds = sorted(train_list, key=lambda d: d['scores'])
            tau_s = ds[len(ds)//2]['scores']
        
        else:
            tau_s = -1000000000.0
        
        # extract evaluation list
        evaluate_test_list = extract_test_list(test_list, eval_list)


        # calculate fdr and efficiency 
        if not args.exact_match:
            fdr_elem, eff_elem = test_fn(evaluate_test_list, tau_s)
        else:
            fdr_elem, eff_elem = test_fn_em(evaluate_test_list, tau_s)


        # append fdr and efficiency
        fdr_lst.append(fdr_elem)
        eff_lst.append(eff_elem)
        

        pass_1_test_elem = test_pass_1(evaluate_test_list, tau_s)
        pass_1_lst.append(pass_1_test_elem)
    
    # save result
    save_result(
        result_path=args.result_path,
        alpha=alpha,
        delta_s=delta_s,
        epsilon_s=epsilon_s,
        epsilon_e=epsilon_e,
        eval_epsilon=eval_epsilon,
        calib_limit=calib_limit,
        eval_limit=eval_limit,
        add_epsilon=add_epsilon,
        model_name=args.model_name,
        dataset_name=args.dataset_name,
        fdr=fdr_lst,
        eff=eff_lst,
        pass_1=pass_1_lst
    )


    print(f'calibration: epsilon = {epsilon_s}, delta = {delta_s}')
    print(f'Test Set FDR {np.mean(fdr_lst)} ± {np.std(fdr_lst)}')
    print(f'Test Set Efficiency {np.mean(eff_lst)} ± {np.std(eff_lst)}')

# calibration_list: find x (<= n_1) -> re sample x and determine
# eval_list: find y (<= n_2) -> re sample y and determine

# each element: scores, alpha-entail (alpha entail or not), split, index
# -> optional: whether the given code passes all the test cases
# --> test cases: give as a list (from the original dataset or sample from fuzz.json)

# 620 unit test result
# divide into n_1, n_1, n_2, n_2 samples

def exp_qualitative(args):

    alpha = args.alpha
    delta_s = args.delta_s
    epsilon_s = args.epsilon_s
    epsilon_e = args.epsilon_e
    eval_epsilon = args.eval_epsilon
    calib_limit = args.calib_limit
    eval_limit = args.eval_limit
    add_epsilon = args.add_epsilon
    
    split_info = return_begin_end_index_split_lst(args.dataset_name)
    print(split_info)

    eval_list = []
    calibrate_list = []

    # debug purpose
    # split_info = [('train', 0, 0)]

    for split_elem in split_info:
        split = split_elem[0]
        begin_index = split_elem[1]
        end_index = split_elem[2]

        ignore_list_path = f"/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem/{args.dataset_name}_{split}.json"

        with open(ignore_list_path, 'r') as f:
            ignore_list = json.load(f)
        
        split_basic_path = f"/home/jeongjw/selective-code-generation/result/execution"
        split_path = os.path.join(split_basic_path, args.model_name, args.dataset_name, split)

        print(split_path)


        if args.exact_match and args.dataset_name != 'MBPP' and args.dataset_name != 'HUMANEVAL' and args.dataset_name != 'MERCURY':
            solution_idx_dict_path = f"/home/jeongjw/selective-code-generation/scripts/fuzz/solution_index/{args.dataset_name}_{split}.json"
            with open(solution_idx_dict_path, 'r') as f:
                solution_idx_dict = json.load(f)
        else:
            solution_idx_dict = {}


        for i in tqdm(range(begin_index, end_index + 1)):
            index_str = f'{i:04d}'
            problem_path = os.path.join(split_path, index_str)
            execution_result_path = os.path.join(problem_path, "execution_result.json")

            if i in ignore_list:
                continue

            if not os.path.exists(execution_result_path):
                continue

            with open(execution_result_path) as f:
                code_info = json.load(f)

            test_result_lst = code_info['test_result']

            if not args.exact_match:

                if 2*calib_limit + 2*eval_limit >= len(test_result_lst):
                    continue

                sample_number_calc_calib_test = test_result_lst[0: calib_limit]
                alpha_determine_calib_test = test_result_lst[calib_limit: 2*calib_limit] 

                sample_number_calc_eval_test = test_result_lst[2*calib_limit: 2*calib_limit + eval_limit]
                alpha_determine_eval_test = test_result_lst[2*calib_limit + eval_limit: 2*calib_limit + 2*eval_limit]

                pass_k_test = test_result_lst[2*calib_limit + 2*eval_limit: 2*calib_limit + 2*eval_limit + pass_k_number]
                
                if sum(pass_k_test) == pass_k_number:
                    pass_k_pass = True
                else:
                    pass_k_pass = False


                # calculate unit test number
                calibrate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    test_limit = calib_limit,
                    test_result_lst = sample_number_calc_calib_test,
                    debug = False
                )

                evaluate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = eval_epsilon,
                    test_limit = eval_limit,
                    test_result_lst = sample_number_calc_eval_test,
                    debug = False
                )
                

                # sample and determine alpha entailment (lower_bound > 1 - alpha)
                calibrate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = calibrate_unit_test_number,
                    test_result_lst = alpha_determine_calib_test,
                    debug = False
                )

                evaluate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = evaluate_unit_test_number,
                    test_result_lst = alpha_determine_eval_test,
                    debug = False
                )

                # add it to eval_list and calibration_list
                calibrate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": calibrate_alpha_equivalence,
                    "index": i,
                    "split": split,
                    "pass_k": pass_k_pass,
                    "tested_total": calibrate_unit_test_number, 
                    "tested_passed": sum(alpha_determine_calib_test[:calibrate_unit_test_number]),
                    "code": code_info['code']
                }

                evaluate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": evaluate_alpha_equivalence,
                    "index": i,
                    "split": split,
                    "pass_k": pass_k_pass,
                    "tested_total": evaluate_unit_test_number, 
                    "tested_passed": sum(alpha_determine_eval_test[:evaluate_unit_test_number]),
                    "code": code_info['code']
                }

            else:
                
                solution_path = f"/home/jeongjw/selective-code-generation/dataset/{args.dataset_name}/{split}/{index_str}/solutions.json"
                
                if args.dataset_name != 'MBPP' and args.dataset_name != 'HUMANEVAL' and args.dataset_name != 'MERCURY':
                    elem = [item for item in solution_idx_dict if item.get("index") == i][0]
                    solution_idx = elem['solution_idx']
                else:
                    solution_idx = 0

                with open(solution_path, 'r') as f:
                    solution_lst = json.load(f)

                pass_k_test = test_result_lst[: pass_k_number]
                
                if sum(pass_k_test) == pass_k_number:
                    pass_k_pass = True
                else:
                    pass_k_pass = False

                try:
                    canonical_solution = solution_lst[solution_idx]
                except:
                    continue

                if canonical_solution == code_info['code']:
                    equivalence = True
                else:
                    equivalence = False

                if 2*calib_limit + 2*eval_limit >= len(test_result_lst):
                    continue

                sample_number_calc_calib_test = test_result_lst[0: calib_limit]
                alpha_determine_calib_test = test_result_lst[calib_limit: 2*calib_limit] 

                sample_number_calc_eval_test = test_result_lst[2*calib_limit: 2*calib_limit + eval_limit]
                alpha_determine_eval_test = test_result_lst[2*calib_limit + eval_limit: 2*calib_limit + 2*eval_limit]

                pass_k_test = test_result_lst[2*calib_limit + 2*eval_limit: 2*calib_limit + 2*eval_limit + pass_k_number]
                
                if sum(pass_k_test) == pass_k_number:
                    pass_k_pass = True
                else:
                    pass_k_pass = False


                # calculate unit test number
                calibrate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    test_limit = calib_limit,
                    test_result_lst = sample_number_calc_calib_test,
                    debug = False
                )

                evaluate_unit_test_number = calc_unit_test_number(
                    alpha = alpha,
                    epsilon_e = eval_epsilon,
                    test_limit = eval_limit,
                    test_result_lst = sample_number_calc_eval_test,
                    debug = False
                )
                

                # sample and determine alpha entailment (lower_bound > 1 - alpha)
                calibrate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = calibrate_unit_test_number,
                    test_result_lst = alpha_determine_calib_test,
                    debug = False
                )

                evaluate_alpha_equivalence = alpha_entailment(
                    alpha = alpha,
                    epsilon_e = epsilon_e,
                    unit_test_number = evaluate_unit_test_number,
                    test_result_lst = alpha_determine_eval_test,
                    debug = False
                )
                
                calibrate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": equivalence,
                    "index": i,
                    "split": split,
                    "pass_k": pass_k_pass, 
                    "alpha_equiv": calibrate_alpha_equivalence,
                    "code": code_info['code']
                }

                evaluate_dict_elem = {
                    "scores": code_info['scores'],
                    "equiv": equivalence,
                    "index": i,
                    "split": split, 
                    "pass_k": pass_k_pass,
                    "alpha_equiv": evaluate_alpha_equivalence,
                    "code": code_info['code']
                }

            
            # print(calibrate_dict_elem)
            # print(evaluate_dict_elem)

            calibrate_list.append(calibrate_dict_elem)
            eval_list.append(evaluate_dict_elem)

    assert len(eval_list) == len(calibrate_list)

    fdr_lst = []
    eff_lst = []
    # only call pass_1 if necessary (running time)
    pass_1_lst = []

    
    # experiment code
    for _ in range(1):

        # split train and test set 
        train_list, test_list = random_split(calibrate_list, 0.8)
        # print(f'train_list len: {len(train_list)} test_list len: {len(test_list)}')


        if not args.manual_selection and not args.wo_selective:
            # calibrate and find tau_s
            tau_s = calibrate(
                calibrate_list = train_list,
                epsilon = epsilon_s,
                delta = delta_s,
                epsilon_e = epsilon_e,
                add_epsilon_s = add_epsilon,
                debug =False
            )

        elif args.manual_selection and not args.wo_selective:
            ds = sorted(train_list, key=lambda d: d['scores'])
            tau_s = ds[len(ds)//2]['scores']
        
        else:
            tau_s = -1000000000.0
        
        # extract evaluation list
        evaluate_test_list = extract_test_list(test_list, eval_list)


        # calculate fdr and efficiency 
        if not args.exact_match:
            fdr_elem, eff_elem = test_fn(evaluate_test_list, tau_s)
        else:
            fdr_elem, eff_elem = test_fn_em(evaluate_test_list, tau_s)


        # append fdr and efficiency
        fdr_lst.append(fdr_elem)
        eff_lst.append(eff_elem)
        

        pass_1_test_elem = test_pass_1(evaluate_test_list, tau_s)
        pass_1_lst.append(pass_1_test_elem)

    
    passed_test_list = []
    failed_test_list = []

    for ele in evaluate_test_list:
        if ele['scores'] >= tau_s:
            passed_test_list.append(ele)
        else:
            failed_test_list.append(ele)

    os.makedirs(args.result_path, exist_ok=True)
    dump_dict = {
        "tau_s": tau_s,
        "passed_test_list": passed_test_list,
        "failed_test_list": failed_test_list
    }

    with open(os.path.join(args.result_path, "qualitative.json"), 'w+') as f:
        json.dump(dump_dict, f, indent=4)

    print(f'calibration: epsilon = {epsilon_s}, delta = {delta_s}')
    print(f'Test Set FDR {np.mean(fdr_lst)} ± {np.std(fdr_lst)}')
    print(f'Test Set Efficiency {np.mean(eff_lst)} ± {np.std(eff_lst)}')


if __name__ == "__main__":
    argparser = ArgParser()
    args = argparser.parse_args()

    alpha = 0.3
    epsilon_e = 0.1
    test_limit = 100

    with open("/home/jeongjw/selective-code-generation/result/execution/gpt-4o/APPS/train/0000/execution_result.json", 'r') as f:
        test_lst = json.load(f)

    args.alpha = 0.35
    args.delta_s = 0.1
    args.epsilon_s = 0.3
    args.epsilon_e = 0.1
    args.eval_epsilon = 0.01
    args.calib_limit = 100
    args.eval_limit = 200
    args.add_epsilon = False
    args.dataset_name = 'APPS'
    args.model_name = 'gpt-4o'
    args.result_path="/home/jeongjw/selective-code-generation/result/exp/debug"
    exp(args)
