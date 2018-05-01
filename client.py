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
    print('client connected')

    def stream():
        for tf in tf_file:
            yield upload_pb2.Tdata(data=tf,size=len(tf_file), name = path)

    input_stream = stub.Fileup(stream())

    def read_incoming():
        next(input_stream).name
    for tf in tqdm(tf_file):
        read_incoming()
