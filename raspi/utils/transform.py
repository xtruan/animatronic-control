import time

def time_floatify(time_str):
    time_list = time_str.split(':')
    return float(int(time_list[0]) * 3600 + int(time_list[1]) * 60 + float(time_list[2]))

def time_stringify(time_secs):
    frac = float(time_secs) - int(time_secs)
    frac = int(frac * 1000)
    return time.strftime('%H:%M:%S', time.gmtime(time_secs)) + '.' + str(frac)
    
