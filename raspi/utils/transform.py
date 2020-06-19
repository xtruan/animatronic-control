import time

def time_floatify(time_str):
    time_list = time_str.split(':')
    return float(int(time_list[0]) * 3600 + int(time_list[1]) * 60 + float(time_list[2]))

def time_stringify(time_secs):
    frac = float(time_secs) - int(time_secs)
    frac = int(frac * 1000)

    frac_str = ''
    if frac < 10:
        frac_str = str(frac) + '00'
    elif frac < 100:
        frac_str = str(frac) + '0'
    else:
        frac_str = str(frac)

    return time.strftime('%H:%M:%S', time.gmtime(time_secs)) + '.' + frac_str

def time_ms_stringify(time_ms):
    time_secs = time_ms / 1000.0
    return time_stringify(time_secs)
    
