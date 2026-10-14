from datasets import load_dataset
from dotenv import load_dotenv, find_dotenv
from friendli import Friendli
from util import parse_args

import json
import jsonlines
import openai
import os

_ = load_dotenv(find_dotenv('/home/jeongjw/selective-code-generation/src/.env'))
openai.api_key = os.environ['OPENAI_API_KEY']

def generate_prompt_MBCPP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbcpp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBCSP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbcsp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBGP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbgp_release_v1.1.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBJP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbjp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBJSP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbjsp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBKP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbkp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBPHP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbphp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBPLP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbplp_release_v1.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBRBP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbrbp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBSCP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbscp_release_v1.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBSWP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbswp_release_v1.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_prompt_MBTSP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbtsp_release_v1.2.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_gpt4o(args):
    
    try:
        mbcpp_prompt = generate_prompt_MBCPP(args.index)
    except:
        mbcpp_prompt = None
    try:
        mbcsp_prompt = generate_prompt_MBCSP(args.index)
    except:
        mbcsp_prompt = None
    try:
        mbgp_prompt = generate_prompt_MBGP(args.index)
    except:
        mbgp_prompt = None
    try:
        mbjp_prompt = generate_prompt_MBJP(args.index)
    except:
        mbjp_prompt = None
    try:
        mbjsp_prompt = generate_prompt_MBJSP(args.index)
    except:
        mbjsp_prompt = None
    try:
        mbkp_prompt = generate_prompt_MBKP(args.index)
    except:
        mbkp_prompt = None
    try:
        mbphp_prompt = generate_prompt_MBPHP(args.index)
    except:
        mbphp_prompt = None
    try:
        mbplp_prompt = generate_prompt_MBPLP(args.index)
    except:
        mbplp_prompt = None
    try:
        mbrbp_prompt = generate_prompt_MBRBP(args.index)
    except:
        mbrbp_prompt = None
    try:
        mbscp_prompt = generate_prompt_MBSCP(args.index)
    except:
        mbscp_prompt = None
    try:
        mbswp_prompt = generate_prompt_MBSWP(args.index)
    except:
        mbswp_prompt = None
    try:
        mbtsp_prompt = generate_prompt_MBTSP(args.index)
    except: 
        mbtsp_prompt = None

    prompt_list = [
        mbcpp_prompt,
        mbcsp_prompt,
        mbgp_prompt,
        mbjp_prompt,
        mbjsp_prompt,
        mbkp_prompt,
        mbphp_prompt,
        mbplp_prompt,
        mbrbp_prompt,
        mbscp_prompt,
        mbswp_prompt,
        mbtsp_prompt
    ]

    MBXP_list = [
        'MBCPP',
        'MBCSP',
        'MBGP',
        'MBJP',
        'MBJSP',
        'MBKP',
        'MBPHP',
        'MBPLP',
        'MBRBP',
        'MBSCP',
        'MBSWP',
        'MBTSP'
    ]

    for (prompt,name) in zip(prompt_list, MBXP_list):

        if prompt is None:
            continue
        
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            logprobs=True,
            max_tokens = 6000
        )

        dataset_type = name
    
        output_dir_path = os.path.join(args.output, dataset_type, args.model_type, "raw", args.split_dir)
        os.makedirs(output_dir_path, exist_ok=True)
        output_path = os.path.join(output_dir_path, f'{args.index}.json')
    
        with open(output_path, 'w+') as f:
            json.dump(response.to_dict(), f, indent=4)

if __name__ == "__main__":
    args = parse_args()
    # generate(args)
    
    generate_gpt4o(args)
