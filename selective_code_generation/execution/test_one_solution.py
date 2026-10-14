"""
Run solutions from one problem.
code from https://github.com/hendrycks/apps/blob/main/eval/test_one_solution.py
"""
import json
import numpy as np
import os
import pprint
import multiprocessing
import time

from typing import Dict
from .testing_util import run_test, run_single_test

def check_correctness(problem, generation, timeout, debug):
    def _temp_run(problem, generation, debug, result):
        try:
            problem["solutions"] = json.loads(problem["solutions"])
            problem["input_output"] = json.loads(problem["input_output"])
            
            result.append(run_test(problem=problem, test=generation, debug=debug))
            if debug:
                print(f"Test completed with result: {result}")
        except Exception as e:
            if debug:
                print(f"Error in _temp_run: {e}")

    manager = multiprocessing.Manager()
    result = manager.list()
    p = multiprocessing.Process(target=_temp_run, args=(problem, generation, debug, result))
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        if debug:
            print(f"Process is still alive. Killing the process.")
        p.kill()
    if not result:
        avg_number_tests = 21
        result = [[-1] * avg_number_tests]
        if debug:
            print(f"Global timeout occurred, returning default result.")
    if debug:
        print(f"Final result: {result}")

    passed_tests = sum(1 for result in result[0] if result == True)
    total_tests = len(result[0])
    if total_tests==0:
        return result[0], 0.0
    return result[0], passed_tests/total_tests

def check_correctness_single_test(generation, timeout, debug, test_case):
    def _temp_run(generation, debug, result, test_case):
        try:            
            result.append(run_single_test(test=generation, debug=debug, test_case=test_case))
            if debug:
                print(f"Test completed with result: {result}")
        except Exception as e:
            if debug:
                print(f"Error in _temp_run: {e}")

    manager = multiprocessing.Manager()
    result = manager.list()
    p = multiprocessing.Process(target=_temp_run, args=(generation, debug, result, test_case))
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        if debug:
            print(f"Process is still alive. Killing the process.")
        p.kill()
    if not result:
        avg_number_tests = len(test_case['inputs'])
        result = [[-1] * avg_number_tests]
        if debug:
            print(f"Global timeout occurred, returning default result.")
    if debug:
        print(f"Final result: {result}")

    passed_tests = sum(1 for result in result[0] if result == True)
    total_tests = len(result[0])
    if total_tests==0:
        return result[0], 0.0
    return result[0], passed_tests/total_tests
