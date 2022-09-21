import trans_star
import time
import os
# C:\Users\injea\PycharmProjects\trans_starbound\assetfile\english\objects\ancient\hologramgalaxy\hologramgalaxy.object

ko = trans_star.asset('sb_korpatch_union-master')
ch = trans_star.asset('chinese')
ko_dirpath = [i.lower() for i in ko.get_dirpath(del_absolute_path=True)]
li = []

for i in ch.patchfiles:
    patch = i
    for e in i.get_lines():
        dirpath = i.get_dirpath(del_absolute_path=True)
        if dirpath.lower() not in ko_dirpath:
            li.append(i)