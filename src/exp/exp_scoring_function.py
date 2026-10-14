from exp import exp

from selective_code_generation.exp.argparse import ArgParser

import os

def exp_model(args):

    args.manual_selection = False
    args.exact_match = False

    default_result_path = args.result_path

    #  scoring_function_lst = ['normalized_prob', 'seq_prob', 'lowest_prob', 'verbalized_prob']
    scoring_function_lst = ['normalized_prob']
    # scoring_function_lst = ['seq_prob']
    # scoring_function_lst = ['lowest_prob']
    # scoring_function_lst = ['verbalized_prob']

    for scoring_function in scoring_function_lst:
        args.result_path = os.path.join(default_result_path, scoring_function)
        exp(args)


    return

if __name__ == "__main__":
    argparser = ArgParser()
    args = argparser.parse_args()

    exp_model(args)
