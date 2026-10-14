import json
import os
import re

class Transform:
    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name

    def generate_prompt(self, solution_code, problem, number_str):        
        prompt = f"""We want to fuzz the following code with Atheris library. Complete the try block in TestOneInput(data) function for fuzzing and return the entire code. Do not add additional explanation or comments.

import atheris
import sys
import json
from io import StringIO

result = []
old_stdin = sys.stdin
old_stdout = sys.stdout

{solution_code}

def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    output_buffer = StringIO()
    sys.stdout = output_buffer
    
    if len(result) >= 101:
        sys.stdout = old_stdout
        sys.exit(0)
        
    try:
        # complete the following part
        
        test(query)
        result.append((query, output_buffer.getvalue().strip() + \"\\n\"))
    except:
        pass
    
    with open(f'../APPS/test/{number_str}/temp_fuzz_{{sys.argv[2]}}.json', 'w+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        data.append(result)
        file.seek(0)
        json.dump(data, file, indent = 4)
        file.truncate()
    
    sys.stdout = old_stdout
    output_buffer.close()

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
    
        - For binary string, use following code. 
    raw_bytes = fdp.ConsumeBytes(n)
    binary_string = ''.join('0' if byte % 2 == 0 else '1' for byte in raw_bytes)
    if len(binary_string) < n: 
        return

    - For English lower case string, use following code.
    lowercase_string = ''.join(chr(fdp.ConsumeIntInRange(ord('a'), ord('z'))) for _ in range(n))
    
    - When we need distinct edges or coordinates, use following code.
    available_edges = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
        
    for _ in range(m):
        u, v = available_edges.pop(fdp.ConsumeIntInRange(0, len(available_edges) - 1))
        query.append(f"{{u}} {{v}}")
    
    - Use fdp.PickValueInList if the problem requires you to choose among string, integer.

    - If we need a string with constraint, use PickValueInList. Avoid using ConsumeUnicode, ConusmeUnicodeNoSurrogates, ConsumeString.

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
    
'''
def generate_stdio_prompt():
    argparser = ArgParser()
    args = argparser.parse_args()

    match = re.search(r'/(\d+)$', args.path)
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
        file_name = f"modified_solution_{args.solution_index:04d}.py"
        with open(args.path + '/modified_code_function_gpt/' + file_name) as f:
            solution_code = f.read()
        
        with open(args.path + '/question.txt') as f:
            question = f.read()
        
        with open(args.path + '/input_output.json') as f:
            input_output = json.load(f)

        transform = Transform(args.path, file_name)
        prompt = transform.generate_prompt(solution_code, question, number_str)
        transform.save_to_python_file(prompt, "prompt.txt")
    except Exception as e:
        print(e)
'''
