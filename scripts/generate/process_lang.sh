#!/bin/bash

src_dir="/home/jeongjw/selective-code-generation/src/"

if [ "$#" -lt 3 ]; then 
    echo "Usage $0 DATASET_TYPE SPLIT_DIR LANGUAGE" 
    exit 1
fi

dataset_type=$1
split_dir=$2
language=$3

python "$src_dir/generate/process_lang_APPS.py" \
    --dataset_type "$dataset_type" \
    --split_dir "$split_dir" \
    --language "$langauge" 