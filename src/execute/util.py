import argparse

from selective_code_generation.util.str_to_type import *

def parse_args():
    parser = argparse.ArgumentParser(description="Modifying data")
    
    parser.add_argument(
        '--dataset_type',
        type=str,
        default="APPS"
    )

    parser.add_argument(
        '--generated_data_path',
        type=str,
        default="",
        help='absolute path of the problem directory'
    ) 

    parser.add_argument(
        '--dataset_path',
        type=str,
        default="",
        help='absolute path of the problem directory'
    ) 

    parser.add_argument(
        '--problem_index',
        type=str,
        default="0000",
        help="begin_index for fuzzing dataset"
    )

    parser.add_argument(
        '--split_dir',
        type=str,
        default="",
        help='split_dir for fuzzing dataset'
    )

    parser.add_argument(
        '--result_dir',
        type=str,
        default="",
        help="result_dir for execution result"
    )

    parser.add_argument(
        '--model_type',
        type=str,
        default="",
        help="model_type"
    )

    return parser.parse_args()
