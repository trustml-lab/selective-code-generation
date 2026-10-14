import subprocess
import os
import sys
import json
from typing import Tuple
from util import parse_args

import os
import subprocess
from typing import Tuple


def compile_kotlin_code(
    kotlin_code: str,
    file_name: str = "Main",          # Main.kt  → class MainKt
    target_dir: str = "sol",
    compile_timeout: float = 5.0,
    verbose: bool = False,
) -> Tuple[bool, str, str]:
    """
    Write `kotlin_code` to <target_dir>/<file_name>.kt and compile it with kotlinc.

    By default the compiler emits .class files into <target_dir>.  If your file is
    Main.kt with a top-level `fun main(...)`, the entry class will be `MainKt`.
    """
    os.makedirs(target_dir, exist_ok=True)
    kt_path = os.path.join(target_dir, f"{file_name}.kt")

    with open(kt_path, "w", encoding="utf-8") as f:
        f.write(kotlin_code)

    # Compile: kotlinc <src> -d <target_dir>
    result = subprocess.run(
        ["kotlinc", kt_path, "-d", target_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=compile_timeout,
    )

    if verbose:
        print(f"[kotlinc stdout]\n{result.stdout}")
        print(f"[kotlinc stderr]\n{result.stderr}")

    return result.returncode == 0, result.stdout, result.stderr


def run_kotlin_with_input(
    input_str: str,
    class_dir: str = "sol",
    main_class: str = "MainKt",       # change if your entry class differs
    timeout: float = 0.3,
    verbose: bool = False,
) -> Tuple[int, str, str]:
    """
    Run the compiled Kotlin program using the JVM.

    Kotlin ≥1.3 ships a small launcher, so we can invoke:
        kotlin -cp <class_dir> <main_class>
    which is equivalent to:
        java -classpath <class_dir>:<kotlin-stdlib> <main_class>
    """
    try:
        proc = subprocess.run(
            ["kotlin", "-cp", class_dir, main_class],
            input=input_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr

    except Exception as e:
        if verbose:
            print(f"[kotlin run] {e}")
        # (-1, "", "") keeps the return types consistent
        return -1, -1, -1

def main():
    exclude_file_path = os.path.join(
        "/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem",
        f'APPS_{args.split_dir}.json'
    )

    with open(exclude_file_path, 'r') as f:
        exclude_lst = json.load(f)
    
    if int(args.problem_index) in exclude_lst:
        sys.exit(0)

    kt_file_path = os.path.join(args.dataset_path, args.split_dir, args.problem_index, 'main.kt')

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
        with open(kt_file_path, 'r', encoding="utf-8") as f:
            kt_code = f.read()
        # print(cpp_code)
    except:
        return execution_result
    
    success, _, _ = compile_kotlin_code(
        kotlin_code=kt_code,
        target_dir= os.path.join(args.dataset_path, args.split_dir, args.problem_index),
        verbose=False
    )

    if success:
        print("Kotlin compile success")
    else:
        print("Kotlin compile failed")
        return execution_result

    for (i, ele) in enumerate(input_output_lst):

        input = '\n'.join(ele[0])
        expected_output = ele[1]

        a, out, c = run_kotlin_with_input(
            input_str= input, 
            class_dir = os.path.join(args.dataset_path, args.split_dir, args.problem_index)
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
