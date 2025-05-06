import json
from typing import List


def read_file(file):
    """
    Считывает строки из файла в список, возвращает список строк.
    :param file:
    :return: []
    """
    lines = [line.rstrip() for line in open(file)]
    return lines


def lid_remover(lines):
    """
    Удаляет LID_X=, возвращает список строк.
    :param lines:
    :return:
    """
    le = []
    for j in lines:
        if 'LID_' in j and '=' in j:
            line = j.split('=')
            if (line[0])[-1].isdigit():
                le.append(line[1])
    return le


def unwrapper_old(clearlines):
    """
    Присоединяет продолжения строк к изначальной строке.
    Использует второй список, возвращает список строк.
    """
    #  queue = ''
    #  index = 0
    #  dollar = 0
    #  for j in range(len(clearlines)):
    #      if '$' in clearlines[j]:
    #          dollar += 1
    #  # print(dollar)
    #  while index < dollar:
    #      if '$' in clearlines[index]:
    #          clearlines[index - 1] += queue
    #          queue = ''
    #          index += 1
    #      else:
    #          line = clearlines.pop(index)
    #          queue += line
    #  #       print(queue)
    #  return clearlines
    result_list = []
    for line in clearlines:
        line.rstrip()
        if '$' in line:
            result_list.append(line)
        else:
            result_list[-1] += line
    for line in result_list:
        line += '\n'
    return result_list


def unwrapper(strings: List[str]):
    """
    Присоединяет продолжения строк к изначальной строке.
    Не использует второй список, изменяет список на месте. Ничего не возвращает.
    """
    i = 0
    while i < len(strings):
        if "$" not in strings[i]:
            strings[i - 1] += strings[i]
            strings.pop(i)
        else:
            i += 1


def changes_detector(clearlines):
    """
    Эта функция для записи ТОЛЬКО ТЕХ параметров, в которые внесены изменения.
    Нужна для того чтобы 54 птм отпараметрировать без проблем.
    :param clearlines:
    :return:
    """
    lst = []
    for j in clearlines:
        if ";" in j:
            continue
        else:
            lst.append(j)
    return lst


def wrapper(lst):
    """
    Сворачивает строки обратно по 80 символов
    :param lst:
    :return:
    """
    result = []
    for i in lst:
        if len(i) > 80:
            while i:
                result.append(i[:80])
                i = i[80:]
        else:
            result.append(i)
    return result


def numerate(lst):
    """
    Проставляет LID-ы
    :param lst:
    :return:
    """
    ln = []
    for j in range(len(lst)):
        ln.append("LID_" + str(j + 1) + "=" + lst[j])
    return ln


def make_dict(lst):
    """
    Хуярим словарь с параметрами
    :param lst:
    :return:
    """
    result = {}
    while lst:
        first = lst.pop(0)
        cell = ''
        offset = ''
        while first:
            # offsets = []
            # cursor = int('0', 16)
            if first[0] == '$':
                cell = first[:5]    # отлавливаем номер ячейки
                result[cell] = {}   # теперь элемент $XXXX - ключ вложенного словаря
                first = first[5:]   # отрезаем ячейку от строки
            elif first[0] == ':':
                offset = '%04X' % (int(first[1:5], 16))  # отлавливаем смещение с которого пойдет запись, может быть не
                first = first[5:]         # с нуля. Отрезаем смещение от строки и пихаем его ключом вложенного словаря
                result[cell][offset] = []       # создаем пустой вложенный список, в котором будут параметры
            elif first[0] == 'X':
                parameter = first[:5]
                first = first[5:]
                result[cell][offset].append(parameter)
            elif first[0] == 'N':
                parameter = first[:1]
                first = first[1:]
                result[cell][offset].append(parameter)
            elif first[0] == '\n':
                pass
            elif first[0] == ';':
                pass
            else:
                parameter = first[:2]
                first = first[2:]
                result[cell][offset].append(parameter)
    return result


if __name__ == '__main__':
    filename = 'ffr_7083_backup.txt'  # input('Введите имя файла: ')
    strings = read_file(filename)
    clear_lines = lid_remover(strings)
    uw_lines = unwrapper_old(clear_lines)
    result = make_dict(uw_lines)
    o = json.dumps(result, sort_keys=True, indent=4)
    print(o)
# woTochka = write(clear_lines)
# Ln = numerate(woTochka)
    out = open('out.txt', 'w', encoding='utf-8')
    out.write(o)
    out.close()
