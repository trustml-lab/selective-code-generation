import openai
import os
import json
import re

from util import parse_args
from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv('/home/jeongjw/selective-code-generation/src/.env'))
openai.api_key = os.environ['OPENAI_API_KEY']


def parse_float(text: str) -> float:
    m = re.search(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', text)
    if not m:
        raise ValueError
    return float(m.group())

def main():

    args.datset_type = "APPS"

    base_dir = f"/home/jeongjw/selective-code-generation/generated_data/{args.dataset_type}/gpt-4o"
    raw_data_path = os.path.join(base_dir, "raw", args.split_dir)

    begin_ind = args.begin_index
    end_ind = args.end_index

    target_word = "python"

    for i in tqdm(range(begin_ind, end_ind + 1)):
        try:
            index_str = f'{i:04d}'

            original_execution_info_path = os.path.join(
                f"/home/jeongjw/selective-code-generation/result/execution/gpt-4o/APPS/{args.split_dir}",
                index_str,
                "execution_result.json"
            )

            with open(original_execution_info_path, 'r') as f:
                original_execution_info = json.load(f)
            
            code = original_execution_info['code']
            prompt = "We have the following python code implementing a method." + code + "What is a well-calibrated percent probability that this code passes the test cases?" + "(Answer with only a single float between 0.0 and 1.0)" + "Probability:"

            # print(original_execution_info)

            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                logprobs=True,
                max_tokens = 6000
            )

            try:
                original_execution_info['scores'] = float(response.choices[0].message.content)
            except:
                try: 
                    original_execution_info['scores'] = parse_float(response.choices[0].message.content)
                except:
                    continue
            
            print(original_execution_info['scores'])
            os.makedirs(f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/verbalized_prob/{args.split_dir}/{index_str}", exist_ok=True)
            with open (f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/verbalized_prob/{args.split_dir}/{index_str}/execution_result.json", 'w+') as f:
                json.dump(original_execution_info, f, ensure_ascii=False, indent = 4)


        except Exception as e:
            print(e)


if __name__ == "__main__":
    args = parse_args()
    main()
