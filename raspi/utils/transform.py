
def time_convert(time_str):
    time_list = time_str.split(':')
    return float(int(time_list[0]) * 3600 + int(time_list[1]) * 60 + float(time_list[2]))
