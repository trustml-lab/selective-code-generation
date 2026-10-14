from datasets import load_dataset
from dotenv import load_dotenv, find_dotenv
from util import parse_args

from lm_polygraph import BlackboxModel, estimate_uncertainty
from lm_polygraph.estimators import *
from lm_polygraph.utils.generation_parameters import GenerationParameters

import json
import jsonlines
import openai
import os

_ = load_dotenv(find_dotenv('/home/jeongjw/selective-code-generation/src/.env'))
openai.api_key = os.environ['OPENAI_API_KEY']

def generate_prompt_MBPP(problem_index):
    with jsonlines.open("/home/jeongjw/selective-code-generation/dataset/mbxp/mbpp_release_v1.jsonl") as f:
        all_items = list(f)
        prompt = all_items[int(problem_index) - 1]['prompt']
    return "Complete the following programming problem.\n" + prompt

def generate_gpt4o(args):

    problem_path = os.path.join(args.base_dir, args.split_dir, args.index)
    prompt = generate_prompt_MBPP(args.index)

    model = BlackboxModel.from_openai(
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model_path='gpt-3.5-turbo',
        supports_logprobs=True
    )

    perplexity_method = Perplexity()
    os.makedirs(os.path.join(args.output, "perplexity"), exist_ok=True)

    ue = estimate_uncertainty(
        model, 
        perplexity_method, 
        input_text=prompt
    )
    
    dump_data = {"score": ue.uncertainty, "generated_code": ue.generation_text}

    with open(os.path.join(args.output, "perplexity", f'{args.index}.json'), 'w+') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)


    max_seq_prob_method = MaximumSequenceProbability()
    os.makedirs(os.path.join(args.output, "maxseqprob"), exist_ok=True)

    ue = estimate_uncertainty(
        model,
        max_seq_prob_method,
        input_text=prompt
    )

    dump_data = {"score": ue.uncertainty, "generated_code": ue.generation_text}

    with open(os.path.join(args.output, "maxseqprob", f'{args.index}.json'), 'w+') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)


    eig_val_laplacian_method = EigValLaplacian()
    os.makedirs(os.path.join(args.output, "eigvallaplacian"), exist_ok=True)

    ue = estimate_uncertainty(
        model, 
        eig_val_laplacian_method,
        input_text=prompt
    )

    dump_data = {"score": ue.uncertainty, "generated_code": ue.generation_text}

    with open(os.path.join(args.output, "eigvallaplacian", f'{args.index}.json'), 'w+') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)
    

    deg_mat_method = DegMat()
    os.makedirs(os.path.join(args.output, "degmat"), exist_ok=True)

    ue = estimate_uncertainty(
        model,
        deg_mat_method,
        input_text=prompt
    )

    dump_data = {"score": ue.uncertainty, "generated_code": ue.generation_text}

    with open(os.path.join(args.output, "degmat", f'{args.index}.json'), 'w+') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)


    ecc_method = Eccentricity()
    os.makedirs(os.path.join(args.output, "ecc"), exist_ok=True)

    ue = estimate_uncertainty(
        model,
        ecc_method,
        input_text=prompt
    )

    dump_data = {"score": ue.uncertainty, "generated_code": ue.generation_text}

    with open(os.path.join(args.output, "ecc", f'{args.index}.json'), 'w+') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    args = parse_args()
    # generate(args)

    os.makedirs(args.output, exist_ok=True)
    generate_gpt4o(args)
