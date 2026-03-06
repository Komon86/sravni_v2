from typing import List


def read_file(file):
    """
    Считывает строки из файла в список, возвращает список строк.
    :param file: str
    :return: []
    """
    lines = [line.rstrip() for line in open(file)]
    return lines


def lid_remover(lines):
    """
    Удаляет LID_X=, возвращает список строк.
    :param lines: str
    :return: []
    """
    le = []
    for j in lines:
        if 'LID_' in j and '=' in j:
            line = j.split('=')
            if (line[0])[-1].isdigit():
                le.append(line[1])
    return le


def unwrapper(strings: List[str]):
    """
    Процедура
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
    Нужна для того чтобы 54 птм отпараметрировать без проблем за один раз.
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
    :param lst: list
    :return: list
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

def dict_len(data_str):
    """
    Считает длину словаря
    :param data_str:
    :return:
    """
    last_colon_index = data_str.rfind(':')
    offset = int(data_str[last_colon_index + 1: last_colon_index + 5], 16)
    remains = data_str[last_colon_index + 5:]
    while remains:
        if remains[0] == 'X':
            remains = remains[5:]
            offset += 1
        elif remains[0] == 'N':
            remains = remains[1:]
            offset += 1
        else:
            remains = remains[2:]
            offset += 1
    return offset


# print(dict_len(s))


def create_empty_dict(dict_len: int):
    """
    Создает пустой словарь нужной длины
    :param dict_len: int
    :return:
    """
    result = {}
    for key in range(dict_len):
        result[f'{key:04X}'] = '    '
    return result


def create_dict(data_str: str):
    """
    Создает словарь в котором есть какие-либо байты
    :param data_str:
    :return:
    """
    result = {}
    while data_str:
        offset_index = data_str.find(':')
        if offset_index == -1:
            break
        offset = int(data_str[offset_index + 1: offset_index + 5], 16)
        # offset_decimal = int(offset, 16)
        result[f'{offset:04X}'] = None
        data_str = data_str[offset_index + 5:]
        while data_str:
            if data_str[0] == ':':
                break
            elif data_str[0] == 'X':
                result[f'{offset:04X}'] = data_str[:5]
                data_str = data_str[5:]
                offset += 1
            elif data_str[0] == 'N':
                result[f'{offset:04X}'] = data_str[:1]
                data_str = data_str[1:]
                offset += 1
            elif data_str[0] == ';':
                continue
            elif data_str[0] == '\n':
                break
            else:
                result[f'{offset:04X}'] = data_str[:2]
                data_str = data_str[2:]
                offset += 1
    return result


def create_address_dict(data_lst: list):
    result = {}
    while data_lst:
        current = data_lst.pop(0)
        if current[0] == '$':
            address = current[:5]
            current = current[5:]
            length = dict_len(current)
            result_dict = create_empty_dict(length)
            not_empty_dict = create_dict(current)
            result_dict.update(not_empty_dict)
            result[address] = result_dict
    return result


def create_parentdict(data: list) -> dict:
    result = {}
    for item in data:
        if item.startswith('$'):
            key = item[:5]
            value = item[5:]
            result[key] = value
    return result

def process_x(b: str, a='00'):
    """
    Накладывает X-запрос на байт, x - первый аргумент байт - второй
    Пример: process_x('X39C6', 'FF')
    :param b: str
    :param a: str
    :return: bin
    """
    x = int(a, 16)
    y1 = int(b[1:3], 16)
    y2 = int(b[3:], 16)
    res = x | y1
    res = res & ~y2
    return f'{res:02X}'


