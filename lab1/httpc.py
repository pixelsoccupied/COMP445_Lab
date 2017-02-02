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


parser = argparse.ArgumentParser(description="httpc is a curl-like application but supports HTTP protocol only.")
subparsers = parser.add_subparsers(help='commands')
get_parser = subparsers.add_parser('get', help='Executes a HTTP GET request and prints the response.')
get_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="Prints the detail of the response such as protocol, status, and headers.")
get_parser.add_argument("-hd", action="store", nargs='*', dest="headers", default=[], help="Associates headers to HTTP Request with the format 'key:value'.")
get_parser.add_argument("-u", action="store", dest="url", required=True, help="Requested URL")

post_parser = subparsers.add_parser('post', help='Executes a HTTP POST request and prints the response.')
post_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="Prints the detail of the response such as protocol, status, and headers.")
post_parser.add_argument("-hd", action="store", nargs='*', dest="headers", default=[], help="Associates headers to HTTP Request with the format 'key:value'.")
group = post_parser.add_mutually_exclusive_group(required=False)
group.add_argument("-d", action="store", dest="data", default="", help="Associates an inline data to the body HTTP POST.")
group.add_argument("-f", action="store", dest="file", default="", help="Associates the content of a file to the body HTTP.")
post_parser.add_argument("-u", action="store", dest="url", required=True, help="Requested URL")

args = parser.parse_args()
run_client(args)
