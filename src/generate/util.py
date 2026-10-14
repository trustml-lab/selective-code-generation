import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Modifying data")
    
    parser.add_argument(
        '--dataset_type',
        type=str,
        default="APPS"
    )

    parser.add_argument(
        '--index',
        type=str,
        default=0,
        help="solution_index for canonical solutions"
    )

    parser.add_argument(
        '--split_dir',
        type=str,
        default="",
        help='split_dir for fuzzing dataset'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=""
    )

    parser.add_argument(
        '--base_dir',
        type=str,
        default=""
    )

    parser.add_argument(
        '--model_type',
        type=str,
        default=""
    )

    parser.add_argument(
        '--language',
        type=str
    )

    parser.add_argument(
        '--begin_index',
        type=int
    )
    
    parser.add_argument(
        '--end_index',
        type=int
    )

    return parser.parse_args()
