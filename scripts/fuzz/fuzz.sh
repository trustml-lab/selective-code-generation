#!/bin/bash

set -e

if [ "$#" -lt 4 ]; then 
    echo "Usage $0 DATASET_TYPE SPLIT_DIR START_INDEX END_INDEX" 
    exit 1
fi

seed_dir="/home/jeongjw/selective-code-generation/seed"
output_file="fuzz.json"
# seed_dir="/home/jeongjw/selective-code-generation/seed2"
# output_file="fuzz_random.json"
dataset_type=$1
split_dir=$2
begin_index=$3
end_index=$4

FILESIZE=3145728
MAX_JOBS=$(nproc)

exclude_problem_json_path="/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem/$1_$2.json"
exclude_problem_list=$(jq -r '.[]' "$exclude_problem_json_path")

case $dataset_type in 
    "CODE_CONTESTS") base_dir="/home/jeongjw/selective-code-generation/dataset/CODE_CONTESTS"
    ;;
    "APPS") base_dir="/home/jeongjw/selective-code-generation/dataset/APPS"
    ;;
    "MBPP") base_dir="/home/jeongjw/selective-code-generation/dataset/MBPP"
    ;;
    "MERCURY") base_dir="/home/jeongjw/selective-code-generation/dataset/MERCURY"
    ;;
    "HUMANEVAL") base_dir="/home/jeongjw/selective-code-generation/dataset/HUMANEVAL"
    ;;
    *) echo "WRONG DATASET_TYPE ARGUMENT"
    exit 1
    ;;
esac

cleanup() {
    echo "Caught Ctrl+C. Terminating all background processes..."
    pkill -P $$
    wait
    exit 1
}

trap cleanup SIGINT

process_problem() {
    current_dir="$base_dir/$1/$2"

    if [ -d "$current_dir" ]; then

        # echo "Generating Seed Directory for (Run #$3)"
        # random_seed_dir="$seed_dir/$1_$2_$3"
        # mkdir "$random_seed_dir"

        # echo "Generating Random Seed for (Run #$3)"
        # cat /dev/urandom | tr -dc '01' | head -c 8000 > "$random_seed_dir/random_seed"
        # for i in {1..5}; do
        #     dd if=/dev/urandom of=/home/jeongjw/selective-code-generation/seed2/$1_$2_$3/random_file_$i.bin bs=1M count=3 iflag=fullblock
        # done


        echo "Processing: $current_dir (Run #$3)"
        # python "$current_dir/modified_fuzz.py" "$random_seed_dir" "$3" || true
        python "$current_dir/modified_fuzz.py" "$seed_dir" "$3" || true
 
        RAND=$(shuf -i 0-100 -n 1)

        # temp_fuzz_$3.json 처리
        if [ -f "$current_dir/temp_fuzz_$3.json" ]; then 
            FUZZING_RESULT=$(cat "$current_dir/temp_fuzz_$3.json")
            if ! echo "$FUZZING_RESULT" | jq empty 2>/dev/null; then
                echo "Invalid JSON in temp_fuzz_$3.json. Skipping..."
                rm -f "$current_dir/temp_fuzz_$3.json"
                return
            fi
        else 
            echo "temp_fuzz_$3.json not found. Skipping..."
            FUZZING_RESULT="[]"
        fi

        # fuzz.json 처리
        LOCKFILE="$current_dir/fuzz.lock"
        exec 200>"$LOCKFILE"
        flock 200 || { echo "Failed to acquire lock for $current_dir/fuzz.json"; return; }

        if [ -f "$current_dir/fuzz.json" ]; then
            CUMULATIVE_FUZZED=$(cat "$current_dir/fuzz.json")
            if [ -z "$CUMULATIVE_FUZZED" ] || ! echo "$CUMULATIVE_FUZZED" | jq empty 2>/dev/null; then
                echo "fuzz.json is empty or invalid. Initializing as empty array."
                CUMULATIVE_FUZZED="[]"
            fi
        else
            echo "fuzz.json not found. Initializing as empty array."
            CUMULATIVE_FUZZED="[]"
        fi

        NEW_TEST_CASE=$(echo "$FUZZING_RESULT" | jq ".[0][$RAND]")
        if [ -z "$NEW_TEST_CASE" ] || [ "$NEW_TEST_CASE" = "null" ]; then
            echo "NEW_TEST_CASE is invalid or empty. Skipping..."
            flock -u 200
            return
        fi

        UPDATED_JSON=$(echo "$CUMULATIVE_FUZZED" | jq ". + [$NEW_TEST_CASE]" 2>/dev/null)
        if [ $? -ne 0 ]; then
            echo "Failed to merge JSON. Skipping..."
            flock -u 200
            return
        fi

        echo "$UPDATED_JSON" > "$current_dir/$output_file"
        echo "Updated fuzz.json successfully."

        flock -u 200
    fi
}

export -f process_problem
export base_dir

for i in $(seq -f "%04g" "$begin_index" "$end_index"); do

    if echo "$exclude_problem_list" | grep -q -w "$i"; then
        echo "Skipping problem $i as it is in the exclude list."
        continue
    fi 

    for j in $(seq 1 620); do
        while [ "$(jobs | wc -l)" -ge "$MAX_JOBS" ]; do
            sleep 0.1 
        done
        process_problem "$split_dir" "$i" "$j" &
    done
    
    wait 

    echo "Cleaning Up temp_fuzz*.json files for problem $i"

    current_dir="$base_dir/$split_dir/$i"

    if [ -d "$current_dir" ]; then 
        for file in "$current_dir/temp_fuzz"*.json; do 
            if [ -e "$file" ]; then 
                rm "$file"
                echo "Removed: $file"
            fi
        done
    fi

    rm -rf "/home/jeongjw/selective-code-generation/seed2/$2_$i"*

done

echo "Cleaning up temp_fuzz_*.json files..."
for dir in "${DIRECTORIES[@]}"; do
    for i in $(seq -f "%04g" "$begin_index" "$end_index"); do
        current_dir="$base_dir/$dir/$i"
        if [ -d "$current_dir" ]; then
            for file in "$current_dir/temp_fuzz_"*.json; do
                if [ -e "$file" ]; then
                    rm "$file"
                fi
            done
        fi
    done
done

patterns=("crash*" "slow-unit*" "oom-*")

for pattern in "${patterns[@]}"; do
    echo "Processing files matching pattern: $pattern"
    files=($pattern) 
    if [ ${#files[@]} -eq 0 ]; then
        echo "No files found for pattern: $pattern"
        continue
    fi
    for file in "${files[@]}"; do
        if [ -e "$file" ]; then
            rm "$file" && echo "$file has been deleted." || echo "Error deleting $file"
        else
            echo "File does not exist: $file"
        fi
    done
done
