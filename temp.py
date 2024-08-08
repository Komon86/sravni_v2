if offset - cursor != 0:  # Если запись производится не с нуля, то забиваем промежуток пробелами
    for i in range(offset - cursor):
        offsets.append('%04X' % cursor)