from trans_star import *


def del_dir(x):
    return [i for i in x if not os.path.isdir(i)]


def unicodeString_to_string(x):
    return x.encode('utf-8').decode('unicode_escape')


def getdata(x, ward):
    b = x[x.find(ward) + len(ward) + 1:]
    c = b[b.find('"') + 1:]
    return c[:c.find('"')]


# def compare_original(x, original):
#     tmp = []
#     temp_en = del_absolute_path(original)
#     for i in del_patch(del_absolute_path(x)):
#         if i not in temp_en:
#             tmp.append(i)
#     return tmp
