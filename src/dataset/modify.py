from selective_code_generation.dataset.modification.fn_to_atheris import fn_to_atheris_mbpp, fn_to_atheris_mercury, fn_to_atheris_humaneval
from selective_code_generation.dataset.modification.atheris_to_final import atheris_to_final_mbpp, atheris_to_final_mercury, atheris_to_final_humaneval
from selective_code_generation.util.dataset_type import DatasetType
from tqdm import tqdm
from util import parse_args

import openai
import os
import re

def modify_mbpp(args):
    split_dir_path = os.path.join(args.path, args.split_dir)
    
    for i in tqdm(range(args.begin_index, args.end_index + 1)):
        problem_index_str = f"{i:04d}"
        problem_path = os.path.join(split_dir_path, problem_index_str)
        fn_to_atheris_mbpp(args.solution_index, problem_path)
        atheris_to_final_mbpp(args.solution_index, problem_path)

def modify_mercury(args):
    split_dir_path = os.path.join(args.path, args.split_dir)

    for i in tqdm(range(args.begin_index, args.end_index + 1)):
        problem_index_str = f"{i:04d}"
        problem_path = os.path.join(split_dir_path, problem_index_str)
        fn_to_atheris_mercury(args.solution_index, problem_path)
        atheris_to_final_mercury(args.solution_index, problem_path)

def modify_humaneval(args):
    split_dir_path = os.path.join(args.path, args.split_dir)

    for i in tqdm(range(args.begin_index, args.end_index + 1)):
        problem_index_str = str(i)

        problem_path = os.path.join(split_dir_path, "HumanEval", problem_index_str)
        fn_to_atheris_humaneval(0, problem_path)
        atheris_to_final_humaneval(0, problem_path)

def modify_code_contests(args):
    pass

# apps: mixed between stdio and fn
# mbpp: all fn methods  
# code_contests: all stdio methods
def main():
    args = parse_args()

    # fn: modified_code_function_atheris fn_to_atheris.py -> atheris_to_final.py 
    # stdio: modified_code_function_atheris stdio_to_func.py -> func_to_atheris.py -> atheris_to_final.py

    if args.dataset_type == DatasetType.MBPP:
        modify_mbpp(args)
    elif args.dataset_type == DatasetType.CODE_CONTESTS:
        modify_code_contests(args)
    elif args.dataset_type == DatasetType.MERCURY:
        modify_mercury(args)
    elif args.dataset_type == DatasetType.HUMANEVAL:
        modify_humaneval(args)
    else:
        pass

if __name__ == "__main__":
    main()
