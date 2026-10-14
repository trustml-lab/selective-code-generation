from enum import Enum
from selective_code_generation.execution.test_one_solution import *
from util.arg_parse import ArgParserVerify
import json
import os
import sys
import io
from tqdm import tqdm

class CodeType(Enum):
    call = 1
    stdio = 2
    unknown = 3

def extract_fn_name_and_type(problem_path):
    try:
        inout_path = os.path.join(problem_path, "input_output.json")
        with open(inout_path) as f:
            input_output = json.load(f)
        
        fn_name = input_output.get('fn_name')
        if fn_name is not None:
            return fn_name, CodeType.call
    except:
        pass
    
    return None, CodeType.stdio

def test():

    # open exclude list 
    exclude_file_path = f"/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem/{args.dataset_type}_{args.split_dir}.json"
    with open(exclude_file_path, 'r') as f:
        exclude_problems = json.load(f)

    # open fuzz index list
    solution_index_file_path = f"/home/jeongjw/selective-code-generation/scripts/fuzz/solution_index/{args.dataset_type}_{args.split_dir}.json"
    with open(solution_index_file_path, 'r') as f:
        fuzz_solution_index = json.load(f)

    for i in tqdm(range(args.begin_index, args.end_index + 1)):
        
        append = False
        try:
            elem = [item for item in fuzz_solution_index if item.get("index") == i][0]
            append = False
            append_dic = {"path": None, "solution_idx": None, 'len': None, 'ratio': None, 'message': None}
        except:
            append = True
            append_dic['path'] = problem_path
            append_dic['solution_idx'] = -1
            append_dic['len'] = 0
            append_dic['ratio'] = -1

        try:
            if i in exclude_problems:
                continue

            problem_path = os.path.join(split_path, f'{i:04d}')

            if os.path.isdir(problem_path):
                fuzzed_result_path = os.path.join(problem_path, "fuzz.json")
                solution_path = os.path.join(problem_path, "solutions.json")

                fn_name, ctype = extract_fn_name_and_type(problem_path)

                with open(fuzzed_result_path) as f:
                    fuzzed_result = json.load(f)

                with open(solution_path) as f:
                    solutions_lst = json.load(f)
                
                solution_code = solutions_lst[elem['solution_idx']].replace("from fractions import gcd", "from math import gcd")
                solution_code = solution_code.replace("stdout.write", "print")
                solution_code = solution_code.replace("fractions.gcd", "math.gcd")
                solution_code = "import math\nimport collections\nimport heapq\n" + solution_code

                if not append:
                    input_list = []
                    output_list = []
                    for testcase in fuzzed_result:
                        if ctype == CodeType.stdio:
                            input_list.append('\n'.join(testcase[0]))
                            output_list.append(testcase[1])
                        elif ctype == CodeType.call:
                            input_list.append(testcase[0])
                            output_list.append(testcase[1])
                    
                    if ctype == CodeType.stdio:
                        result = check_correctness_single_test(solution_code, 300, True, dict(inputs=input_list, outputs=output_list))
                    elif ctype == CodeType.call:
                        result = check_correctness_single_test(solution_code, 300, True, dict(inputs=input_list, outputs=output_list, fn_name=fn_name))                   

                    # if result[1] != 1.0:
                    append_dic['path'] = problem_path
                    append_dic['solution_idx'] = elem['solution_idx']
                    append_dic['len'] = len(result[0])
                    append_dic['ratio'] = result[1]
                
                if append_dic['ratio'] != 1.0: 
                    append = True
                
                if append_dic['ratio'] != 1.0:
                    append_dic['message'] = "Ratio not 1.0!!!!!!"
                else:
                    append_dic['message'] = "Ratio is 1.0"

        except Exception as e:
            append = True
            append_dic['path'] = problem_path
            append_dic['message'] = e
            
        if append:
            verification_path = os.path.join(args.result_path, f'{args.dataset_type}_{args.split_dir}.json')

            if os.path.exists(verification_path):
                with open(verification_path, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            existing_data.append(append_dic)

            with open(verification_path, 'w') as f:
                json.dump(existing_data, f, indent=4, default=str)



if __name__ == "__main__":
    argparser = ArgParserVerify()
    args = argparser.parse_args()

    if args.dataset_type == "APPS":
        base_path = "/home/jeongjw/selective-code-generation/dataset/APPS"
    elif args.dataset_type == "HUMANEVAL":
        base_path = "/home/jeongjw/selective-code-generation/dataset/HUMANEVAL"
    elif args.dataset_type == "MBPP":
        base_path = "/home/jeongjw/selective-code-generation/dataset/MBPP"
    elif args.dataset_type == "MERCURY":
        base_path = "/home/jeongjw/selective-code-generation/dataset/MERCURY"

    split_path = os.path.join(base_path, args.split_dir)
    os.makedirs(args.result_path, exist_ok=True)

    test()
