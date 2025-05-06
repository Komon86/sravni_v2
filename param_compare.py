from mylib import *


def make_simple_dict(lst):
    result = {}
    while lst:
        first = lst.pop(0)
        if first[0] == '$':
            key = first[:5]
            value = first[6:]
            result[key] = value
    return result


# if __name__ == '__main__':
#    filename = 'ffr_7083_backup.txt'  # input('Введите имя файла: ')
#    strings = read_file(filename)
#    clear_lines = file_processing(strings)
#    uw_lines = unwrap(clear_lines)
#    result = make_dict(uw_lines)
#    o = json.dumps(result, sort_keys=True, indent=4)
#    print(o)
# woTochka = write(clear_lines)
# Ln = numerate(woTochka)




file1 = input("Первый файл :")
file2 = input("Второй файл :")
lines1 = read_file(file1)
lines2 = read_file(file2)
clearlines1 = lid_remover(lines1)
clearlines2 = lid_remover(lines2)
unwrap1 = unwrapper_old(clearlines1)
unwrap2 = unwrapper_old(clearlines2)
dict1 = make_simple_dict(unwrap1)
dict2 = make_simple_dict(unwrap2)
if len(dict2) < len(dict1):
    maindict = dict1
    sec_dict = dict2
else:
    maindict = dict2
    sec_dict = dict1
result_naked = []
not_found = []
for i in maindict.keys():
    if i in sec_dict.keys():
        result_naked.append(i + ":" + sec_dict[i])
for i in sec_dict.keys():
    if i not in maindict.keys():
        not_found.append(i)
result_naked = wrapper(result_naked)
result = numerate(result_naked)
# for j in result:
#    print(j)


out = open('out.txt', 'w', encoding='utf-8')
for i in result:
    out.write(i + "\n")
out.write('Недостающие ячейки: \n')
for i in not_found:
    out.write(i + '\n')
out.close()
