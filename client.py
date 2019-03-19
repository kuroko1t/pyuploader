#MIT License
#
#Copyright (c) 2018 kurosawa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import threading
import grpc
import time
import codecs
from pprint import pprint
from tqdm import tqdm
import base64
import os
import argparse
from proto import upload_pb2_grpc
from proto import upload_pb2

def getfile(path,chunksize):
    readsize = 0
    filesize = os.path.getsize(path)
    data =[]
    i = 0
    with open(path,'rb') as f:
        while readsize < filesize:
            f.seek(readsize)
            data_chunk = f.read(chunksize)
            data.append(base64.b64encode(data_chunk))
            data_size = len(data_chunk)
            readsize = readsize + data_size
    return data

def run(tf_file, path, ip):
    channel = grpc.insecure_channel('{}:50053'.format(ip))
    stub = upload_pb2_grpc.UploadStub(channel)
    print(path)

    def stream():
        for tf in tf_file:
            yield upload_pb2.Tdata(data=tf,size=len(tf_file), name = path)

    input_stream = stub.Fileup(stream())

    def read_incoming():
        next(input_stream).name
    for tf in tf_file:
        read_incoming()
