from selective_code_generation.dataset.format.tree_struct.format import *
from selective_code_generation.util.dataset_type import DatasetType
from util import parse_args

def main():
    args = parse_args()
    if args.dataset_type == DatasetType.MBPP:
        format_mbpp(args.path)
    elif args.dataset_type == DatasetType.CODE_CONTESTS:
        format_code_contests(args.path)
    elif args.dataset_type == DatasetType.MERCURY:
        format_mercury(args.path)
    elif args.dataset_type == DatasetType.HUMANEVAL:
        format_humaneval(args.path)
    else:
        pass

if __name__ == "__main__":
    main()
