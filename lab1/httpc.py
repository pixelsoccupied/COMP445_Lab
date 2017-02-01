from socket import *
import argparse
import sys


def run_client(args):
    print args
    return None
    conn = socket(AF_INET, SOCK_STREAM)
    try:
        conn.connect((host, port))
	conn.send("GET /status/418 HTTP/1.0\nHOST:Host: httpbin.org\n\n")
	response = conn.recv(1024)
	print 'From Server:', response
    finally:
        conn.close()


parser = argparse.ArgumentParser(add_help=False)
subparsers = parser.add_subparsers(help='commands')
get_parser = subparsers.add_parser('GET', help='get help')
get_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="")
get_parser.add_argument("-h", action="store", dest="headers", default=[], help="server port")

post_parser = subparsers.add_parser('POST', help='get help')
post_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="")
post_parser.add_argument("-h", action="store", dest="headers", default=[], help="server port")
group = post_parser.add_mutually_exclusive_group(required=False)
group.add_argument("-d", action="store", dest="inline", default="", help="")
group.add_argument("-f", action="store", dest="file", default="", help="")

args = parser.parse_args()
run_client(args)
