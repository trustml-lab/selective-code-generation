# model: gemini, codellama-13b-instruct, gpt-4o
model="deepseek-r1"
overleaf_push=false
result_path="/home/jeongjw/selective-code-generation/result"
alpha=0.05
delta_s=0.1
epsilon_s=0.2
epsilon_e=0.03

: '
python /home/jeongjw/selective-code-generation/src/exp/baseline_1.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e

python /home/jeongjw/selective-code-generation/src/exp/baseline_2.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e

python /home/jeongjw/selective-code-generation/src/exp/basic_1.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e

python /home/jeongjw/selective-code-generation/src/exp/basic_2.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e

python ../../exp/basic_3.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e

python ../../exp/basic_4.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e


python ../../exp/basic_5.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e
'

python /home/jeongjw/selective-code-generation/src/exp/plot.py \
    --model_name $model \
    --result_path $result_path \
    --alpha $alpha \
    --delta_s $delta_s \
    --epsilon_s $epsilon_s \
    --epsilon_e $epsilon_e

if $overleaf_push; then
    python ../../exp/overleaf.py
    echo "Overleaf push has been executed."
else
    echo "Overleaf push is set to false. Skipping overleaf.py execution."
fi
