import socket
import threading
import argparse
import os
import json
import glob
import time

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
            request_split = split_request(data)
            method_tuple = get_method(request_split[0])
            # print method_tuple
            if method_tuple[0] == "GET":
                print data
                send_get_data(request_split[0], conn, method_tuple[1])
                break
            elif method_tuple[0] == "POST":
                print data
                send_post_data(request_split, conn, method_tuple[1])
                break
            else:
                body = make_return_header(None, 0, "")
                conn.sendall(body)
                break

    finally:
        conn.close()

def split_request(data):
    return data.split("\r\n\r\n")

def get_method(headers):
    return headers.split()[:2]

def send_post_data(request, conn, path):
    path = path.replace("/","")
    print path
    print request
    if len(path) > 0 and len(request) == 2:
        try:
            filename = glob.glob(os.path.join(dir_path, path + '.*'))[0]
            print filename
            with open(filename, 'w') as myfile:
                myfile.write(request[1])
                data = make_return_header(True, 0, "")
        except IndexError, e:
            print e
            data = make_return_header(False, 0, "")
    else:
        data = make_return_header(False, 0, "")
    conn.sendall(data)

def send_get_data(headers, conn, path):
    path = path.replace("/","")
    if len(path) > 0:
        try:
            filename = glob.glob(os.path.join(dir_path, path + '.*'))[0]
            print filename
            with open(filename, 'r') as myfile:
                file_data = myfile.read()
                file_length = len(file_data)
                data = make_return_header(True, file_length, "text/plain")
                data += file_data + "\r\n"
        except IndexError, e:
            data = make_return_header(False, 0, "")
    else:
        file_data = json.dumps(os.listdir(dir_path))
        file_length = len(file_data)
        data = make_return_header(True, file_length, "text/plain")
        data += file_data + "\r\n"
    conn.sendall(data)

def make_return_header(ok, length, content_type):
    header_string = ""
    if ok is True:
        header_string += "HTTP/1.0 200 OK\r\n"
    elif ok is False:
        header_string += "HTTP/1.0 404 Not Found\r\n"
    else:
        header_string += "HTTP/1.0 400 Bad Request\r\n"

    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    header_string += "Date: " + current_date + "\r\n"
    header_string += "Server: Simple Python Server\r\n"

    if length > 0:
        header_string += "Content-Type: " + content_type + "\r\n"
        header_string += "Content-Length: " + str(length) + "\r\n"
    header_string += "\r\n"
    return header_string

# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8006)
args = parser.parse_args()
run_server('', args.port)
