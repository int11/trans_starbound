from trans_star import *


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
        lines = []
        with open(x, encoding='UTF-8') as f:
            content = f.read()
            while content.find('}') != -1:
                a = content[content.find('{') + 1:content.find('}')]
                line = line(self.dir, getdata(a, 'path'), getdata(a, 'value'))
                lines.append(line)
                content = content[content.find('}') + 1:]
        return lines


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
