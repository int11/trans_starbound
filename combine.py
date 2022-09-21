import trans_star
import time
import os
# C:\Users\injea\PycharmProjects\trans_starbound\assetfile\english\objects\ancient\hologramgalaxy\hologramgalaxy.object

ko = trans_star.asset('sb_korpatch_union-master')
ch = trans_star.asset('chinese')
count = 0
for i in ch.get_lines():
    print(i.original_value('english'))
    count += 1
print(count)
