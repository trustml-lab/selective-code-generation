import os
import json

from util import parse_args

def main():

    base_dir = f"/home/jeongjw/selective-code-generation/generated_data/{args.dataset_type}/gpt-4o"
    raw_data_path = os.path.join(base_dir, "raw", args.split_dir)

    begin_ind = 0

    if args.dataset_type == "APPS":
        end_ind = 4999
        target_word = "python"
    elif args.dataset_type =="HUMANEVAL":
        end_ind = 163
        target_word = "python"
    elif args.dataset_type == "MERCURY":
        if args.split_dir == "train":
            end_ind = 1632
        elif args.split_dir == "eval":
            end_ind = 255
        target_word = "python"
    elif args.dataset_type == "MBPP":
        begin_ind = 1
        end_ind = 974
        target_word = "python"
    elif args.dataset_type == "MBCPP":
        begin_ind = 1
        end_ind = 974
        target_word = "cpp"
    elif args.dataset_type == "MBCSP":
        begin_ind = 1
        end_ind = 974
        target_word = "csharp"
        # target_word = "sharp"
    elif args.dataset_type == "MBGP":
        begin_ind = 1
        end_ind = 974
        target_word = "go"
    elif args.dataset_type == "MBJP":
        begin_ind = 1
        end_ind = 974
        target_word = "java"
    elif args.dataset_type == "MBJSP":
        begin_ind = 1
        end_ind = 974
        target_word = "javascript"
    elif args.dataset_type == "MBKP":
        begin_ind = 1
        end_ind = 974
        # target_word = "otlin"
        target_word = "kotlin"
    elif args.dataset_type == "MBPHP":
        begin_ind = 1
        end_ind = 974
        target_word = "php"
    elif args.dataset_type == "MBPLP":
        begin_ind = 1
        end_ind = 974
        target_word = "perl"
    elif args.dataset_type == "MBRBP":
        begin_ind = 1
        end_ind = 974
        target_word = "ruby"
    elif args.dataset_type == "MBSCP":
        begin_ind = 1
        end_ind = 974
        target_word = "scala"
    elif args.dataset_type == "MBSWP":
        begin_ind = 1
        end_ind = 974
        target_word = "swift"
    elif args.dataset_type == "MBTSP":
        begin_ind = 1
        end_ind = 974
        target_word = "javascript"  

    for i in range(begin_ind, end_ind + 1):
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

            for index in range(begin_code_token, end_code_token):    
                # print(f"{data['choices'][0]['logprobs']['content'][index]['token']}: {log_prob_score}")
                log_prob_score += data['choices'][0]['logprobs']['content'][index]['logprob']
                total_count += 1

            dump_data = {"score": log_prob_score/total_count, "generated_code": trimmed_code}

            os.makedirs(f"/home/jeongjw/selective-code-generation/generated_data/{args.dataset_type}/gpt-4o/{args.split_dir}", exist_ok=True)
            with open (f"/home/jeongjw/selective-code-generation/generated_data/{args.dataset_type}/gpt-4o/{args.split_dir}/{index_str}.json", 'w+') as f:
                json.dump(dump_data, f, ensure_ascii=False, indent = 4)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    args = parse_args()
    main()
