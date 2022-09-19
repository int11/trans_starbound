import time
from glob import glob
import os


def del_dir(x):
    return [i for i in x if not os.path.isdir(i)]


# def compare_original(x, original):
#     tmp = []
#     temp_en = del_absolute_path(original)
#     for i in del_patch(del_absolute_path(x)):
#         if i not in temp_en:
#             tmp.append(i)
#     return tmp


def unicodeString_to_string(x):
    return x.encode('utf-8').decode('unicode_escape')


def getdata(x, ward):
    b = x[x.find(ward) + len(ward) + 1:]
    c = b[b.find('"') + 1:]
    return c[:c.find('"')]


class line:
    def __init__(self, dir, path, value):
        self.dir = dir
        self.path = path
        self.value = value

    def get_dir(self, del_patch=False, del_absolute_path=False):
        dir = self.dir
        if del_patch:
            dir = os.path.splitext(dir)[0] if 'patch' in os.path.splitext(dir)[1] else dir
        if del_absolute_path:
            dir = dir[dir.find('\\', dir.find('\\') + 1) + 1:]
        return dir

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return self.get_dir(del_patch, del_absolute_path) + self.path


class patchfile:
    def __init__(self, patch_dir):
        self.dir = patch_dir
        self.lines = self.getline(patch_dir)

    def getline(self, x):
        temp = []
        with open(x, encoding='UTF-8') as f:
            content = f.read()
            while content.find('}') != -1:
                a = content[content.find('{') + 1:content.find('}')]
                tmp = line(self.dir, getdata(a, 'path'), getdata(a, 'value'))
                temp.append(tmp)
                content = content[content.find('}') + 1:]
        return temp


class asset:
    def __init__(self, asset_dir):
        patch_dirs = del_dir(glob(asset_dir + '\\**', recursive=True))

        self.patchfiles = [patchfile(i) for i in patch_dirs if 'patch' in os.path.splitext(i)[1]]
        self.outerfile_dirs = [i for i in patch_dirs if 'patch' not in os.path.splitext(i)[1]]

    def iter_patchfiles(self):
        for patchfile in self.patchfiles:
            yield patchfile

    def iter_all_lines(self):
        for patchfile in self.patchfiles:
            for line in patchfile.lines:
                yield line

    def get_all_lines_dirpath(self, del_patch=False, del_absolute_path=False):
        return [i.get_dirpath(del_patch, del_absolute_path) for i in self.iter_all_lines()]

    @staticmethod
    def download_original_assets(starbound_dir):
        current_dir = os.getcwd()
        os.chdir(starbound_dir)
        print('asset unpacking...')
        dir = f'{current_dir}\\compare\\unpackedassets'
        os.system(f'.\\win32\\asset_unpacker.exe .\\assets\\packed.pak {dir}')
        os.chdir(current_dir)
        return dir


# en_dir = asset.download_original_assets('E:\SteamLibrary\steamapps\common\Starbound')
# en = asset(en_dir)
ko = asset('compare\\sb_korpatch_union-master')
ch = asset('compare\\chinese')
ch_dirpath = ch.get_all_lines_dirpath(del_absolute_path=True)
ko_dirpath = ko.get_all_lines_dirpath(del_absolute_path=True)
print(len(ko_dirpath), len(ch_dirpath))
li = [0, 0, 0, 0]
li0 = [[], [], [], []]

for i in ko.iter_all_lines():
    dirpath = i.get_dirpath(del_absolute_path=True)
    if dirpath in ch_dirpath:
        li[0] += 1
        li0[0].append(dirpath)
    else:
        li[1] += 1
        li0[1].append(dirpath)

for i in ch.iter_all_lines():
    dirpath = i.get_dirpath(del_absolute_path=True)
    if dirpath in ko_dirpath:
        li[2] += 1
        li0[2].append(dirpath)
    else:
        li[3] += 1
        li0[3].append(dirpath)

print(li)