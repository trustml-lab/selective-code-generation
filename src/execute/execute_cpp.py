import subprocess
import os
import sys
import json
from typing import Tuple
from util import parse_args

def compile_cpp_code(
    cpp_code: str,
    source_name: str = "main",
    target_dir: str = "sol",
    compile_timeout: float = 5.0,
    verbose: bool = False
) -> Tuple[bool, str, str]:
    os.makedirs(target_dir, exist_ok=True)
    cpp_path = os.path.join(target_dir, f"{source_name}.cpp")
    with open(cpp_path, "w", encoding="utf-8") as f:
        f.write(cpp_code)

    exe_path = os.path.join(target_dir, source_name)
    result = subprocess.run(
        ["g++", "-std=c++17", "-O2", "-o", exe_path, cpp_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=compile_timeout
    )

    if verbose:
        print(f"[g++ stdout]\n{result.stdout}")
        print(f"[g++ stderr]\n{result.stderr}")

    return result.returncode == 0, result.stdout, result.stderr

def run_cpp_with_input(
    input_str: str,
    executable_dir: str = "sol",
    executable_name: str = "main",
    timeout: float = 0.01
) -> Tuple[int, str, str]:
    exe_path = os.path.join(executable_dir, executable_name)
    try:
        proc = subprocess.run(
            [exe_path],
            input=input_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
    except:
        return -1, -1, -1


    # print("=== stdout ===")
    # print(proc.stdout or "<no output>")
    # print("=== stderr ===")
    # print(proc.stderr or "<no error>")

    return proc.returncode, proc.stdout, proc.stderr

def main():
    exclude_file_path = os.path.join(
        "/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem",
        f'APPS_{args.split_dir}.json'
    )

    with open(exclude_file_path, 'r') as f:
        exclude_lst = json.load(f)
    
    if int(args.problem_index) in exclude_lst:
        sys.exit(0)

    cpp_file_path = os.path.join(args.dataset_path, args.split_dir, args.problem_index, 'main.cpp')

    input_output_path = os.path.join(
        '/home/jeongjw/selective-code-generation/dataset/APPS',
        args.split_dir,
        args.problem_index,
        'fuzz.json'
    )

    print(input_output_path)

    try:
        with open(input_output_path, 'r') as f:
            input_output_lst = json.load(f)
    except Exception as e:
        print(e)
        sys.exit(0)

    execution_result = [False] * len(input_output_lst)

    try:
        with open(cpp_file_path, 'r', encoding="utf-8") as f:
            cpp_code = f.read()
        # print(cpp_code)
    except:
        return execution_result
    
    success, _, _ = compile_cpp_code(
        cpp_code=cpp_code,
        target_dir= os.path.join(args.dataset_path, args.split_dir, args.problem_index),
        verbose=False
    )

    if success:
        print("C++ compile success")
    else:
        print("C++ compile failed")
        return execution_result

    for (i, ele) in enumerate(input_output_lst):

        input = '\n'.join(ele[0])
        expected_output = ele[1]

        a, out, c = run_cpp_with_input(
            input_str= input, 
            executable_dir = os.path.join(args.dataset_path, args.split_dir, args.problem_index)
        )

        if a == -1 and out == -1 and c == -1:
            continue

        if out == expected_output:
            execution_result[i] = True

    return execution_result

    # sample multi-test input (same as your Java example)
    # sample_input = (
    #     "4\n"
    #     "4\n"
    #     "0001\n1000\n0011\n0111\n"
    #     "3\n"
    #     "010\n101\n0\n"
    #     "2\n"
    #     "00000\n00001\n"
    #     "4\n"
    #     "01\n001\n0001\n00001\n"
    # )
    # run_cpp_with_input(
    #     input_str=sample_input,
    #     executable_dir="sol"
    # )

def save_result(execution_result):
    try:
        code_info_path = os.path.join(args.generated_data_path, args.split_dir, f'{args.problem_index}.json')

        with open(code_info_path, 'r') as f:
            code_info = json.load(f)
    
    except:
        sys.exit(0)

    code = code_info['generated_code']
    score = code_info['score']

    dump_dict = {
        "test_result": execution_result, 
        "code": code,
        "scores": score,
        "total_tested": len(execution_result),
        "total_passed": sum(execution_result)
    }

    save_dir_path = os.path.join(args.result_dir, args.split_dir, f'{args.problem_index}')
    os.makedirs(save_dir_path, exist_ok=True)
    execution_result_path =os.path.join(save_dir_path, 'execution_result.json')

    with open(execution_result_path, 'w+') as f:
        json.dump(dump_dict, f, indent=4)


if __name__ == "__main__":
    args = parse_args()
    execution_result = main()
    save_result(execution_result)
