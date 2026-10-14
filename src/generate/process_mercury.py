import os
import json

def main():
    raw_data_path = os.path.join("/home/jeongjw/selective-code-generation/generated_data/MERCURY", "raw")

    for i in range(200):
        try:
            index_str = f'{i}'

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

            
            for j in range(data['usage']['completion_tokens'] - 1):
                token = data['choices'][0]['logprobs']['content'][j]['token']

                if '``' in token:
                    if begin_code_token == -1:
                        begin_code_token = j
                    else:
                        end_code_token = j
                        break

            if '```python' not in completion:
                continue

            trimmed_code = completion[completion.rfind("```python\n") + len("```python\n"):completion.rfind("```")]

            if trimmed_code == None or trimmed_code == "":
                continue

            iterator = data['usage']['completion_tokens']

            for index in range(begin_code_token, end_code_token):    
                # print(f"{data['choices'][0]['logprobs']['content'][index]['token']}: {log_prob_score}")
                log_prob_score += data['choices'][0]['logprobs']['content'][index]['logprob']
                total_count += 1

            dump_data = {"score": log_prob_score/total_count, "generated_code": trimmed_code}

            os.makedirs(f"/home/jeongjw/selective-code-generation/generated_data/MERCURY/processed", exist_ok=True)
            with open (f"/home/jeongjw/selective-code-generation/generated_data/MERCURY/processed/{i}.json", 'w+') as f:
                json.dump(dump_data, f, ensure_ascii=False, indent = 4)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
