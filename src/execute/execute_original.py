from selective_code_generation.util.dataset_type import DatasetType
from util import parse_args
from enum import Enum
from test_one_solution import check_correctness_single_test

import json
import os
import re

class CodeType(Enum):
    call = 1
    stdio = 2
    unknown =3

def extract_python_function_gemini(code:str):
    pattern = r"```python(.*?)```"    
    matches = re.findall(pattern, code, re.DOTALL)
    return [match.strip() for match in matches][0]

def extract_python_function_llama(code:str):
    pattern = r"\[PYTHON\](.*?)\[/PYTHON\]"   
    matches = re.findall(pattern, code, re.DOTALL)
    return [match.strip() for match in matches][0]

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
        with open(os.path.join(self.args.dataset_path, self.args.split_dir, self.args.problem_index, "fuzz.json")) as f:
            # print(os.path.join(self.args.dataset_path, self.args.split_dir, "fuzz.json"))
            self.loaded_test_cases = json.load(f)

    def extract_python_code(self, text):
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
    
    def load_generated_code(self):
        print(os.path.join(self.args.generated_data_path, self.args.split_dir, f'{self.args.problem_index}.json'))
        if not os.path.exists(os.path.join(self.args.generated_data_path, self.args.split_dir, f'{self.args.problem_index}.json')):
            raise Exception("123")

        with open(os.path.join(self.args.generated_data_path, self.args.split_dir, f'{self.args.problem_index}.json')) as f:
            dataset = json.load(f)
            # print(dataset)
            # self.generated_code = extract_python_function_gemini(dataset['generated_code'])
            self.generated_code = extract_python_function_llama(dataset['generated_code'])
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
        
        directory_path = f'/home/jeongjw/selective-code-generation/exec_result/original/codellama-13b-instruct/{self.args.split_dir}/{self.args.problem_index}'
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
        
        directory_path = f'/home/jeongjw/selective-code-generation/exec_result/original/codellama-13b-instruct/{self.args.split_dir}/{self.args.problem_index}'
        print(directory_path)
        os.makedirs(directory_path, exist_ok=True)
        
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
            # self.load_testcases()
            self.load_generated_code()
            fn_name = self.get_fn_name()
        except Exception as e:
            print(e)
            return

        # print(self.load_testcases)

        self.result = []
        self.tested_total = 0
        self.tested_correct = 0
        
        # for ele in self.loaded_test_cases:
        #    current_test_case = ele
        
        input_list = []
        output_list = []

        original_input_list = []
        original_output_list = []

        with open(os.path.join(self.args.dataset_path, self.args.split_dir, self.args.problem_index,"input_output.json")) as f:
            input_output = json.load(f)

        try:
            for (input_i, output_i) in zip(input_output['inputs'], input_output['outputs']):
                if self.codetype == CodeType.stdio:
                    if isinstance(input_i, list):
                        original_input_list.append('\n'.join(input_i))
                    else:
                        original_input_list.append(input_i)
                        
                    if isinstance(output_i, list):
                        original_output_list.append('\n'.join(output_i))
                    else:
                        original_output_list.append(output_i)
                elif self.codetype == CodeType.call:
                    original_input_list.append(input_i)
                    original_output_list.append(output_i)
        except Exception as e:
            print(e)
            return

        if self.codetype == CodeType.stdio:
            result = check_correctness_single_test(self.generated_code, 5, False, 
                                                dict(inputs=original_input_list, outputs=original_output_list))
        elif self.codetype == CodeType.call:
            result = check_correctness_single_test(self.generated_code, 5, False, 
                                                dict(inputs=original_input_list, outputs=original_output_list, fn_name=fn_name))
        
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

    execute = Execute(args)
    execute.execute()

if __name__ == "__main__":
    main()
