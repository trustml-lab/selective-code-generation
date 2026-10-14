# fn_to_atheris function
from dotenv import load_dotenv, find_dotenv

import json
import openai
import os
import re

class Transform:
    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name

    def extract_python_code(self, text):
        match = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip() 
        return None

    def extract_function_name(self, assert_statement: str) -> str:
        match = re.search(r'assert\s+(\w+)\(', assert_statement)
        if match:
            return match.group(1).strip()
        return None

    def generate_prompt(self, solution_code, fn_name, problem):
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

def main():
    atheris.Setup(sys.argv[:2], TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()

The inputs of the function should satisfy the problem requirements. 
Note: Use following code snippet if necessary.
    - query parameter should be argument vector type and be called as function_name(*query)

    - When completing code, use ConsumeBytes, ConsumeIntInRange, ConsumeFloat, PickValueInList, ConsumeBool only. 

    - For string input, use PickValueInList function.

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
    lowercase_string = ''.join(chr(fdp.ConsumeIntInRange(ord('a'), ord('z'))) for _ in range(n)))
    
    - If we have to select from certain character, use fdp.PickValueInList([])
    
    - Do not use random library, rather use ConsumeIntInRange. 

{problem}

        """
        return prompt
    
    def save_to_python_file(self, text, file_name):
        # with open(os.path.dirname(self.path) + f'//{file_name}', 'w') as f:
        with open(os.path.join(self.path, file_name), 'w+') as f:
            f.write(text)

    def generate_modified_code_gpt(self, solution_code, fn_name, question):
        prompt = self.generate_prompt(solution_code, fn_name, question)

        _ = load_dotenv(find_dotenv('/home/jeongjw/selective-code-generation/src/.env'))
        openai.api_key = os.environ['OPENAI_API_KEY']

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens = 10000
            )

            self.modified_code = self.extract_python_code(response.choices[0].message.content)

            self.save_to_python_file(self.modified_code, self.file_name)
        
        except Exception as e:
            print(e)
        
        return

def fn_to_atheris_mbpp(solution_index: int, path: str):
    try:
        file_name = f'modified_solution_{solution_index:04d}.py'
        
        with open(os.path.join(path, 'question.txt')) as f:
            question = f.read()

        with open(os.path.join(path, 'modified_code_function', file_name)) as f:
            solution_code = f.read()

        with open(os.path.join(path, 'test.json')) as f:
            test_code_lst = json.load(f)
        
        try:
            os.makedirs(os.path.join(path, 'modified_code_function_atheris'), exist_ok=True)
            transform = Transform(os.path.join(path, 'modified_code_function_atheris'), file_name)
            fn_name = transform.extract_function_name(test_code_lst[0])
            transform.generate_modified_code_gpt(solution_code, fn_name, question)

        except Exception as e:
            print(e)
    
    except:
        pass

def extract_function_name_mercury(code_str):
    match = re.search(r'def\s+(\w+)\s*\(', code_str)
    if match:
        return match.group(1)
    return None

def fn_to_atheris_mercury(solution_index: int, path: str):
    try:
        file_name = f'modified_solution_{solution_index:04d}.py'
        
        with open(os.path.join(path, 'question.txt')) as f:
            question = f.read()

        with open(os.path.join(path, 'modified_code_function', file_name)) as f:
            solution_code = f.read()

        try:
            os.makedirs(os.path.join(path, 'modified_code_function_atheris'), exist_ok=True)
            transform = Transform(os.path.join(path, 'modified_code_function_atheris'), file_name)
            fn_name = extract_function_name_mercury(solution_code[0])
            transform.generate_modified_code_gpt(solution_code, fn_name, question)

        except Exception as e:
            print(e)
    
    except:
        pass

def fn_to_atheris_humaneval(solution_index: int, path: str):
    try:
        file_name = f'modified_solution_{solution_index:04d}.py'
        
        with open(os.path.join(path, 'question.txt')) as f:
            question = f.read()

        with open(os.path.join(path, 'modified_code_function', file_name)) as f:
            solution_code = f.read()

        try:
            os.makedirs(os.path.join(path, 'modified_code_function_atheris'), exist_ok=True)
            transform = Transform(os.path.join(path, 'modified_code_function_atheris'), file_name)
            fn_name = extract_function_name_mercury(solution_code[0])
            transform.generate_modified_code_gpt(solution_code, fn_name, question)

        except Exception as e:
            print(e)
    
    except:
        pass
