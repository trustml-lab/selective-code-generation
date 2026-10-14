import json
import os

from selective_code_generation.util.dataset_type import DatasetType
from selective_code_generation.util.code_type import CodeType

def organize_mbpp(path: str):
    solution_json_file_path = os.path.join(path, 'solutions.json')

    if not os.path.exists(solution_json_file_path):
        return
    
    with open(solution_json_file_path) as f:
        solutions = json.load(f)
    
    os.makedirs(os.path.join(path, 'modified_code_function'), exist_ok=True)

    with open(os.path.join(path, 'modified_code_function', 'modified_solution_0000.py'), 'w+') as f:
        f.write(solutions[0])


def organize_code_contests(path: str):
    solution_json_file_path = os.path.join(path, 'solutions.json')

    if not os.path.exists(solution_json_file_path):
        return

    with open(solution_json_file_path) as f:
        solutions_dict = json.load(f)

    os.makedirs(os.path.join(path, 'modified_code_function'), exist_ok=True)

    solution_idx = 0
    for idx, lang_type in enumerate(solutions_dict['language']):
        if lang_type == 3:
            solution_idx_str = f'{solution_idx:04d}'
            with open(os.path.join(path, 'modified_code_function', f'modified_solution_{solution_idx_str}.py'), 'w+') as f:
                f.write(solutions_dict['solution'][idx])

            solution_idx += 1

def organize_mercury(path: str):
    solution_json_file_path = os.path.join(path, 'solutions.json')

    if not os.path.exists(solution_json_file_path):
        return 
    
    with open(solution_json_file_path) as f:
        solutions_dict = json.load(f)
    
    os.makedirs(os.path.join(path, 'modified_code_function'), exist_ok=True)

    for solution_idx, solution in enumerate(solutions_dict):
        solution_idx_str = f'{solution_idx:04d}'
        with open(os.path.join(path, 'modified_code_function', f'modified_solution_{solution_idx_str}.py'), 'w+') as f:
            f.write(solution)

def organize_humaneval(path: str):
    solution_json_file_path = os.path.join(path, 'solutions.json')

    print(solution_json_file_path)

    if not os.path.exists(solution_json_file_path):
        return
    
    with open(solution_json_file_path) as f:
        solutions_dict = json.load(f)

    os.makedirs(os.path.join(path, 'modified_code_function'), exist_ok=True)

    for solution_idx, solution in enumerate(solutions_dict):
        solution_idx_str = f'{solution_idx:04d}'
        with open(os.path.join(path, 'modified_code_function', f'modified_solution_{solution_idx_str}.py'), 'w+') as f:
            f.write(solution)


def organize_sol_dir(dataset_type: DatasetType, code_type: CodeType, path: str):    
    if dataset_type == DatasetType.MBPP:
        organize_mbpp(path)
    elif dataset_type == DatasetType.CODE_CONTESTS:
        organize_code_contests(path)
    elif dataset_type == DatasetType.MERCURY:
        organize_mercury(path)
    elif dataset_type == DatasetType.HUMANEVAL:
        organize_humaneval(path)
    else:
        return
