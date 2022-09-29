import os
import shutil
import trans_star

os.chdir('../')
asset = trans_star.asset('test')
new = trans_star.asset('test1')
b = {}
c = []
for patchfile in asset.patchfiles:
    print(patchfile.dir)
    newpatch = new.newPatchAppend(patchfile.dir)
    for line in patchfile.get_lines():
        pathdir = line.path[:line.path.rfind('/')]
        pathname = line.path[line.path.rfind('/') + 1:]

        try:
            pathname = int(pathname)
            try:
                if pathname not in b[pathdir]:
                    b[pathdir].append(pathname)
            except KeyError:
                b[pathdir] = []
                b[pathdir].append(pathname)
        except ValueError:
            c.append(line)
        print(line.path)

    for i in b.values(): i.sort()
    print(b)
    if b:
        for i in b.keys():
            l = newpatch.newLineAppend('replace', i, [])
            for a in b[i]:
                index = [line.path for line in patchfile.get_lines()].index(f'{i}/{a}')
                l.value.append([line for line in patchfile.get_lines()][index].value)

    for s in c:
        if s.path not in [i.path for i in newpatch.get_lines()]:
            newpatch.newLineAppend(s.op, s.path, s.value)
    newpatch.sort()
    b = {}
    c = []
    print()

new.save()

for i in asset.outerfile_dirs:
    if not os.path.exists(f"{new.dir}\\{os.path.dirname(i)}"):
        os.makedirs(f"{new.dir}\\{os.path.dirname(i)}")
    shutil.copy(f"{asset.dir}\\{i}", f"{new.dir}\\{i}")
    print(f"{asset.dir}\\{i}", f"{new.dir}\\{i}")




