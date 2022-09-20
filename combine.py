import trans_star
import time
import os
ko = trans_star.asset('assetfile\\sb_korpatch_union-master')
ch = trans_star.asset('assetfile\\chinese')

ko_dirpath = [i.lower() for i in ko.get_dirpath(del_absolute_path=True)]
li = []

for i in ch.get_lines():
    dirpath = i.get_dirpath(del_absolute_path=True)
    if dirpath.lower() not in ko_dirpath:
        li.append(i)


ko_dir = [i.lower() for i in ko.get_dir(del_absolute_path=True)]
for i in li:
    print(i.get_dir(del_absolute_path=True))
    if i.get_dir(del_absolute_path=True) in ko_dir:
        os.system(f'assetfile\\sb_korpatch_union-master\\{i.get_dir(del_absolute_path=True)}')
        print(1)
        os.system(f'assetfile\\chinese\\{i.get_dir(del_absolute_path=True)}')
        print(2)
        time.sleep(10)
