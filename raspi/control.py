from collections import deque
import csv
import argparse
import time

import utils.transform as transform
import utils.i2c as i2c
from objects.anim_action import AnimAction

COL_TIME_STR = 0
COL_DEVICE_TYPE = 1
COL_DEVICE_ID = 2
COL_SETTING = 3

anim_actions = deque([])

def read_anim_csv(filename, delimiter=',', quotechar='"'):
    csv_file = open(filename, 'r')
    csv_reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)

    for row in csv_reader:
        time_str = str(row[COL_TIME_STR])
        time_sec = transform.time_convert(time_str)
        device_type = str(row[COL_DEVICE_TYPE])
        device_id = str(row[COL_DEVICE_ID])
        setting = str(row[COL_SETTING])
        
        action = AnimAction(time_str, time_sec, device_type, device_id, setting)
        anim_actions.append(action)        

    csv_file.close()

def handle_anim():
    start = time.time()
    end = time.time()
    while len(anim_actions) > 0:
        if anim_actions[0].time_sec <= end - start:
            handle_action(anim_actions.popleft())
        time.sleep(0.001)
        end = time.time()

def handle_action(action):
    i2c.write_anim_i2c(action)
    print(action)

def main():
    parser = argparse.ArgumentParser(description="Animatronic Control Program")
    parser.add_argument('-i', '--input', type=str, required=True)
    args = parser.parse_args()

    input_file = args.input
    print('Input file: ' + input_file)
    if '.csv' in input_file.lower():
        print('Loading file...')
        read_anim_csv(input_file)
        print('Loaded!')
        wait = input('Press enter to continue...')
        handle_anim()
    else:
        raise Exception('Invalid file type')

if __name__ == '__main__':
    main()
