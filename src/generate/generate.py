from datasets import load_dataset
from dotenv import load_dotenv, find_dotenv
from friendli import Friendli
from util import parse_args

import json
import jsonlines
import openai
import os

client = Friendli(token="flp_ZiT9uFilHDwcuoYdCZBHioGE1D7thmB4AHODfTZQQLRgaa")
_ = load_dotenv(find_dotenv('/home/jeongjw/selective-code-generation/src/.env'))
openai.api_key = os.environ['OPENAI_API_KEY']

def generate_prompt_APPS(test_case, prompt, starter_code=None):
    _input = "\nWrite a python code to solve the following code problem that obeys the constraints and passes the example test cases. Do not add any explanations and just write code. \nQUESTION:\n"
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

def generate_prompt_MBPP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbpp_release_v1.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_HumanEval(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/multilingual_humaneval/HumanEval.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index)]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MERCURY(problem_index, split_dir):
    ds = load_dataset("Elfsong/Mercury")[split_dir]
    ele = ds[int(problem_index)]
    return "Solve the follwing programming problem.\n" + ele['pretty_content'][0] + ele['prompt']

def recursive_to_dict(obj):
    if isinstance(obj, list):
        return [recursive_to_dict(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return {k: recursive_to_dict(v) for k, v in vars(obj).items()}
    else:
        return obj

def generate_deepseek_r1(args):

    problem_path = os.path.join(args.base_dir, args.split_dir, args.index)

    input_output_path = os.path.join(problem_path, 'input_output.json')
    with open(input_output_path, 'r') as f:
        input_output = json.load(f)
    
    question_path = os.path.join(problem_path, 'question.txt')
    with open(question_path, 'r') as f:
        question = f.read()
    
    try:   
        starter_code_path = os.path.join(problem_path, 'starter_code.py')
        with open(starter_code_path, 'r') as f:
            starter_code = f.read()
    except:
        starter_code = None
    
    prompt = generate_prompt_APPS(input_output, question, starter_code)

    chat_completion = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {
                "role": "user",
                "content": f"{prompt}"
                # "content": "What is the capital of Japan?"
            }
        ],
        logprobs=True,
        max_tokens=20000
    )
    chat_completion_dict = recursive_to_dict(chat_completion)
    
    output_dir_path = os.path.join(args.output, args.dataset_type, args.model_type, "raw", args.split_dir)
    os.makedirs(output_dir_path, exist_ok=True)
    output_path = os.path.join(output_dir_path, f'{args.index}.json')
    
    with open(output_path, 'w+') as f:
        json.dump(chat_completion_dict, f, indent=4)

def generate_gpt4o(args):
    problem_path = os.path.join(args.base_dir, args.split_dir, args.index)

    if args.dataset_type == "APPS":
        input_output_path = os.path.join(problem_path, 'input_output.json')
        with open(input_output_path, 'r') as f:
            input_output = json.load(f)
        
        question_path = os.path.join(problem_path, 'question.txt')
        with open(question_path, 'r') as f:
            question = f.read()
        
        try:   
            starter_code_path = os.path.join(problem_path, 'starter_code.py')
            with open(starter_code_path, 'r') as f:
                starter_code = f.read()
        except:
            starter_code = None
    
    if args.dataset_type == "APPS":
        prompt = generate_prompt_APPS(input_output, question, starter_code)
    elif args.dataset_type == "MERCURY":
        prompt = generate_prompt_MERCURY(args.index, args.split_dir)
    elif args.dataset_type == "HUMANEVAL":
        prompt = generate_prompt_HumanEval(args.index)
    elif args.dataset_type == "MBPP":
        prompt = generate_prompt_MBPP(args.index)

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        logprobs=True,
        max_tokens = 6000
    )
    
    output_dir_path = os.path.join(args.output, args.dataset_type, args.model_type, "raw", args.split_dir)
    os.makedirs(output_dir_path, exist_ok=True)
    output_path = os.path.join(output_dir_path, f'{args.index}.json')
    
    with open(output_path, 'w+') as f:
        json.dump(response.to_dict(), f, indent=4)

if __name__ == "__main__":
    args = parse_args()
    # generate(args)

    if args.model_type == "deepseek-r1":
        generate_deepseek_r1(args)
    elif args.model_type == "gpt-4o":
        generate_gpt4o(args)
    else:
        raise NotImplemented
