import argparse

from selective_code_generation.util.dataset_type import DatasetType
from selective_code_generation.util.code_type import CodeType

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
    
def str2datasettype(v):
    if v=="APPS":
        return DatasetType.APPS
    elif v=="MBPP":
        return DatasetType.MBPP
    elif v=="CODE_CONTESTS":
        return DatasetType.CODE_CONTESTS
    elif v=="MERCURY":
        return DatasetType.MERCURY
    elif v=="HUMANEVAL":
        return DatasetType.HUMANEVAL
    else:
        return DatasetType.UNKNOWN
    
def str2codetype(v):
    if v=="STDIO":
        return CodeType.STDIO
    elif v=="CALL":
        return CodeType.CALL
    else:
        return CodeType.UNKNOWN
