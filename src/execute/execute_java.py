import subprocess
import os
import sys
import json
from typing import Tuple
from util import parse_args

def compile_java_code(
    java_code: str,
    class_name: str = "Main",
    target_dir: str = "sol",
    compile_timeout: float = 5.0,
    verbose: bool = False,
) -> Tuple[bool, str, str]:
    """
    Write `java_code` to <target_dir>/<class_name>.java and compile it with `javac`.

    Returns
    -------
    success : bool
        True if `javac` exited with code 0.
    stdout : str
        Anything printed to stdout by the compiler.
    stderr : str
        Anything printed to stderr by the compiler.
    """
    os.makedirs(target_dir, exist_ok=True)
    java_path = os.path.join(target_dir, f"{class_name}.java")

    with open(java_path, "w", encoding="utf-8") as f:
        f.write(java_code)

    result = subprocess.run(
        ["javac", "-encoding", "UTF-8", java_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=compile_timeout,
    )

    if verbose:
        print(f"[javac stdout]\n{result.stdout}")
        print(f"[javac stderr]\n{result.stderr}")

    return result.returncode == 0, result.stdout, result.stderr


def run_java_with_input(
    input_str: str,
    class_dir: str = "sol",
    main_class: str = "Main",
    timeout: float = 0.1,
    verbose: bool = False,
) -> Tuple[int, str, str]:
    """
    Run `java -cp <class_dir> <main_class>` with `input_str` on stdin.

    Returns
    -------
    returncode : int
        The JVM process exit code (‒1 if the process failed to start).
    stdout : str
        Text printed to stdout by the program.
    stderr : str
        Text printed to stderr by the program.
    """
    try:
        proc = subprocess.run(
            ["java", "-cp", class_dir, main_class],
            input=input_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        if verbose:
            print(f"[java run] {e}")
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

    java_file_path = os.path.join(args.dataset_path, args.split_dir, args.problem_index, 'main.java')

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
        with open(java_file_path, 'r', encoding="utf-8") as f:
            java_code = f.read()
        # print(cpp_code)
    except:
        return execution_result
    
    success, _, _ = compile_java_code(
        java_code=java_code,
        target_dir= os.path.join(args.dataset_path, args.split_dir, args.problem_index),
        verbose=False
    )

    if success:
        print("Java compile success")
    else:
        print("Java compile failed")
        return execution_result

    for (i, ele) in enumerate(input_output_lst):

        input = '\n'.join(ele[0])
        expected_output = ele[1]

        a, out, c = run_java_with_input(
            input_str= input, 
            class_dir = os.path.join(args.dataset_path, args.split_dir, args.problem_index),
            verbose=False
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
