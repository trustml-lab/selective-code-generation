#!/usr/bin/env python3

# Usage
# sys.argv[1]: DATASET_TYPE, sys.argv[2]: SPLIT_DIR, sys.argv[3]: START_INDEX, sys.argv[4]:END_INDEX

import glob
import json
import multiprocessing 
import os
import random
import subprocess
import sys
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

start_time = time.time()

seed_dir = "/home/jeongjw/selective-code-generation/seed"
output_file = "fuzz.json"

dataset_type = sys.argv[1]
split_dir = sys.argv[2]
begin_index = int(sys.argv[3])
end_index = int(sys.argv[4])

exclude_problem_json_path = f"/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem/{dataset_type}_{split_dir}.json"

with open(exclude_problem_json_path, 'r') as f:
    exclude_problem_list = json.load(f)


if dataset_type == "CODE_CONTESTS":
    base_dir = "/home/jeongjw/selective-code-generation/dataset/CODE_CONTESTS"
elif dataset_type == "APPS":
    base_dir="/home/jeongjw/selective-code-generation/dataset/APPS"
elif dataset_type == "MBPP":
    base_dir="/home/jeongjw/selective-code-generation/dataset/MBPP"
elif dataset_type == "MERCURY":
    base_dir="/home/jeongjw/selective-code-generation/dataset/MERCURY"
elif dataset_type == "HUMANEVAL":
    base_dir="/home/jeongjw/selective-code-generation/dataset/HUMANEVAL"
else:
    print("WRONG DATASET TYPE ARGUMENT")
    sys.exit(1)


def process_problem(problem_id, run_id, base_dir, split_dir, seed_dir, output_file):
    current_dir = os.path.join(base_dir, split_dir, problem_id)

    if not os.path.isdir(current_dir):
        return 
    
    print(f"Processing: {current_dir} (Run #{run_id})")

    fuzz_python_path = os.path.join(current_dir, "modified_fuzz.py")

    try:
        subprocess.run(["python3", fuzz_python_path, seed_dir, str(run_id)])
    except Exception as e:
        print(f"Error running fuzz script: {e}")


max_jobs = multiprocessing.cpu_count()
print(max_jobs)

with ThreadPoolExecutor(max_workers=max_jobs) as executor:
    for i in range(begin_index, end_index + 1):
        pid = str(i).zfill(4)

        if i in exclude_problem_list:
            print(f"Skipping problem {pid} as it is in the exclude list")
            continue
    
        futures = [executor.submit(
            process_problem, pid, j, base_dir, split_dir, seed_dir, output_file
        ) for j in range(1, 621)]

        for _ in as_completed(futures):
            pass

        current_dir = os.path.join(base_dir, split_dir, pid)

        final_result = []

        for run_id in range(1, 621):
            rand = random.randint(0, 100)
            temp_file = os.path.join(current_dir, f"temp_fuzz_{run_id}.json")

            if not os.path.isfile(temp_file):
                print("temp_fuzz file not found. Skipping...")
                continue
            
            try:
                with open(temp_file, 'r') as f:
                    fuzz_res = json.load(f)
            except Exception as e:
                print("Invalid JSON in temp_fuzz file. Removing and skipping...")
                # os.remove(temp_file)
                continue

            try:
                os.remove(temp_file)
            except Exception as e:
                pass
            
            final_result.append(fuzz_res[0][rand])

        final_file_path = os.path.join(current_dir, output_file)
        with open(final_file_path, 'w+') as f:
            json.dump(final_result, f, indent=4)

patterns = ["crash*", "slow-unit*", "oom-*"]
for pattern in patterns:
    print(f"Processing files matching pattern: {pattern}")
    files = glob.glob(pattern)
    if not files:
        print(f"No files found for pattern: {pattern}")
        continue
    for file in files:
        try:
            os.remove(file)
            print(f"{file} has been deleted.")
        except Exception:
            print(f"Error deleting {file}")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time} seconds")
