import trans_star


ko = trans_star.asset('sb_korpatch_union-master')
ch = trans_star.asset('chinese')
ch_dirpath = [i for i in ch.get_dirpath(del_absolute_path=True)]
ko_dirpath = [i for i in ko.get_dirpath(del_absolute_path=True)]

compare = [0, 0, 0, 0]


for i in ko.get_lines():
    dirpath = i.get_dirpath(del_absolute_path=True)
    if dirpath in ch_dirpath:
        compare[0] += 1
    else:
        compare[1] += 1

for i in ch.get_lines():
    dirpath = i.get_dirpath(del_absolute_path=True)
    if dirpath in ko_dirpath:
        compare[2] += 1
    else:
        compare[3] += 1

print(compare, '\n\n')

print(f'한국어 번역된 문장 : {len(ko_dirpath)}개, 중국어 번역된 문장 : {len(ch_dirpath)}개')
print(f'중국어 한국어 공통 번역 문장 {compare[0]}개')
print(f'한국어만 번역된 문장 {compare[1]}개')
print(f'중국어만 번역된 문장 {compare[3]}개')
