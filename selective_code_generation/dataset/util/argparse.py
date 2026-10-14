import argparse

class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Prompt generation for datasets')
        self.parser.add_argument('path', type=str, help='code path to be processed')
        self.parser.add_argument('solution_index', type=int, help='solution index')

    def parse_args(self):
        return self.parser.parse_args()
