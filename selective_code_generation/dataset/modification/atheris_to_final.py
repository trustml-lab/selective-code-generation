import json
import os

class Transform:
    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
    
    def save_to_python_file(self, text):
        with open(self.path + f'/{self.file_name}', 'w+') as f:
            f.write(text)
    
    def modify_code(self, solution_index: int):
        with open(self.path + f'/modified_code_function_atheris/modified_solution_{solution_index:04d}.py') as f:
            self.code = f.read()
        
        if 'sys.stdout = old_stdout' in self.code:
            self.type = "std"
        else:
            self.type = "call"
        
        begin = False
        inTestOneInput = False
        temp_code = self.code.split("\n")
        final_code = ""
        for index, line in enumerate(temp_code):
            if "import" in line or "from" in temp_code:
                final_code += f"{line}\n"
                continue
            
            '''
            if not begin:
                begin = True
                final_code += "\nimport json"
                final_code += "\nfrom io import StringIO\nresult = []\nold_stdin = sys.stdin\nold_stdout = sys.stdout\n"
            '''
                
            final_code += f"{line}\n"
            
            
            if "atheris.FuzzedDataProvider" in line:
                # final_code += "    output_buffer = StringIO()\n    sys.stdout = output_buffer\n\n"
                # final_code += "    if len(result) >= 101:\n        sys.stdout = old_stdout\n        sys.exit(0)\n\n"
                # final_code += "    try:\n" 
                inTestOneInput = True
                continue
            
            if self.type == "std":
                if index + 2 < len(temp_code) and 'sys.stdout = old_stdout' in temp_code[index+1] and 'output_buffer.close()' in temp_code[index+2]:
                    inTestOneInput = False
                    final_code += f"    with open(f'{self.path}/temp_fuzz_{{sys.argv[2]}}.json', 'w+') as file:\n        try:\n"
                    final_code += "            data = json.load(file)\n        except json.JSONDecodeError:\n            data = []\n\n"
                    final_code += "        data.append(result)\n        file.seek(0)\n        json.dump(data, file, indent = 4)\n        file.truncate()\n\n"
            else:
                if index + 1 < len(temp_code) and 'def main():' in temp_code[index+1]:
                    inTestOneInput = False
                    final_code += f"    with open(f'{self.path}/temp_fuzz_{{sys.argv[2]}}.json', 'w+') as file:\n        try:\n"
                    final_code += "            data = json.load(file)\n        except json.JSONDecodeError:\n            data = []\n\n"
                    final_code += "        data.append(result)\n        file.seek(0)\n        json.dump(data, file, indent = 4)\n        file.truncate()\n\n"
        
        self.save_to_python_file("import json\n" + final_code)

def check_directory_exists(path):
    target_directory = "modified_code_function_atheris"

    full_path = os.path.join(path, target_directory)
    print(full_path)
    return os.path.isdir(full_path)

def atheris_to_final_mbpp(solution_index: int, path: str):
    if check_directory_exists(path):
        transform = Transform(path, "modified_fuzz.py")
        transform.modify_code(solution_index)

    else: 
        pass

def atheris_to_final_mercury(solution_index: int, path: str):
    if check_directory_exists(path):
        transform = Transform(path, "modified_fuzz.py")
        transform.modify_code(solution_index)

    else: 
        pass

def atheris_to_final_humaneval(solution_index: int, path: str):
    if check_directory_exists(path):
        transform = Transform(path, "modified_fuzz.py")
        transform.modify_code(solution_index)
    
    else:
        pass
