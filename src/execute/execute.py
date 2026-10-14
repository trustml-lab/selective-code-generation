from selective_code_generation.util.dataset_type import DatasetType
from util import parse_args
from enum import Enum
from test_one_solution import check_correctness_single_test

import json
import os
import re

def extract_gemini_code(text: str) -> str:
    pattern = r'```python\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def extract_codellama_code(text):
    """
    Extracts the Python code between [PYTHON] and [/PYTHON] tags.

    Parameters:
        text (str): The input string containing [PYTHON] and [/PYTHON] tags.

    Returns:
        str: Extracted Python code if tags are found, otherwise an empty string.
    """
    pattern = r'\[PYTHON\](.*?)\[/PYTHON\]'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

class CodeType(Enum):
    call = 1
    stdio = 2
    unknown =3

class Execute:
    def __init__(self, args):
        self.args = args
        self.result_test_cases = []
        self.loaded_test_cases = None
        self.result = []
        
        self.tested_total = 0
        self.tested_correct = 0
        
        self.index = 0
        
        self.codetype = CodeType.unknown
    
    
    def load_testcases(self):
        try:
            with open(os.path.join(self.args.dataset_path, self.args.split_dir, self.args.problem_index, "fuzz.json")) as f:
                # print(os.path.join(self.args.dataset_path, self.args.split_dir, "fuzz.json"))
                self.loaded_test_cases = json.load(f)
        except Exception as e:
            print(e)
        
    def load_generated_code(self):
        print(os.path.join(self.args.generated_data_path, self.args.split_dir, f'{self.args.problem_index}.json'))
        if not os.path.exists(os.path.join(self.args.generated_data_path, self.args.split_dir, f'{self.args.problem_index}.json')):
            raise Exception("123")

        with open(os.path.join(self.args.generated_data_path, self.args.split_dir, f'{self.args.problem_index}.json')) as f:
            dataset = json.load(f)
            # print(dataset)

            if self.args.model_type == "gemini":
                self.generated_code = extract_gemini_code(dataset['generated_code'])
            elif self.args.model_type == "codellama-13b-instruct":
                self.generated_code = extract_codellama_code(dataset['generated_code'])
            else:
                self.generated_code = dataset['generated_code']

            self.score = dataset['score']
            
        # print(self.generated_code)
        return
            
            
    def get_fn_name(self):
        try:
            with open(os.path.join(self.args.dataset_path, self.args.split_dir, self.args.problem_index,"input_output.json")) as f:
                input_output = json.load(f)
            fn_name = input_output.get('fn_name')
            
            if fn_name is not None:
                self.codetype = CodeType.call
            else:
                self.codetype = CodeType.stdio
            
            return fn_name
        except:
            return None 
            
    def save_to_json(self):
        name = "execution_result_detailed.json"
        
        directory_path = os.path.join(self.args.result_dir, self.args.model_type, self.args.dataset_type, self.args.split_dir, self.args.problem_index)
        print(directory_path) 
        os.makedirs(directory_path, exist_ok=True)
        
        with open(os.path.join(directory_path, name), 'w+') as f:
            entry = {
                "test_result": self.result,
                "code": self.generated_code, 
                "scores": self.score,
                "total_tested": self.tested_total,
                "total_passed": self.tested_correct,
                "test_cases": self.result_test_cases
            }
            json.dump(entry, f, indent=4, separators=(",", ": "))
            
        name = "execution_result.json"
        with open(os.path.join(directory_path, name), 'w+') as f:
            entry = {
                "test_result": self.result,
                "code": self.generated_code, 
                "scores": self.score,
                "total_tested": self.tested_total,
                "total_passed": self.tested_correct
            }
            json.dump(entry, f, indent=4, separators=(",", ": "))
            
    def execute(self):
        try:
            self.load_testcases()
            self.load_generated_code()
            fn_name = self.get_fn_name()
        except Exception as e:
            return

        # print(self.load_testcases)

        self.result = []
        self.tested_total = 0
        self.tested_correct = 0
        
        for ele in self.loaded_test_cases:
            current_test_case = ele
        
        input_list = []
        output_list = []
        for testcase in self.loaded_test_cases:
            if self.codetype == CodeType.stdio:
                input_list.append('\n'.join(testcase[0]))
                output_list.append(testcase[1])
            elif self.codetype == CodeType.call:
                input_list.append(testcase[0])
                output_list.append(testcase[1])

        # print(input_list[0])
        # print(output_list[0])
    
        try:
            if self.codetype == CodeType.stdio:
                result = check_correctness_single_test(self.generated_code, 30, False, 
                                                    dict(inputs=input_list, outputs=output_list))
            elif self.codetype == CodeType.call:
                result = check_correctness_single_test(self.generated_code, 30, False, 
                                                    dict(inputs=input_list, outputs=output_list, fn_name=fn_name))
        except Exception as e:
            result = [False]  * len(input_list)
        
        print(result)
        for ele in result[0]:
            self.tested_total += 1
            if ele == True:
                self.tested_correct += 1
                self.result.append(True)
            else:
                self.result.append(False)
        self.result_test_cases.append((input_list, output_list))
        
        self.save_to_json()
        return

def main():
    args = parse_args()

    with open(f'/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem/{args.dataset_type}_{args.split_dir}.json', 'r') as f:
        exclude_list = json.load(f)

    if int(args.problem_index) in exclude_list:
        return
 
    execute = Execute(args)
    execute.execute()

if __name__ == "__main__":
    main()
