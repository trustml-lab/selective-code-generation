from selective_code_generation.dataset.prompt.fn_prompt import generate_prompt_MBPP
from selective_code_generation.util.dataset_type import DatasetType
from util import parse_args

def main():
    args = parse_args()
    if args.dataset_type == DatasetType.MBPP:
        generate_prompt_MBPP(args.path)
    elif args.dataset_type == DatasetType.CODE_CONTESTS:
        pass
    else:
        pass

if __name__ == "__main__":
    main()
