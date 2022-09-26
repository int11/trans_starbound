import os
from trans_star import *


def del_dir(x):
    return [i for i in x if not os.path.isdir(i)]


def del_patch(dir):
    return os.path.splitext(dir)[0] if 'patch' in os.path.splitext(dir)[1] else dir


def del_absolute_path(dir):
    if len(dir.split('\\')) >= 2:
        return os.path.join(*dir.split('\\')[2:])
    elif len(dir.split('/')) >= 2:
        return os.path.join(*dir.split('/')[2:])
    else:
        raise




def unicodeString_to_string(str):
    return str.encode('utf-8').decode('unicode_escape')




# def compare_original(x, original):
#     tmp = []
#     temp_en = del_absolute_path(original)
#     for i in del_patch(del_absolute_path(x)):
#         if i not in temp_en:
#             tmp.append(i)
#     return tmp
