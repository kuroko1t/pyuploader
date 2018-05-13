import argparse
import client
import server
import threading
import grpc
from proto import upload_pb2_grpc
from proto import upload_pb2
from concurrent import futures
import time
import os

def serve():
    fserver = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    upload_pb2_grpc.add_UploadServicer_to_server(
        server.Upload(), fserver)

    fserver.add_insecure_port('[::]:50053')
    fserver.start()
    print('file waiting...')
    while 1:
        time.sleep(1)

def client_run(path, ip):
    chunksize = 1000000
    path = args.f
    tf_file = client.getfile(path, chunksize)
    #file_name = os.path.basename(path)
    #client.run(tf_file, file_name, ip)
    client.run(tf_file, path, ip)
    print('done!')

def client_all(paths, ip):
    if os.path.isdir(paths):
        dir_exist = True
        base_dir = paths.split("/")[-1]
        if base_dir == "":
            base_dir = paths.split("/")[-2]
        paths = [paths]
        while(dir_exist):
            dir_exist = False
            tmp_paths = []
            for path in paths:
                for files in os.listdir(path):
                    if os.path.isdir(path + files):
                        tmp_paths.append(path +  files + "/")
                        dir_exist = True
                    else:
                        #print(path + files)
                        pass
            paths = tmp_paths
    else:
        client_run(paths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This script is uploading file to another server',
        add_help=True)
    parser.add_argument('f', help='file name you want to transfer',
                        type=str,nargs='?')
    parser.add_argument('-s', '--serve', help='for serve file',
                    action='store_true')
    parser.add_argument('-i', '--ip', help='ip address of uploading server',
                        type=str)
    args = parser.parse_args()
    if args.serve:
            serve()
    else:
        if args.ip:
            #client_run(args.f, args.ip)
            client_all(args.f, args.ip)
        else:
            print('please set ip adress')
