# model: gemini, codellama-13b-instruct, gpt-4o
model="deepseek-r1"
overleaf_push=false
result_path="/home/jeongjw/selective-code-generation/result"
alpha=0.1
delta_s=0.1
epsilon_s=0.2
epsilon_e=0.03


python /home/jeongjw/selective-code-generation/src/exp/basic_2_pass_fuzz.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e
