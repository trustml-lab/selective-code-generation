
def return_begin_end_index_split_lst(dataset_name):

    if dataset_name == "APPS":

        begin_index = 0
        end_index = 4999

        return [('train', begin_index, end_index), ('test', begin_index, end_index)]

    elif dataset_name == "HUMANEVAL":

        begin_index = 0
        end_index = 163

        return [('test', begin_index, end_index)]

    elif dataset_name == "MERCURY":

        return [('train', 0, 1632), ('eval', 0, 255)]

    else:
        begin_index = 1
        end_index = 974

        return [('test', 1, 974)]
