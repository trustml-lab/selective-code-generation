from datasets import load_dataset
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm
from util import parse_args

import json
import jsonlines
import openai
import os

_ = load_dotenv(find_dotenv('/home/jeongjw/selective-code-generation/src/.env'))
openai.api_key = os.environ['OPENAI_API_KEY']

# lang = ['Cpp', 'Java', 'Perl', 'Kotlin']
lang = ['Javascript']

def generate_prompt_APPS(test_case, prompt, starter_code=None):
    _input = "\nSolve the following code problem that obeys the constraints and passes the example test cases. Do not add any explanations and just write code. \nQUESTION:\n"
    data = prompt
    _input += data
    if starter_code != None:
        data = starter_code
        data = "\n" + data #+ "\n"
        _input += data
    else:
        #_input += "\n\n"
        pass

    data = test_case
    if not data.get("fn_name"):
        _input += "\nUse Standard Input format"#\n"
    else:
        _input += "\nUse Call-Based format"#\n"
    
    _input += "\nANSWER:\n"

    return _input

def generate_gpt41(args):
    
    base_dir = "/home/jeongjw/selective-code-generation/dataset/APPS"

    split = args.split_dir
    split_dir = os.path.join(base_dir, split)
    exclude_file_path = f'/home/jeongjw/selective-code-generation/scripts/fuzz/exclude_problem/APPS_{split}.json'
    
    with open(exclude_file_path, 'r') as f:
        exclude_list = json.load(f)
    
    problem_idx = int(args.index)

    if problem_idx in exclude_list:
        print("Skipping")
        return

    problem_dir_path = os.path.join(split_dir, f'{args.index}')
    input_output_path = os.path.join(problem_dir_path, "input_output.json")

    with open(input_output_path, 'r') as f:
        input_output_info = json.load(f)

    if input_output_info.get('fn_name'):
        print("Skipping")
        return

    question_path = os.path.join(problem_dir_path, "question.txt")
    with open(question_path, 'r') as f:
        question = f.read()

    try:   
        starter_code_path = os.path.join(problem_dir_path, 'starter_code.py')
        with open(starter_code_path, 'r') as f:
            starter_code = f.read()
    except:
        starter_code = None


    for language in lang:

        prompt = f"You are an expert {language} programmer, solve the following problem in {language}"

        prompt += generate_prompt_APPS(input_output_info, question, starter_code=None)

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt}
            ],
            logprobs=True,
            max_tokens = 6000
        )
    
        output_dir_path = os.path.join(args.output, "APPS_lang", language, "raw", args.split_dir)
        os.makedirs(output_dir_path, exist_ok=True)
        output_path = os.path.join(output_dir_path, f'{args.index}.json')
    
        with open(output_path, 'w+') as f:
            json.dump(response.to_dict(), f, indent=4)

if __name__ == "__main__":
    args = parse_args()
    # generate(args)
    
    generate_gpt41(args)
