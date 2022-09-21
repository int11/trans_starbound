from trans_star import *
import json


class line:
    def __init__(self, dir, op, path, value):
        self.dir = dir
        self.op = op
        self.path = path
        self.value = value

    def get_dir(self, del_patch=False, del_absolute_path=False):
        dir = self.dir
        if del_patch:
            dir = function.del_patch(dir)
        if del_absolute_path:
            dir = function.del_absolute_path(dir)
        return dir

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return self.get_dir(del_patch, del_absolute_path) + self.path

    def get_value(self, encoding=None):
        value = self.value
        if encoding == 'unicode_escape':
            value = function.unicodeString_to_string(value)
        return value

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
    def __init__(self, patch_dir):
        self.dir = patch_dir
        self.lines = []
        with open(patch_dir, encoding='UTF-8') as f:
            content = f.read()
            jsdir = json.loads(content, strict=False)
            for i in jsdir:
                self.lines.append(line(patch_dir, i['op'],i['path'], i['value']))

    def get_dir(self, del_patch=False, del_absolute_path=False):
        dir = self.dir
        if del_patch:
            dir = function.del_patch(dir)
        if del_absolute_path:
            dir = function.del_absolute_path(dir)
        return dir

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return [i.get_dirpath(del_patch, del_absolute_path) for i in self.get_lines()]

    def get_lines(self):
        for line in self.lines:
            yield line


class asset:
    def __init__(self, asset_name):
        patch_dirs = del_dir(glob('assetfile\\' + asset_name + '\\**', recursive=True))

        self.patchfiles = [patchfile(i) for i in patch_dirs if 'patch' in os.path.splitext(i)[1]]
        self.outerfile_dirs = [i for i in patch_dirs if 'patch' not in os.path.splitext(i)[1]]

    def get_dir(self, del_patch=False, del_absolute_path=False):
        for patchfile in self.patchfiles:
            yield patchfile.get_dir(del_patch, del_absolute_path)

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return [i.get_dirpath(del_patch, del_absolute_path) for i in self.get_lines()]

    def get_lines(self):
        for patchfile in self.patchfiles:
            yield from patchfile.get_lines()

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
