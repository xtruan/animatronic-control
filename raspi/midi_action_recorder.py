import pygame.midi
import time

csv_file = open('rec.csv', 'w')
import time
import utils.transform as transform

import pygame.midi

def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n,pygame.midi.get_device_info(n))

def note_to_actuator(note):
    if note == 62:
        return '8,LIGHT,0'
    elif note == 64:
        return '8,LIGHT,1'
    elif note == 65:
        return '8,LIGHT,2'
    elif note == 67:
        return '8,LIGHT,3'
    elif note == 69:
        return '8,LIGHT,4'
    elif note == 71:
        return '8,LIGHT,5'
    elif note == 72:
        return '8,LIGHT,6'
    elif note == 74:
        return '8,LIGHT,7'
    else:
        return '4,SERVO,1'

def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number % 12]

def read_input(input_device, player):
    global csv_file
    while True:
        if input_device.poll():
            event = input_device.read(1)[0]
            data = event[0]
            timestamp = event[1]
            
            note_number = data[1]
            velocity = data[2]

            if velocity != 0:
                player.note_on(note_number, velocity)

                if note_number == 48:
                    csv_file.close()
                    break

                act = note_to_actuator(note_number)
                out_str = transform.time_ms_stringify(timestamp) + ',' + act + ',90'
                print(out_str)
                csv_file.write(out_str + '\n')

            else:
                player.note_off(note_number, velocity)

                act = note_to_actuator(note_number)
                out_str = transform.time_ms_stringify(timestamp) + ',' + act + ',00'
                print(out_str)
                csv_file.write(out_str + '\n')

                if note_number == 79:
                    print('--RESET--')
                    csv_file.close()
                    csv_file = open('rec.csv', 'w')

            # note = number_to_note(note_number)
            # print(note, note_number, velocity)

if __name__ == '__main__':
    pygame.midi.init()
    print_devices()

    player = pygame.midi.Output(0)
    player.set_instrument(0)

    device = pygame.midi.Input(1)
    read_input(device, player)