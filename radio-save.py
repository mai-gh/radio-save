#!/usr/bin/env python3

# Intergalactic FM: Cybernetic Broadcasting System
#stream_url = 'http://radio.intergalactic.fm:80/1'

# Intergalactic FM: Disco Fetish
stream_url = 'http://radio.intergalactic.fm:80/2'

# Intergalactic FM: Dream Machine
#stream_url = 'http://radio.intergalactic.fm:80/3'

# XWave Radio
#stream_url = 'http://ns319459.ip-91-121-67.eu:8000'



from requests import get
from time import time


#import code
#code.interact(local=locals())
#import sys
#stream_url = sys.argv[1]


def rip():
    r = get(stream_url, headers={'Icy-MetaData': '1'}, stream=True)
    
    metaint = int(r.headers['icy-metaint'])
    byte_counter = 0
    stream_buffer = bytearray()
    metadata_buffer = bytearray()
    meta_start_pos = metaint + 1
    stream_title = ''
    file_size = 0
    extension = 'mp3'
    file_name = ''

    play_time = str(int(time()))
    
    for key, value in r.headers.items():
         print(key, ':', value)
    
    for byte in r.iter_content(1):
        byte_counter += 1
        if byte_counter <= metaint:
            stream_buffer.extend(byte)
        elif byte_counter == meta_start_pos:
            if stream_title:
                file_size += byte_counter
                file_name = play_time + ' ' + stream_title + '.' + extension
                file_name = file_name.replace('/', '\u2215').replace('\0', '')
                print('\r', "Saving File:", file_name, file_size, end='')
                f = open(file_name, 'ab')
                f.write(stream_buffer)
                f.close()
                stream_buffer = bytearray()
            byte_int = int.from_bytes(byte, 'little')
            metalen = byte_int * 16
            meta_end_pos = meta_start_pos + metalen
            if metalen == 0:
                byte_counter = 0
        elif byte_counter < meta_end_pos:
            metadata_buffer.extend(byte)
        elif byte_counter == meta_end_pos:
            metadata_buffer.extend(byte)
            if file_name:
                logf = open("logfile.txt", "a")
                logf.write(file_name + '\n')
                logf.close()
            stream_title = metadata_buffer.decode().split("StreamTitle='")[1].rsplit("';")[0]
            play_time = str(int(time()))
            print()
            #print("Now Playing:", stream_title)
            metadata_buffer = bytearray()
            byte_counter = 0
            file_size = 0


if __name__ == '__main__':
    while True:
        rip()

