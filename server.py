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
from proto import upload_pb2_grpc
from proto import upload_pb2
import time
from concurrent import futures
import base64
from pprint import pprint
import os
import re

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
                if re.search('/',out_ite.name):
                    os.makedirs(os.path.dirname(out_ite.name),exist_ok=True)
                    file_name = out_ite.name
                else:
                    file_name = out_ite.name
                with open(file_name, 'ab') as f:
                    f.write(binary_data)
            i += 1
            if i == out_ite.size and not file_exist:
                print('complete! {} '.format(out_ite.name))
            yield upload_pb2.Tdata(data = out_ite.data, size = out_ite.size, name = out_ite.name)
