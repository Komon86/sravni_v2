def process_x(b, a='00'):
    x=int(a, 16)
    y1=int(b[1:3], 16)
    y2=int(b[3:], 16)
    res=x | y1
    res=res & ~y2
    return bin(res)