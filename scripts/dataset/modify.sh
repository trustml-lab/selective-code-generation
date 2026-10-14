#!/bin/bash

PYTHON_PATH="/home/jeongjw/selective-code-generation/src/dataset/modify.py"

if [ "$#" -lt 5 ]; then 
    echo "USAGE: $0 DATASET_TYPE SPLIT_DIR BEGIN_INDEX END_INDEX SOLUTION_INDEX" 
    exit 1
fi

dataset_type=$1
split_dir=$2
begin_index=$3
end_index=$4
solution_index=$5

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

python $PYTHON_PATH \
    --dataset_type $dataset_type \
    --path $base_dir \
    --begin_index $begin_index \
    --end_index $end_index \
    --solution_index $solution_index \
    --split_dir $split_dir    
