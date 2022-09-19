import trans_star

# en_dir = asset.download_original_assets('E:\SteamLibrary\steamapps\common\Starbound')
# en = asset(en_dir)
ko = trans_star.asset('assetfile\\sb_korpatch_union-master')
ch = trans_star.asset('assetfile\\chinese')
ch_dirpath = ch.get_all_lines_dirpath(del_absolute_path=True)
ko_dirpath = ko.get_all_lines_dirpath(del_absolute_path=True)

compare = [0, 0, 0, 0]


for i in ko.iter_all_lines():
    dirpath = i.get_dirpath(del_absolute_path=True)
    if dirpath in ch_dirpath:
        compare[0] += 1
    else:
        compare[1] += 1

for i in ch.iter_all_lines():
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
