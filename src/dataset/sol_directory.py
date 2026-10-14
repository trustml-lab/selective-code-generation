import os

from selective_code_generation.dataset.format.sol_dir.organize_sol_dir import *
from selective_code_generation.util.dataset_type import DatasetType
from tqdm import tqdm
from util import parse_args

def iter_directory(dataset_path: str, split_lst: list, dataset_type: DatasetType):
    for split in split_lst:
        split_path = os.path.join(dataset_path, split)

        directory_list = os.listdir(split_path)

        for dir_candidate in tqdm(directory_list): 
            problem_dir_path = os.path.join(split_path, dir_candidate)

            if not os.path.isdir(problem_dir_path):
                continue

            if dataset_type == DatasetType.MERCURY:
                code_type = CodeType.CALL
            elif dataset_type == DatasetType.MBPP:
                code_type = CodeType.CALL
            elif dataset_type == DatasetType.HUMANEVAL:
                code_type = CodeType.CALL
            organize_sol_dir(dataset_type, code_type, problem_dir_path)

def main():
    args = parse_args()

    # depending on the datatype call each function, create split_lst
    if args.dataset_type == DatasetType.MBPP:
        split_lst = ['train', 'test', 'validation', 'prompt'] 
        dataset_path = os.path.join(args.path, "MBPP")
    elif args.dataset_type == DatasetType.CODE_CONTESTS:
        split_lst = ['train', 'valid', 'test']
        dataset_path = os.path.join(args.path, "CODE_CONTESTS")
    elif args.dataset_type == DatasetType.MERCURY:
        split_lst = ['train', 'eval']
        dataset_path = os.path.join(args.path, "MERCURY")
    elif args.dataset_type == DatasetType.HUMANEVAL:
        split_lst = ['test/HumanEval']
        dataset_path = os.path.join(args.path, "HUMANEVAL")
    else:
        return 

    # for each dataset file, call organize_sol_dir function with appropriate parameter    
    iter_directory(dataset_path, split_lst, args.dataset_type)


if __name__ == "__main__":
    main()
