import json
import os

from datasets import load_dataset
from tqdm import tqdm

# path: where to place the dataset
def format_mbpp(path: str):
    split_lst = ['train', 'test', 'validation', 'prompt']

    ds = load_dataset("google-research-datasets/mbpp", "full")

    os.makedirs(os.path.join(path, "MBPP"), exist_ok=True)

    for split in split_lst:
        split_dir = os.path.join(path, "MBPP", split)
        os.makedirs(split_dir, exist_ok=True)

        problem_lst = ds[split]

        for problem in tqdm(problem_lst):
            problem_id = problem['task_id']
            problem_id_str = f'{problem_id:04d}'
            problem_dir = os.path.join(split_dir, problem_id_str)

            os.makedirs(problem_dir, exist_ok=True)

            question_file_path = os.path.join(problem_dir, 'question.txt')
            with open(question_file_path, 'w+') as f:
                f.write(problem['text'])

            solution_lst = [problem['code']]

            solutions_file_path = os.path.join(problem_dir, "solutions.json")
            
            with open(solutions_file_path, 'w+') as f:
                json.dump(solution_lst, f)
            
            test_code_lst = problem['test_list']
            test_code_path = os.path.join(problem_dir, "test.json")

            with open(test_code_path, 'w+') as f:
                json.dump(test_code_lst, f)
            

def format_code_contests(path: str):
    split_lst = ['train', 'valid', 'test']

    ds = load_dataset("deepmind/code_contests")
    os.makedirs(os.path.join(path, "CODE_CONTESTS"), exist_ok=True)

    for split in split_lst:
        split_dir = os.path.join(path, "CODE_CONTESTS", split)
        os.makedirs(split_dir, exist_ok=True)

        problem_lst = ds[split]

        # problem_id (index) is not specified for code_contests 
        problem_id = 0
        for problem in tqdm(problem_lst):

            problem_id_str = f'{problem_id:04d}'
            problem_dir = os.path.join(split_dir, problem_id_str)
            
            os.makedirs(problem_dir, exist_ok=True)

            question_file_path = os.path.join(problem_dir, 'question.txt')
            with open(question_file_path, 'w+') as f:
                f.write(problem['description'])

            solution_dict = problem['solutions']
            solutions_file_path = os.path.join(problem_dir, "solutions.json")

            with open(solutions_file_path, 'w+') as f:
                json.dump(solution_dict, f)

            problem_id += 1

def format_mercury(path: str):
    split_lst = ['train', 'eval']

    ds = load_dataset("Elfsong/Mercury")
    os.makedirs(os.path.join(path, "MERCURY"), exist_ok=True)

    for split in split_lst:
        split_dir = os.path.join(path, "MERCURY", split)
        os.makedirs(split_dir, exist_ok=True)

        problem_lst = ds[split]

        problem_id = 0

        for problem in tqdm(problem_lst):

            problem_id_str = f'{problem_id:04d}'
            problem_dir = os.path.join(split_dir, problem_id_str)

            os.makedirs(problem_dir, exist_ok=True)

            question_file_path = os.path.join(problem_dir, 'question.txt')

            try:
                with open(question_file_path, 'w+') as f:
                    f.write(problem['pretty_content'][0])
            except:
                print(f"Error on problem {problem_id}")

            solutions_list = problem['solutions']
            solution_json = []

            for solution_dict in solutions_list:
                solution_json.append(solution_dict['solution'])
            
            solutions_file_path = os.path.join(problem_dir, "solutions.json")
            with open(solutions_file_path, 'w+') as f:
                json.dump(solution_json, f)
            
            problem_id += 1

# path: where to place the dataset
def format_humaneval(path: str):
    split_lst = ['test']

    ds = load_dataset("openai/openai_humaneval")

    os.makedirs(os.path.join(path, "HUMANEVAL"), exist_ok=True)

    for split in split_lst:
        split_dir = os.path.join(path, "HUMANEVAL", split)
        os.makedirs(split_dir, exist_ok=True)

        problem_lst = ds[split]

        for problem in tqdm(problem_lst):
            problem_id_str = problem['task_id']
            problem_dir = os.path.join(split_dir, problem_id_str)

            print(problem_dir)

            os.makedirs(problem_dir, exist_ok=True)

            question_file_path = os.path.join(problem_dir, 'question.txt')
            with open(question_file_path, 'w+') as f:
                f.write(problem['prompt'])

            solution_lst = [problem['prompt'] + problem['canonical_solution']]

            solutions_file_path = os.path.join(problem_dir, "solutions.json")
            
            with open(solutions_file_path, 'w+') as f:
                json.dump(solution_lst, f)
            
            test_code_lst = problem['test']
            test_code_path = os.path.join(problem_dir, "test.json")

            with open(test_code_path, 'w+') as f:
                json.dump(test_code_lst, f)
