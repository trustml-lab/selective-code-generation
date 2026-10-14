#!/bin/bash

PYTHON_PATH="/home/jeongjw/selective-code-generation/src/dataset/verification/verify.py"

if [ "$#" -lt 4 ]; then 
    echo "USAGE: $0 DATASET_TYPE SPLIT_DIR BEGIN_INDEX END_INDEX" 
    exit 1
fi

dataset_type=$1
split_dir=$2
begin_index=$3
end_index=$4
solution_index=$5

python $PYTHON_PATH \
    --dataset_type $dataset_type \
    --begin_index $begin_index \
    --end_index $end_index \
    --split_dir $split_dir 
