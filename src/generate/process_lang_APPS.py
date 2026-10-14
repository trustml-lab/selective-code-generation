import os
import json

from util import parse_args

def main():

    base_dir = f"/home/jeongjw/selective-code-generation/generated_data/APPS_lang/{args.language}"
    raw_data_path = os.path.join(base_dir, "raw", args.split_dir)
    print(raw_data_path)

    begin_ind = 0
    end_ind = 4999

    if args.language == "Cpp":
        target_word = "cpp"
    elif args.language == "Java":
        target_word = "java"
    elif args.language == "Kotlin":
        target_word = "kotlin"
    elif args.language == "Perl":
        target_word = "perl"
    elif args.language == 'Javascript':
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

            print(dump_data)
            os.makedirs(f"/home/jeongjw/selective-code-generation/generated_data/APPS_lang/{args.language}/{args.split_dir}", exist_ok=True)
            with open (f"/home/jeongjw/selective-code-generation/generated_data/APPS_lang/{args.language}/{args.split_dir}/{index_str}.json", 'w+') as f:
                json.dump(dump_data, f, ensure_ascii=False, indent = 4)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    args = parse_args()
    main()
