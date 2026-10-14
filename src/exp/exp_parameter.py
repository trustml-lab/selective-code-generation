from exp import exp

from selective_code_generation.exp.argparse import ArgParser

import os

def exp_model(args):

    args.manual_selection = False
    args.exact_match = False

    default_result_path = args.result_path

    # 14 ~ 60
    # # alpha exp 
    # alpha_lst = [0.1, 0.2, 0.3, 0.4, 0.5]
    # default_alpha = args.alpha

    # for alpha in alpha_lst:
    #     args.result_path = os.path.join(default_result_path, "alpha")
    #     args.alpha = alpha
    #     exp(args)
    
    # args.alpha = default_alpha


    # # epsilon_s exp
    # epsilon_s_lst = [0.1, 0.2, 0.3, 0.4, 0.5]
    # default_epsilon_s = args.epsilon_s

    # for epsilon_s in epsilon_s_lst:
    #     args.result_path = os.path.join(default_result_path, "epsilon_s")
    #     args.epsilon_s = epsilon_s
    #     exp(args)

    # args.epsilon_s = default_epsilon_s


    # # epsilon_e exp 
    # # epsilon_e_lst = [0.1, 0.2, 0.3, 0.4, 0.5]
    # epsilon_e_lst = [0.05, 0.1, 0.15, 0.2]
    # default_epsilon_e = args.epsilon_e

    # for epsilon_e in epsilon_e_lst:
    #     args.result_path = os.path.join(default_result_path, "epsilon_e")
    #     args.epsilon_e = epsilon_e
    #     exp(args)

    # args.epsilon_e = default_epsilon_e


    # # delta_s exp
    # delta_s_lst = [0.001, 0.01, 0.1]
    # default_delta_s = args.delta_s

    # for delta_s in delta_s_lst:
    #     args.result_path = os.path.join(default_result_path, "delta_s")
    #     args.delta_s = delta_s
    #     exp(args)

    # args.delta_s = default_delta_s


    # eval_limit exp
    eval_limit_lst = [25, 70, 110, 150]
    default_eval_limit = args.eval_limit

    for eval_limit in eval_limit_lst:
        args.result_path = os.path.join(default_result_path, "eval_limit")
        args.eval_limit = eval_limit
        exp(args)

    args.eval_limit = default_eval_limit

    return

if __name__ == "__main__":
    argparser = ArgParser()
    args = argparser.parse_args()

    exp_model(args)
