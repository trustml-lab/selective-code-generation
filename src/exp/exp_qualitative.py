from exp import exp_qualitative

from selective_code_generation.exp.argparse import ArgParser

import os

def exp_qual(args):

    args.exact_match = False
    args.manual_selection = False
    args.wo_selective = False
    exp_qualitative(args)

    return

if __name__ == "__main__":
    argparser = ArgParser()
    args = argparser.parse_args()

    exp_qual(args)
