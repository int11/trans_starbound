from trans_star import *


class line:
    def __init__(self, dir, path, value):
        self.dir = dir
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


class patchfile:
    def __init__(self, patch_dir):
        self.dir = patch_dir
        self.lines = []
        with open(patch_dir, encoding='UTF-8') as f:
            content = f.read()
            while content.find('}') != -1:
                a = content[content.find('{') + 1:content.find('}')]
                self.lines.append(line(patch_dir, getdata(a, 'path'), getdata(a, 'value')))
                content = content[content.find('}') + 1:]

    def get_lines(self):
        for line in self.lines:
            yield line

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return [i.get_dirpath(del_patch, del_absolute_path) for i in self.get_lines()]


class asset:
    def __init__(self, asset_dir):
        patch_dirs = del_dir(glob(asset_dir + '\\**', recursive=True))

        self.patchfiles = [patchfile(i) for i in patch_dirs if 'patch' in os.path.splitext(i)[1]]
        self.outerfile_dirs = [i for i in patch_dirs if 'patch' not in os.path.splitext(i)[1]]

    def get_patchfiles(self):
        for patchfile in self.patchfiles:
            yield patchfile

    def get_lines(self):
        for patchfile in self.patchfiles:
            yield from patchfile.get_lines()

    def get_dirpath(self, del_patch=False, del_absolute_path=False):
        return [i.get_dirpath(del_patch, del_absolute_path) for i in self.get_lines()]

    @staticmethod
    def download_original_assets(starbound_dir):
        current_dir = os.getcwd()
        os.chdir(starbound_dir)
        print('original asset unpacking...')
        dir = f'{current_dir}\\assetfile\\unpackedassets'

        try:
            os.system(f'.\\win32\\asset_unpacker.exe .\\assets\\packed.pak {dir}')
        except:
            if os.path.exists(dir):
                os.remove(dir)
            raise

        os.chdir(current_dir)
        return dir
