#!/bin/bash

src_dir="/home/jeongjw/selective-code-generation/src/"

if [ "$#" -lt 2 ]; then 
    echo "Usage $0 DATASET_TYPE SPLIT_DIR" 
    exit 1
fi

dataset_type=$1
split_dir=$2

python "$src_dir/generate/process_seqprob.py" \
    --dataset_type $dataset_type \
    --split_dir $split_dir
