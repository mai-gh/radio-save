#!/usr/bin/env python3

from requests import get
from time import time
from sys import argv
from datetime import datetime
from os import popen

if len(argv) > 1:
    if argv[1] == 'xwave':
        stream_url = 'http://ns319459.ip-91-121-67.eu:8000'
    elif argv[1] == 'ifm1':
        stream_url = 'http://radio.intergalactic.fm:80/1'
    elif argv[1] == 'ifm2':
        stream_url = 'http://radio.intergalactic.fm:80/2'
    elif argv[1] == 'ifm3':
        stream_url = 'http://radio.intergalactic.fm:80/3'
    elif (argv[1].split(':')[0] == 'http') or (argv[1].split(':')[0] == 'https'):
        stream_url = argv[1]
    else:
        print('invalid stream:', argv[1])
        exit()
else:
    print('must provide a stream as the only argument')
    exit()

def rip():
    r = ''
    while not r:
        try:
            r = get(stream_url, headers={'Icy-MetaData': '1'}, stream=True, timeout=10)
        except:
            print('there was a problem connecting to the stream')
            
    metaint = int(r.headers['icy-metaint'])
    bitrate = int(r.headers['icy-br'].split(', ')[0])
    stream_buffer = bytearray()
    stream_byte_counter = 0
    extension = 'mp3'
    mp3_file_name = ''
    sec_save_interval = 15
    bytes_per_second = (bitrate * 1024) / 8
    mp3_write_chunk_size = bytes_per_second * sec_save_interval

    all_current_headers = ''
    for key, value in r.headers.items():
         this_header_string = key + ' : ' + value
         all_current_headers += this_header_string + '\n'

    header_file_name = str(int(time())) + ' ' + 'headers' + '.' + 'txt'
    with open(header_file_name, "w") as headerf:
         headerf.write(all_current_headers)
    print(all_current_headers)

    while True:
        for mp3_chunk in r.iter_content(chunk_size=metaint):
            stream_buffer.extend(mp3_chunk)
            stream_byte_counter += metaint
            time_now = str(datetime.now()).split('.')[0]
            columns = int(popen('stty size', 'r').read().split()[1])
            name_size = columns - 19 - 10 - 4
            pstr = time_now # 19 chars
            pstr += " "
            pstr += mp3_file_name[0:name_size]
            pstr += " "
            pstr += str(stream_byte_counter) # assume this is 10 chars
            pstr += " "
            pstr += str(int(stream_byte_counter / bytes_per_second)) # 4chars
            print(pstr, end='\r')
            break
        for metalen_byte in r.iter_content(chunk_size=1):
            metalen = int.from_bytes(metalen_byte, 'little') * 16
            break
        if mp3_file_name and (len(stream_buffer) >= mp3_write_chunk_size):
                with open(mp3_file_name, 'ab') as f:
                    f.write(stream_buffer)
                stream_buffer = bytearray()
        if metalen > 0:
            if mp3_file_name:
                with open(mp3_file_name, 'ab') as f:
                    f.write(stream_buffer)
                stream_buffer = bytearray()
                with open("logfile.txt", "a") as logf:
                    logf.write(mp3_file_name + '\n')
            for meta_chunk in r.iter_content(chunk_size=metalen):
                stream_title = meta_chunk.decode().split("StreamTitle='")[1].rsplit("';")[0]
                title_change_time = str(int(time()))
                mp3_file_name = title_change_time + ' ' + stream_title + '.' + extension
                mp3_file_name = mp3_file_name.replace('/', '\u2215').replace('\0', '')
                print()
                stream_byte_counter = 0
                break
#rip()
if __name__ == '__main__':
    while True:
        try:
            rip()
        except KeyboardInterrupt:
            print()
            exit()
        except:
            print("error with rip()")
            pass

