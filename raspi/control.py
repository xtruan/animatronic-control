from collections import deque
import csv
import argparse
import time

from playsound import playsound
import mido

import utils.transform as transform
#import utils.i2c as i2c
from objects.anim_action import AnimAction

COL_TIME_STR = 0
COL_DEVICE_I2C_ADDR = 1
COL_DEVICE_TYPE = 2
COL_DEVICE_ID = 3
COL_SETTING = 4

anim_actions = deque([])
action_viz = {}
mid_notes = {}

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
        add_action = True
        if len(anim_actions) > 0:
            last_action = anim_actions[-1]
            if action.device_i2c_addr == last_action.device_i2c_addr and \
                action.device_id == last_action.device_id and \
                action.device_type == last_action.device_type and \
                action.setting == last_action.setting:
                add_action = False

        if add_action:
            anim_actions.append(action)        

    csv_file.close()

def build_anim_action_from_mid_msg(time_sec, msg):
    try:
        time_str = str(transform.time_stringify(time_sec))
        device_i2c_addr = 8
        device_type = 'LIGHT'
        device_id = mid_note_to_device_id(msg.note)
        if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            setting = 0
        else:
            setting = 1

        return AnimAction(time_str, time_sec, device_i2c_addr, device_type, device_id, setting)
    except AttributeError:
        pass
    
def mid_note_to_device_id(note):
    if note not in mid_notes:
        mid_notes[note] = len(mid_notes)
    return mid_notes[note]

def read_anim_mid(filename):
    mid = mido.MidiFile(filename)
    
    ret_offset = 0.0
    time_sec = 0.0
    for msg in mid:
        time_sec += msg.time
        if not msg.is_meta:
            action = build_anim_action_from_mid_msg(time_sec, msg)
            if action is not None:
                add_action = True
                if len(anim_actions) > 0:
                    last_action = anim_actions[-1]
                    if action.device_i2c_addr == last_action.device_i2c_addr and \
                        action.device_id == last_action.device_id and \
                        action.device_type == last_action.device_type and \
                        action.setting == last_action.setting:
                        add_action = False

                if add_action:
                    anim_actions.append(action)
        else:
            if '[music_start]' in str(msg):
                ret_offset = time_sec * -1.0
            print(msg)
    
    return ret_offset

def handle_anim(offset=0.0):
    print('Playing...')
    print()

    start = time.time() + offset
    end = time.time()
    while len(anim_actions) > 0:
        if anim_actions[0].time_sec <= end - start:
            handle_action(anim_actions.popleft())
        time.sleep(0.001)
        end = time.time()

def handle_action(action):
    #i2c.write_anim_i2c(action)
    
    if action.setting == 0:
        action_viz[action.device_id] = '   '
    else:
        action_viz[action.device_id] = 'XXX'
    
    print('\r{}'.format('  '.join(action_viz.values())), end="")

def main():
    parser = argparse.ArgumentParser(description="Animatronic Control Program")
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-a', '--audio', type=str, required=True)
    args = parser.parse_args()

    input_file = args.input
    audio_file = args.audio
    print('Input file: ' + input_file)
    if '.csv' in input_file.lower():
        print('Loading file...')
        read_anim_csv(input_file)
        print('Loaded!')
        wait = input('Press enter to continue...')

        playsound(audio_file, False)

        handle_anim()
    if '.mid' in input_file.lower():
        print('Loading file...')
        offset = read_anim_mid(input_file)
        print('Loaded! (offset = ' + str(offset) + ')')
        wait = input('Press enter to continue...')

        playsound(audio_file, False)

        handle_anim(offset=offset)

        # DEBUGGING
        # notes = {}
        # note_count = {}
        # for msg in mid:
        #     if not msg.is_meta:
        #         time.sleep(msg.time)
        #         #print(str(msg))
        #         try:
        #             if msg.velocity == 0:
        #                 notes[msg.note] = '   '
        #             else:
        #                 notes[msg.note] = 'XXX'
        #                 if msg.note not in note_count:
        #                     note_count[msg.note] = -1
        #                 note_count[msg.note] += 1
        #             print(str(notes))
        #             print(str(note_count))
        #         except AttributeError:
        #             pass
        
    else:
        raise Exception('Invalid file type')

    time.sleep(5)

if __name__ == '__main__':
    main()
