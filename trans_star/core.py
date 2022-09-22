import os.path
import copy
from trans_star import *
from trans_star.function import *
import json


class line:
    def __init__(self, op, path, value, target_patch=None):
        self.op = op
        self.path = path
        self.value = value
        self.target_patch = target_patch

    def get_dir(self, del_patch=False, del_absolute_path=False):
        return self.target_patch.get_dir(del_patch, del_absolute_path)

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return self.get_dir(del_patch, del_absolute_path) + self.path

    def original_value(self, originalAssetName):
        if self.op == 'add':
            return None

        temp = self.path.split('/')[1:]
        asdf = os.path.join('assetfile', originalAssetName, self.get_dir(True, True))
        # print(f'{os.getcwd()}\\assetfile\\sb_korpatch_union-master\\{self.get_dir(del_absolute_path=True)}')
        # print(f'{os.getcwd()}\\assetfile\\chinese\\{self.get_dir(del_absolute_path=True)}')
        # print(f'{os.getcwd()}\\assetfile\\english\\{self.get_dir(True, del_absolute_path=True)}')

        with open(asdf, 'r', encoding='UTF-8') as f:
            read = f.read()
            while True:
                try:
                    jsdic = json.loads(read, strict=False)
                    break
                except json.decoder.JSONDecodeError as e:
                    index = read.find('//')
                    if index == -1:
                        index = read.find('/*')
                    if index == -1:
                        index = read.find('*/')
                    if index == -1:
                        read = read[:e.pos] + ',' + read[e.pos:]
                    b = read[index:]
                    read = read[:index] + b[b.find('\n'):]
                    continue

        for i in temp:
            try:
                jsdic = jsdic[i]
            except TypeError:
                try:
                    jsdic = jsdic[int(i)]
                except IndexError:
                    print(jsdic)
                    raise print(f"""\n\n Can't find Value of original "{self.path}"\n {asdf + self.path}\n""")
            except KeyError:
                print(jsdic)
                raise print(f"""\n\n Can't find Value of original "{self.path}"\n {asdf + self.path}\n""")

        return jsdic


class patchfile:
    def __init__(self, patch_dir=None, asset_target=None):
        self.dir = patch_dir
        self.lines = []
        self.asset_target = asset_target
        if os.path.exists(self.get_dir()):
            with open(self.get_dir(), encoding='UTF-8') as f:
                content = f.read()
                jsdir = json.loads(content, strict=False)
                for i in jsdir:
                    self.lines.append(line(i['op'], i['path'], i['value'], self))

    def get_dir(self, del_patch=False, del_absolute_path=False):
        dir = self.dir
        if del_patch:
            dir = function.del_patch(dir)
        if not del_absolute_path and self.asset_target is not None:
            dir = os.path.join(self.asset_target.dir, dir)
        return dir

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return [i.get_dirpath(del_patch, del_absolute_path) for i in self.get_lines()]

    def get_lines(self):
        for line in self.lines:
            yield line

    def newLineAppend(self, op, path, value):
        l = line(op, path, value, self)
        self.lines.append(l)
        return l

    def save(self):
        assert not os.path.exists(self.get_dir()), 'must save other directory for protect data'
        if not os.path.exists(os.path.dirname(self.get_dir())):
            os.makedirs(os.path.dirname(self.get_dir()))
        js = []
        for i in self.get_lines():
            print(i.get_dirpath(), i.value)
            js.append({'op': i.op, 'path': i.path, 'value': i.value})

        with open(self.get_dir(), 'w', encoding='UTF-8') as f:
            json.dump(js, f, indent=4, ensure_ascii=False)


class asset:
    def __init__(self, name):
        self.name = name
        self.dir = os.path.join('assetfile', name)
        patch_dirs = del_dir(glob(self.dir + '\\**', recursive=True))
        self.patchfiles = [patchfile(del_absolute_path(i), self) for i in patch_dirs if
                           'patch' in os.path.splitext(i)[1]]
        self.outerfile_dirs = [i for i in patch_dirs if 'patch' not in os.path.splitext(i)[1]]

    def get_dir(self, del_patch=False, del_absolute_path=False):
        for patchfile in self.patchfiles:
            yield patchfile.get_dir(del_patch, del_absolute_path)

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return [i.get_dirpath(del_patch, del_absolute_path) for i in self.get_lines()]

    def get_lines(self):
        for patchfile in self.patchfiles:
            yield from patchfile.get_lines()

    def newPatchAppend(self, dir):
        patch = patchfile(dir, self)
        self.patchfiles.append(patch)
        return patch

    def save(self):
        if not os.path.exists(self.dir):
            print(f"""Not found assetfile.\nMake aasetfile path : '{self.dir}''""")
            os.mkdir(self.dir)

        for i in self.patchfiles:
            i.save()

    def findPatch(self, dir):
        temp = [i.dir for i in self.patchfiles]
        try:
            return self.patchfiles[temp.index(dir)]
        except:
            return None


    @staticmethod
    def download_original_assets(starbound_dir, asset_name):
        current_dir = os.getcwd()
        os.chdir(starbound_dir)
        dir = f'{current_dir}\\assetfile\\{asset_name}'
        print('Original asset unpacking...')
        print(dir)

        try:
            os.system(f'.\\win32\\asset_unpacker.exe .\\assets\\packed.pak {dir}')
            print('Done')
        except:
            if os.path.exists(dir):
                os.remove(dir)
            print('Unpacking Fail')
            raise

        os.chdir(current_dir)
        return asset_name
