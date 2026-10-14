import os
import json

from util import parse_args
from tqdm import tqdm

def main():

    args.datset_type = "APPS"

    base_dir = f"/home/jeongjw/selective-code-generation/generated_data/{args.dataset_type}/gpt-4o"
    raw_data_path = os.path.join(base_dir, "raw", args.split_dir)

    begin_ind = 0
    end_ind = 4999

    target_word = "python"

    for i in tqdm(range(begin_ind, end_ind + 1)):
        try:
            index_str = f'{i:04d}'

            code_raw_path = os.path.join(raw_data_path, f'{index_str}.json')

            if not os.path.exists(code_raw_path): 
                continue

            with open(code_raw_path, 'r') as f:
                data = json.load(f)
            
            log_prob_score = 0
            total_count = 0
            iterator = 0

            # assert(data['choices'][0]['logprobs']['content'][0]['token'] == '```')
            # assert(data['choices'][0]['logprobs']['content'][1]['token'] == 'python')
            #assert(data['choices'][0]['logprobs']['content'][ data['usage']['completion_tokens'] - 1]['token'] == '`\n' 
            #       or data['choices'][0]['logprobs']['content'][ data['usage']['completion_tokens'] - 1]['token'] == '```'
            #       or data['choices'][0]['logprobs']['content'][ data['usage']['completion_tokens'] - 1]['token'] == '\n')
            
            completion = data['choices'][0]['message']['content']
            # print(completion)

            begin_code_token = -1
            end_code_token = -1

            
            for j in range(data['usage']['completion_tokens']):
                token = data['choices'][0]['logprobs']['content'][j]['token']
                # print(f'token: {token}')
                    
                if '``' in token:
                    if begin_code_token == -1:
                        begin_code_token = j
                    else:
                        end_code_token = j
                        break

            if f'```{target_word}' not in completion:
                continue

            # trimmed_code = completion[completion.find("```python\n") + len("```python\n"):completion.find("```")]
            parts = completion.split(f"```{target_word}", 1)
            trimmed_code = parts[1].split("```", 1)[0].strip()

            if trimmed_code == None or trimmed_code == "":
                continue

            iterator = data['usage']['completion_tokens']

            log_prob_lst = []
            total_cnt = 0
            log_prob_score = 0
            for index in range(3, end_code_token):    
                # print(f"{data['choices'][0]['logprobs']['content'][index]['token']}: {log_prob_score}")
                total_cnt += 1
                log_prob_lst.append(data['choices'][0]['logprobs']['content'][index]['logprob'])

                log_prob_score += data['choices'][0]['logprobs']['content'][index]['logprob']


            dump_data = {"score": sum(log_prob_lst), "generated_code": trimmed_code}

            original_execution_info_path = os.path.join(
                f"/home/jeongjw/selective-code-generation/result/execution/gpt-4o/APPS/{args.split_dir}",
                index_str,
                "execution_result.json"
            )

            with open(original_execution_info_path, 'r') as f:
                original_execution_info = json.load(f)
            
            original_execution_info['scores'] = sum(log_prob_lst)
            # print(original_execution_info)

            os.makedirs(f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/seq_prob/{args.split_dir}/{index_str}", exist_ok=True)
            with open (f"/home/jeongjw/selective-code-generation/result/execution/scoring-function/seq_prob/{args.split_dir}/{index_str}/execution_result.json", 'w+') as f:
                json.dump(original_execution_info, f, ensure_ascii=False, indent = 4)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    args = parse_args()
    main()
