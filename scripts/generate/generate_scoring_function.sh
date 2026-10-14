#!/bin/bash

src_dir="/home/jeongjw/selective-code-generation/src"

if [ "$#" -lt 5 ]; then 
    echo "Usage $0 DATASET_TYPE SPLIT_DIR START_INDEX END_INDEX MODEL_TYPE" 
    exit 1
fi

dataset_type=$1
split_dir=$2
begin_index=$3
end_index=$4
model_type=$5

base_dir="/home/jeongjw/selective-code-generation/dataset/$dataset_type"
output_dir="/home/jeongjw/selective-code-generation/generated_data/scoring_function"

for i in $(seq -f "%04g" "$begin_index" "$end_index"); do

    CUDA_VISIBLE_DEVICES=3 python $src_dir/generate/generate_scoring_function.py \
    --dataset_type $dataset_type \
    --split_dir $split_dir \
    --index $i \
    --output $output_dir \
    --model_type $model_type \
    --base_dir $base_dir || true

done
