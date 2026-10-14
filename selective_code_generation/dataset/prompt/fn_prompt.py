import json
import os
import re

class Transform:
    def __init__(self, path, file_name, solution_index = 0):
        self.path = path
        self.file_name = file_name
        self.solution_index = solution_index

    def extract_function_name(self, assert_statement: str) -> str:
        match = re.search(r'assert\s+(\w+)\(', assert_statement)
        return match.group(1) if match else None

    def generate_prompt_apps(self, solution_code, fn_name, problem, number):
        call_code = ""
        if "class Solution" in solution_code:
            call_code = f"ret_val = Solution().{fn_name}(*query)"
        else:
            call_code = f"ret_val = {fn_name}(*query)"
        
        prompt = f"""We want to fuzz the following code with Atheris library. Complete the try block in TestOneInput(data) function for fuzzing and return the entire code. Do not add additional explanation or comments.

import atheris
import sys
import json
import time
from itertools import accumulate, product, permutations, combinations
from collections import Counter, OrderedDict, deque, defaultdict, ChainMap
from functools import lru_cache
from math import sqrt, sin, cos, tan, ceil, fabs, floor, gcd, exp, log, log2
import fractions
from typing import List, Tuple
import numpy as np
import random
from heapq import *
result = []

{solution_code}

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    if len(result) >= 101:
        sys.exit(0)
        
    try:
        # complete the following part
        
        {call_code}
        result.append((query, ret_val))
    except:
        pass
    
    with open(f'../APPS/train/{number_str}/temp_fuzz_{{sys.argv[2]}}.json', 'w+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        data.append(result)
        file.seek(0)
        json.dump(data, file, indent = 4)
        file.truncate()

def main():
    atheris.Setup(sys.argv[:2], TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
    
Note: Use following code snippet if necessary.
    - For pemutation, use following code snippet.
    available_values = list(range(1, n + 1))
    permutation = []

    for _ in range(n):
        index = fdp.ConsumeIntInRange(0, len(available_values) - 1) 
        permutation.append(available_values.pop(index))
    
    - For binary string, use following code snippet. 
    raw_bytes = fdp.ConsumeBytes(n)
    binary_string = ''.join('0' if byte % 2 == 0 else '1' for byte in raw_bytes)
    if len(binary_string) < n:
        return

    - For English lower case string, use following code snippet.
    lowercase_string = ''.join(chr(fdp.ConsumeIntInRange(ord('a'), ord('z'))) for _ in range(n))

The inputs of the function should satisfy the problem requirements. 

{problem}

        """
        return prompt

    def generate_prompt_no_fn_name_apps(self, solution_code, problem, number):
        call_code = "# Call function and save return value to ret_val"
        if "class Solution" in solution_code:
            call_code = f"# ret_val = Solution(). function_name (*query)"
        else:
            call_code = f"# ret_val = function_name (*query)"
        
        prompt = f"""We want to fuzz the following code with Atheris library. Complete the try block in TestOneInput(data) function for fuzzing and return the entire code. Do not add additional explanation or comments.

import atheris
import sys
import json
import time
from itertools import accumulate, product, permutations, combinations
from collections import Counter, OrderedDict, deque, defaultdict, ChainMap
from functools import lru_cache
from math import sqrt, sin, cos, tan, ceil, fabs, floor, gcd, exp, log, log2
import fractions
from typing import List, Tuple
import numpy as np
import random
from heapq import *
result = []

{solution_code}

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    if len(result) >= 101:
        sys.exit(0)
        
    try:
        # complete the following part
        
        # Call function and save return value to ret_val
        {call_code}
        result.append((query, ret_val))
    except:
        pass
    
    with open(f'../APPS/train/{number_str}/temp_fuzz_{{sys.argv[2]}}.json', 'w+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        data.append(result)
        file.seek(0)
        json.dump(data, file, indent = 4)
        file.truncate()

def main():
    atheris.Setup(sys.argv[:2], TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
    
Note: Use following code snippet if necessary.
    - For pemutation, use following code snippet.
    available_values = list(range(1, n + 1))
    permutation = []

    for _ in range(n):
        index = fdp.ConsumeIntInRange(0, len(available_values) - 1) 
        permutation.append(available_values.pop(index))
    
    - For binary string, use following code snippet. 
    raw_bytes = fdp.ConsumeBytes(n)
    binary_string = ''.join('0' if byte % 2 == 0 else '1' for byte in raw_bytes)
    if len(binary_string) < n:
        return

    - For English lower case string, use following code snippet.
    lowercase_string = ''.join(chr(fdp.ConsumeIntInRange(ord('a'), ord('z'))) for _ in range(n))

The inputs of the function should satisfy the problem requirements. 

{problem}

        """
        return prompt

    def generate_prompt_mbpp(self, dataset_path, solution_code, problem, func_name, split, number_str):
        call_code = "# Call function and save return value to ret_val"
        call_code = f"# ret_val = {func_name}(*query)"
        
        prompt = f"""We want to fuzz the following code with Atheris library. Complete the try block in TestOneInput(data) function for fuzzing and return the entire code. Do not add additional explanation or comments.

import atheris
import sys
import json
import time
from itertools import accumulate, product, permutations, combinations
from collections import Counter, OrderedDict, deque, defaultdict, ChainMap
from functools import lru_cache
from math import sqrt, sin, cos, tan, ceil, fabs, floor, gcd, exp, log, log2
import fractions
from typing import List, Tuple
import numpy as np
import random
from heapq import *
result = []

{solution_code}

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    if len(result) >= 101:
        sys.exit(0)
        
    try:
        # complete the following part
        
        # Call function and save return value to ret_val
        {call_code}
        result.append((query, ret_val))
    except:
        pass
    
    with open(f'{dataset_path}/MBPP/{split}/{number_str}/temp_fuzz_{{sys.argv[2]}}.json', 'w+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        data.append(result)
        file.seek(0)
        json.dump(data, file, indent = 4)
        file.truncate()

def main():
    atheris.Setup(sys.argv[:2], TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
    
Note: Use following code snippet if necessary.
    - For pemutation, use following code snippet.
    available_values = list(range(1, n + 1))
    permutation = []

    for _ in range(n):
        index = fdp.ConsumeIntInRange(0, len(available_values) - 1) 
        permutation.append(available_values.pop(index))
    
    - For binary string, use following code snippet. 
    raw_bytes = fdp.ConsumeBytes(n)
    binary_string = ''.join('0' if byte % 2 == 0 else '1' for byte in raw_bytes)
    if len(binary_string) < n:
        return

    - For English lower case string, use following code snippet.
    lowercase_string = ''.join(chr(fdp.ConsumeIntInRange(ord('a'), ord('z'))) for _ in range(n))

The inputs of the function should satisfy the problem requirements. 

{problem}

        """
        return prompt
    
    def save_to_python_file(self, text, file_name):
        with open(self.path + f'//{file_name}', 'w') as f:
            f.write(text)
    
    def extract_python_code(self, text):
        match = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip() 
        return None
    
def generate_fn_prompt(path, solution_index):
    match = re.search(r'/(\d+)$', path)
    if match:
        number = int(match.group(1)) 
    else:
        pass
    
    if number < 10000:
        number_str = f'{number:04d}'
    else:
        number_str = f'{number:05d}'

    try:
        # solution file
        file_name = f"modified_solution_{solution_index:04d}.py"
        with open(path + '/modified_code_function/' + file_name) as f:
            solution_code = f.read()
            
        with open(path + '/question.txt') as f:
            question = f.read()
        
        try:
            with open(path + '/input_output.json') as f:
                input_output = json.load(f)

            if input_output.get('fn_name') is not None:
                transform = Transform(path, file_name)
                prompt = transform.generate_prompt(solution_code, input_output.get('fn_name'), question, number_str)
                transform.save_to_python_file(prompt, "prompt.txt")
        except Exception as e:
            transform = Transform(path, file_name)
            prompt = transform.generate_prompt_no_fn_name(solution_code, question, number_str)
            transform.save_to_python_file(prompt, "prompt.txt")
        
    except Exception as e:
        pass

def generate_prompt_MBPP(path: str, solution_index: int = 0):
    dataset_path = os.path.join(path, "MBPP")

    split_lst = ['train', 'test', 'validation', 'prompt']

    for split in split_lst:
        split_dir_path = os.path.join(dataset_path, split)

        sub_prob_dir_lst = os.listdir(split_dir_path)

        for directory in sub_prob_dir_lst:
            
            prob_dir_path = os.path.join(split_dir_path, directory)

            problem_path = os.path.join(prob_dir_path, 'question.txt')
            with open(problem_path, 'r') as f:
                problem = f.read()

            solution_path = os.path.join(prob_dir_path, 'modified_code_function', f'modified_solution_{solution_index:04d}.py')
            with open(solution_path, 'r') as f:
                solution = f.read()

            test_path = os.path.join(prob_dir_path, 'test.json')
            with open(test_path, 'r') as f:
                test_list = json.load(f)

            match = re.search(r'/(\d+)$', prob_dir_path)
            if match:
                number = int(match.group(1)) 
            else:
                number = -1
            print(number)

            if number < 10000:
                number_str = f'{number:04d}'
            else:
                number_str = f'{number:05d}'

            transform = Transform(prob_dir_path, solution_index)
            func_name = transform.extract_function_name(test_list[0])
            prompt = transform.generate_prompt_mbpp(dataset_path=path, solution_code=solution, problem=problem, func_name=func_name, split=split, number_str=number_str)
            transform.save_to_python_file(prompt, "prompt.txt")
