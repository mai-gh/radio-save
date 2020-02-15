# radio-save.py

### description:
this program downloads a shoutcast / icecast mp3 radio stream, and 
saves the songs to the streamtitle name that was sent during the 
broadcast. all files are saved to the current directory, and file 
names are also saved to a logfile after the song is over.

i made this to replace the program streamripper 


### how to use:
read the code before using.
```bash
./radio-save.py <http_url>
```

or

```bash
./radio-save.py xwave
```


### links that were helpful:
  * [https://web.archive.org/web/20170624182814/https://www.smackfu.com/stuff/programming/shoutcast.html]
  * [https://stackoverflow.com/questions/41022893/monitoring-icy-stream-metadata-title-python]
  * [https://en.wikipedia.org/wiki/Filename#Comparison_of_filename_limitations]
  * [http://dir.xiph.org/search?search=wave]


### bugs i might fix / features i might add:
  * TODO: find a work-around for streamripper relays / HTTP/0.9
  * TODO: temporary files
  * TODO: ogg support
  * TODO: make http server that relays the stream


### intentionally didnt do
windows filename support. the problem here is that you are using windows.



