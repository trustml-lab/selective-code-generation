from exp import exp

from selective_code_generation.exp.argparse import ArgParser

import os

def exp_model(args):
    
    model_lst = ['gpt-4o', 'gemini', 'deepseek-r1', 'codellama-13b-instruct']

    for model in model_lst:
        # if model == 'codellama-13b-instruct':
        #    args.alpha = 0.7

        # gpt-4o experiment
        args.model_name = model
        original_result_path = args.result_path
        original_calib_limit = args.calib_limit

        # basic selective classifier with exact match
        args.result_path = os.path.join(original_result_path, "SCG-EM")
        args.calib_limit = original_calib_limit
        args.add_epsilon = False
        args.manual_selection = False
        args.exact_match = True
        exp(args)

        # selective classifier with 21 unit tests
        args.result_path = os.path.join(original_result_path, "SCG-small")
        args.calib_limit = 21
        args.add_epsilon = True
        args.manual_selection = False
        args.exact_match = False
        exp(args)

        # manual selection
        args.result_path = os.path.join(original_result_path, "SCG-manual")
        args.calib_limit = original_calib_limit
        args.add_epsilon = True
        args.manual_selection = True
        args.exact_match = False
        exp(args)

        # SCG-H
        args.result_path = os.path.join(original_result_path, "SCG-H")
        args.calib_limit = original_calib_limit
        args.add_epsilon = False
        args.manual_selection = False
        args.exact_match = False
        exp(args)

        # SCG
        args.result_path = os.path.join(original_result_path, "SCG")
        args.calib_limit = original_calib_limit
        args.add_epsilon = True
        args.manual_selection = False
        args.exact_match = False
        exp(args)

        args.result_path = original_result_path

    return

if __name__ == "__main__":
    argparser = ArgParser()
    args = argparser.parse_args()

    exp_model(args)
