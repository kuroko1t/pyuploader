# pyuploader
Transfer file to another server.
This script using grpc protocol.

# Usage
waiting file..
```
$python uploader.py -s
```
upload file to waiting server 
```
$python uploader.py filename -i 192.168.10.5
```
help
```
$python uploader.py -h
usage: uploader.py [-h] [-s] [-i IP] [f]

This script is uploading file to another server

positional arguments:
  f               file name you want to transfer

optional arguments:
  -h, --help      show this help message and exit
  -s, --serve     for serve file
  -i IP, --ip IP  ip address of uploading server
```

# License
MIT
