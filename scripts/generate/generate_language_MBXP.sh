#!/bin/bash

src_dir="/home/jeongjw/selective-code-generation/src"

if [ "$#" -lt 3 ]; then 
    echo "Usage $0 SPLIT_DIR START_INDEX END_INDEX" 
    exit 1
fi

split_dir=$1
begin_index=$2
end_index=$3

output_dir="/home/jeongjw/selective-code-generation/generated_data"

for i in $(seq -f "%04g" "$begin_index" "$end_index"); do

    echo $i

    python $src_dir/generate/generate_lang_MBPP.py \
    --split_dir $split_dir \
    --index $i \
    --output $output_dir || true

done
