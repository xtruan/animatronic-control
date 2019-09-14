from collections import deque
import csv
import argparse
import time

import utils.transform as transform
import utils.i2c as i2c
from objects.anim_action import AnimAction

COL_TIME_STR = 0
COL_DEVICE_I2C_ADDR = 1
COL_DEVICE_TYPE = 2
COL_DEVICE_ID = 3
COL_SETTING = 4

anim_actions = deque([])

def read_anim_csv(filename, delimiter=',', quotechar='"'):
    csv_file = open(filename, 'r')
    csv_reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)

    for row in csv_reader:
        time_str = str(row[COL_TIME_STR])
        time_sec = transform.time_floatify(time_str)
        device_i2c_addr = int(row[COL_DEVICE_I2C_ADDR])
        device_type = str(row[COL_DEVICE_TYPE])
        device_id = int(row[COL_DEVICE_ID])
        setting = int(row[COL_SETTING])
        
        action = AnimAction(time_str, time_sec, device_i2c_addr, device_type, device_id, setting)
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

def record_mode():
    start = time.time()
    rec_action = AnimAction(transform.time_stringify(start), start, 8, 'RECORD', 0, 0)
    i2c.write_anim_i2c(rec_action)

def record_to_csv(output_file):
    start = time.time()
    rec_action = AnimAction(transform.time_stringify(start), start, 8, 'RECORD', 0, 0)
    csv_file = open(output_file, 'w')

    while True:
        data = i2c.read_mecca_i2c(rec_action.device_i2c_addr)
        end = time.time()
        str_time = transform.time_stringify(end - start)

        if (data[0] == 0):
            for i in range (1, 6):
                j = i * 2
                out_str = str_time + ',' + str(rec_action.device_i2c_addr) + ',MEC,' + str(data[j - 1]) + ',' + str(data[j])
                print(out_str)
                csv_file.write(out_str + '\n')
        
        time.sleep(0.5)

def main():
    parser = argparse.ArgumentParser(description="Animatronic Control Program")
    parser.add_argument('-i', '--input', type=str, required=False)
    parser.add_argument('-o', '--output', type=str, required=False)
    args = parser.parse_args()

    if args.input is not None:
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
    elif args.output is not None:
        output_file = args.output
        print('Output file: ' + output_file)
        if '.csv' in output_file.lower():
            print('Enabling recording...')
            record_mode()
            print('Enabled!')
            wait = input('Press enter to continue...')
            record_to_csv(output_file)
    else:
        print('Nothing to do!')

if __name__ == '__main__':
    main()
