from pynput.keyboard import Key, Listener
import time

import utils.transform as transform

csv_file = open('rec.csv', 'w')
start = time.time()
key_mode = 0

def on_press(key):
    global csv_file, start, key_mode
    if key_mode <= 0:
        key_mode = 1
        
        end = time.time()
        out_str = transform.time_stringify(end - start) + ',SVO,2,90'
        print(out_str)
        csv_file.write(out_str + '\n')

def on_release(key):
    global csv_file, start, key_mode
    if key_mode >= 0:
        key_mode = -1
        
        end = time.time()
        out_str = transform.time_stringify(end - start) + ',SVO,2,00'
        print(out_str)
        csv_file.write(out_str + '\n')

    if key == Key.esc:
        # Stop listener
        return False
    if key == Key.backspace:
        print('--RESET--')
        csv_file.close()
        csv_file = open('rec.csv', 'w')
        start = time.time()

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()