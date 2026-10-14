dataset_name="change"
result_path="/home/jeongjw/selective-code-generation/result/exp/exp_dataset"
alpha=0.35
delta_s=0.1
epsilon_s=0.3
epsilon_e=0.05
eval_epsilon=0.01
calib_limit=50
eval_limit=150
add_epsilon=True
model_name="gpt-4o"

python /home/jeongjw/selective-code-generation/src/exp/exp_dataset.py \
    --model_name $model_name \
    --dataset_name $dataset_name \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e \
    --eval_epsilon $eval_epsilon \
    --calib_limit $calib_limit \
    --eval_limit $eval_limit \
    --add_epsilon $add_epsilon
