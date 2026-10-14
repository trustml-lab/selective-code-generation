DATASET_PATH="/home/jeongjw/selective-code-generation/dataset"
PYTHON_LAYOUT_PATH="/home/jeongjw/selective-code-generation/src/dataset/dataset_layout.py"
PYTHON_ORG_PATH="/home/jeongjw/selective-code-generation/src/dataset/sol_directory.py"
DATASET_TYPE="HUMANEVAL"

python $PYTHON_LAYOUT_PATH \
    --path $DATASET_PATH \
    --dataset_type $DATASET_TYPE

python $PYTHON_ORG_PATH \
    --path $DATASET_PATH \
    --dataset_type $DATASET_TYPE
