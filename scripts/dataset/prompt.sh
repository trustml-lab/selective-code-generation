DATASET_PATH="/home/jeongjw/selective-code-generation/dataset"
PYTHON_PROMPT_PATH="/home/jeongjw/selective-code-generation/src/dataset/generate_prompt.py"
DATASET_TYPE="MBPP"

python $PYTHON_PROMPT_PATH \
    --path $DATASET_PATH \
    --dataset_type $DATASET_TYPE
