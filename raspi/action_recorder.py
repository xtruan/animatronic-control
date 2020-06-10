from pynput.keyboard import Key, Listener
import time

import utils.transform as transform

csv_file = open('rec.csv', 'w')
start = time.time()
key_mode = 0

def on_press(key):
    global csv_file, start, key_mode

    if key == Key.esc:
        # Stop listener
        return False

    if key_mode <= 0:
        key_mode = 1
        
        end = time.time()
        act = key_to_actuator(key)
        out_str = transform.time_stringify(end - start) + ',8,' + act + ',90'
        print(out_str)
        csv_file.write(out_str + '\n')

def on_release(key):
    global csv_file, start, key_mode
    if key_mode >= 0:
        key_mode = -1
        
        end = time.time()
        act = key_to_actuator(key)
        out_str = transform.time_stringify(end - start) + ',8,' + act + ',00'
        print(out_str)
        csv_file.write(out_str + '\n')

    if key == Key.backspace:
        print('--RESET--')
        csv_file.close()
        csv_file = open('rec.csv', 'w')
        start = time.time()

def key_to_actuator(key):
    key_str = str(key).replace("'", "")
    if key == Key.space:
        return 'SERVO,1'
    if key_str == 'a':
        return 'LIGHT,0'
    elif key_str == 's':
        return 'LIGHT,1'
    elif key_str == 'd':
        return 'LIGHT,2'
    elif key_str == 'f':
        return 'LIGHT,3'
    elif key_str == 'j':
        return 'LIGHT,4'
    elif key_str == 'k':
        return 'LIGHT,5'
    elif key_str == 'l':
        return 'LIGHT,6'
    elif key_str == ';':
        return 'LIGHT,7'
    else:
        return 'SERVO,1'

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()