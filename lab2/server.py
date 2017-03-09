import socket
import threading
import argparse
import os
import json
import glob

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/data"

def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    print 'New client from', addr
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            headers = get_headers(data)
            method_tuple = get_method(headers)
            print method_tuple
            if method_tuple[0] == "GET":
                print data
                send_get_data(headers, conn, method_tuple[1])

    finally:
        conn.close()

def get_headers(data):
    return data.split("\r\n")[0]

def get_method(headers):
    return headers.split()[:2]

def send_get_data(headers, conn, path):
    path = path.replace("/","")
    if len(path) > 0:
        try:
            filename = glob.glob(os.path.join(dir_path, path + '.*'))[0]
            print filename
            with open(filename, 'r') as myfile:
                data = 'HTTP/1.0 200 OK\r\n'
                data = data + "Content-Type: text/plain\r\n\r\n"
                data = data + myfile.read()
        except IndexError, e:
            data = 'HTTP/1.0 404 Not Found\r\n'
    else:
        data = 'HTTP/1.0 200 OK\r\n'
        data = data + "Content-Type: application/json\r\n\r\n"
        data += json.dumps(os.listdir(dir_path))
    conn.sendall(data)



# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8006)
args = parser.parse_args()
run_server('', args.port)
