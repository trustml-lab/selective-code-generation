import argparse

def str2bool(v):
    """Util function for user friendly boolean flag args"""
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='transform stdio')
        self.parser.add_argument('--model_name', type=str)
        self.parser.add_argument('--dataset_name', type=str)
        self.parser.add_argument('--result_path', type=str)
        self.parser.add_argument('--alpha', type=float)
        self.parser.add_argument('--delta_s', type=float)
        self.parser.add_argument('--epsilon_s', type=float)
        self.parser.add_argument('--epsilon_e', type=float) 
        self.parser.add_argument('--eval_epsilon', type=float)
        self.parser.add_argument('--calib_limit', type=int)
        self.parser.add_argument('--eval_limit', type=int)  
        self.parser.add_argument('--add_epsilon', type=bool) 
        self.parser.add_argument('--manual_selection', type=bool, default=False)
        self.parser.add_argument('--exact_match', type=bool, default=False)
        self.parser.add_argument('--wo_selective', type=bool, default=False)

    def parse_args(self):
        return self.parser.parse_args()

    