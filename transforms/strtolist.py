
import trans_star

asset = trans_star.asset('test')
new = trans_star.asset('test1')
b = {}
for patchfile in asset.patchfiles:
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
            pass
        print(line.path)

    for i in b.values(): i.sort()
    print(b)
    b = {}
    print()