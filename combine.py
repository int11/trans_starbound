import trans_star
import time
import os

# C:\Users\injea\PycharmProjects\trans_starbound\assetfile\english\objects\ancient\hologramgalaxy\hologramgalaxy.object

ko = trans_star.asset('sb_korpatch_union-master')
ch = trans_star.asset('chinese')
ko_dirpath = [i for i in ko.get_dirpath(del_absolute_path=True)]
li = []
new = trans_star.asset('korean')



for i in ko.patchfiles:
    temp = new.newPatchAppend(i.dir)
    for e in i.get_lines():
        temp.newLineAppend(e.op, e.path, e.value)

count = 0
for i in new.get_lines():
    count += 1
print(count)


temp_dir = ""
for i in ch.patchfiles:
    for e in i.get_lines():
        dirpath = e.get_dirpath(del_absolute_path=True)
        if dirpath not in ko_dirpath:
            patch = new.findPatch(e.target_patch.dir)
            if temp_dir != e.get_dir() and patch is None:
                patch = new.newPatchAppend(i.dir)
            patch.newLineAppend(e.op, e.path, e.value)
            temp_dir = e.get_dir()


count = 0
for i in new.get_lines():
    count += 1
print(count)

new.save()