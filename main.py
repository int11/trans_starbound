from glob import glob
import os


def del_dir(x):
    return [i for i in x if not os.path.isdir(i)]


def del_absolute_path(x):
    return [i[i.find('\\', i.find('\\') + 1) + 1:] for i in x]


def del_patch(x):
    tmp = []
    for i in x:
        tmp.append(os.path.splitext(i)[0]) if 'patch' in os.path.splitext(i)[1] else tmp.append(i)
    return tmp


def tarns_lower(x):
    return [i.lower() for i in x]


def compare_original(x):
    tmp = []
    temp_en = del_absolute_path(en)
    for i in del_patch(del_absolute_path(x)):
        if i not in temp_en:
            tmp.append(i)
    return tmp


def unicodeString_to_string(x):
    return x.encode('utf-8').decode('unicode_escape')


def getdata(x, ward):
    b = x[x.find(ward) + len(ward) + 1:]
    c = b[b.find('"') + 1:]
    return c[:c.find('"')]


class patchfile:
    def __init__(self, dir):
        self.dir = dir
        self.text = patchfile.gettext(dir)

    @staticmethod
    def gettext(x):
        temp = []
        with open(x) as f:
            print(x)
            content = f.read()
            while content.find('}') != -1:
                a = content[content.find('{') + 1:content.find('}')]
                tmp = {'path': getdata(a, 'path'), 'value': getdata(a, 'value')}
                temp.append(tmp)
                content = content[content.find('}') + 1:]
        return temp


def get_All_patchfiles(dir_list):
    return [patchfile(i) for i in dir_list if 'patch' in os.path.splitext(i)[1]]


# en = del_dir(glob('compare\\unpackedassets\\**', recursive=True))
ko = del_dir(glob('compare\\sb_korpatch_union-master\\**', recursive=True))
ch = del_dir(glob('compare\\chinese\\**', recursive=True))

with open(ch[1], 'r', encoding='UTF-8') as f:
    content = f.read()

ch = get_All_patchfiles(ch)
ko = get_All_patchfiles(ko)
