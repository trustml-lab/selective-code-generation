import argparse

from selective_code_generation.util.str_to_type import *

def parse_args():
    parser = argparse.ArgumentParser(description="Modifying data")
    
    parser.add_argument(
        '--dataset_type',
        type=str2datasettype,
        default="APPS"
    )

    parser.add_argument(
        '--path',
        type=str,
        default="",
        help='absolute path of the problem directory'
    ) 

    parser.add_argument(
        '--begin_index',
        type=int,
        default=0,
        help="begin_index for fuzzing dataset"
    )

    parser.add_argument(
        '--end_index',
        type=int,
        default=0,
        help="end_index for fuzzing dataset"
    )

    parser.add_argument(
        '--solution_index',
        type=int,
        default=0,
        help="solution_index for canonical solutions"
    )

    parser.add_argument(
        '--split_dir',
        type=str,
        default="",
        help='split_dir for fuzzing dataset'
    )

    return parser.parse_args()
