import threading
import grpc
from proto import upload_pb2_grpc
from proto import upload_pb2
import time
from concurrent import futures
import base64
from pprint import pprint
import os

class Upload(upload_pb2_grpc.UploadServicer):

    def Fileup(self, request_iterator, context):
        def stream():
            while 1:
                ite = next(request_iterator)
                yield ite

        output_stream = stream()
        i = 0
        file_exist = False
        while 1:
            out_ite = next(output_stream)
            binary_data = base64.b64decode(out_ite.data)
            if (os.path.exists(out_ite.name) and i == 0) or file_exist:
                if i == 0:
                    print('{} already exists,So no copy this file.'.format(out_ite.name))
                file_exist = True
                pass
            else:
                os.mkdir(out_ite.name,exist_ok=True)
                file_name = os.path.basename(out_ite.name)
                with open(file_name, 'ab') as f:
                    f.write(binary_data)
            i += 1
            if i == out_ite.size and not file_exist:
                print('complete! {} '.format(out_ite.name))
            yield upload_pb2.Tdata(data = out_ite.data, size = out_ite.size, name = out_ite.name)
