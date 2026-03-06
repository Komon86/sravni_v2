from mylib import *
from tema2 import *


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
unwrapper(clearlines1)
unwrapper(clearlines2)
dict1=create_parentdict(clearlines1)
dict2=create_parentdict(clearlines2)
for cell in dict1.keys():
    dict1[cell] = create_full_dict(dict1[cell])
for cell in dict2.keys():
    dict2[cell] = create_full_dict(dict2[cell])
#if len(dict2) < len(dict1):
#    maindict = dict1
#    sec_dict = dict2
#else:
#    maindict = dict2
#    sec_dict = dict1
#result_naked = []
#not_found = []
#for i in maindict.keys():
#    if i in sec_dict.keys():
#        result_naked.append(i + ":" + sec_dict[i])
#for i in sec_dict.keys():
#    if i not in maindict.keys():
#        not_found.append(i)
#result_naked = wrapper(result_naked)
#result = numerate(result_naked)
## for j in result:
##    print(j)

for cell in dict1.keys():
    for offset in dict1[cell].keys():
        if dict1[cell][offset].startswith('X'):
            dict1[cell][offset] = process_x(dict1[cell][offset])


lst=''
out=open('out.txt','w', encoding='utf-8')
for i in dict1.keys(): # печатаем номер ячейки
    cell=i
    out.write(i + ': ')
    try:
        for j in dict1[cell].keys():    # печатаем смещения
            out.write(j + ' ')
    except:
        for j in dict1[cell].keys():
            out.write(j + ' ')
        pass
    out.write('\n')
    out.write('       ')
    try:
        for j in dict1[cell].values():  # печатаем значения первого файла
            out.write(j + '   ')
    except:
        out.write('ячейка пуста')
        lst += i+'\n'
        pass
    out.write('\n')
    out.write('       ')
    try:
        for j in dict2[cell].keys():        # печатаем значения второго файла
            if dict2[cell][j].startswith('X'):
                dict2[cell][j] = process_x(dict2[cell][j], dict1[cell][j])
            out.write(dict2[cell][j]+'   ')
    except:
        out.write('ячейка пуста')
        lst += i+'\n'
        pass
        #for j in dict2[cell].keys():        # печатаем значения второго файла
        #    out.write(d1[cell][j]+'   ')
        #pass
    out.write('\n')
    try:
        if len(dict2[cell]) > len(dict1[cell]):
            out.write('АПАСНО!')
        else:
            out.write('       ')
        for j in dict1[cell].keys(): # указатель на несовпадения
            if dict1[cell][j] == 'N ' or dict2[cell][j] == 'N ':
                out.write('     ')
                continue
            elif dict1[cell][j] == '  ' or dict2[cell][j] == '  ':
                out.write('     ')
                continue
            elif dict1[cell][j] != dict2[cell][j]:
                out.write('ЖЖЖ  ')
                continue
            else:
                out.write('     ')
                continue
    except:
         out.write('???  ')
         pass
    out.write('\n')
out.write('Недостающие ячейки: ' + lst)
out.close()
