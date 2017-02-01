from socket import *
import argparse
import sys


def run_client(host, port):
    conn = socket(AF_INET, SOCK_STREAM)
    try:
        conn.connect((host, port))
	conn.send("GET /status/418 HTTP/1.0\nHOST:Host: httpbin.org\n\n")
	response = conn.recv(1024)
	print 'From Server:', response
    finally:
        conn.close()


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="httpbin.org")
parser.add_argument("--port", help="server port", type=int, default=80)
args = parser.parse_args()
run_client(args.host, args.port)
