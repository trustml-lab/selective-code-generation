import argparse

class ArgParserVerify:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='transform stdio')
        self.parser.add_argument('--dataset_type', type=str, default="")
        self.parser.add_argument('--split_dir', type=str, default="")
        self.parser.add_argument('--begin_index', type=int, default=0)
        self.parser.add_argument('--end_index', type=int, default=0)
        self.parser.add_argument('--result_path', type=str, default="/home/jeongjw/selective-code-generation/result/verification")

    def parse_args(self):
        return self.parser.parse_args()
    