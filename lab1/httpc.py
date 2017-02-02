#Example Usage
#python httpc.py get -u 'http://httpbin.org/get?course=networking&assignment=1%27'
#python httpc.py get -hd Accept:application/json -v -u 'http://httpbin.org/get?course=networking&assignment=1%27'

from socket import *
import argparse
import sys
from urlparse import urlparse
import json

def run_client(args):
    print args
    request_string = ""

    if not validate_url(args.url):
        return None

    if args.which == "get":
        request_string = build_get(args)
    elif args.which == "post":
        request_string = build_post(args)
    else:
        print "Method was not recognized"
        return None
    conn = socket(AF_INET, SOCK_STREAM)
    try:
        conn.connect((args.url.netloc, 80))
        print request_string
        conn.send(request_string)
        response = conn.recv(1024)
        response = build_verbose(args, response)
        print "** Server Response **"
        print response
    finally:
        conn.close()

def build_get(args):
    query_params = "/"
    if not args.url.query == "":
        query_params = "?" + args.url.query
    request_string = "GET " + args.url.path + query_params + " HTTP/1.0" + build_headers(args) + "\n\n"
    return request_string

def build_post(args):
    request_string = "POST " + args.url.path + " HTTP/1.0" + build_headers(args) + "\n\n"
    return request_string

def build_headers(args):
    header_string = "\nHOST: " + args.url.netloc
    if len(args.headers) > 0:
        for head in args.headers:
            split_head = head.split(":")
            if len(split_head) == 2:
                header_string = header_string + "\n" + split_head[0] + ": " + split_head[1]
    return header_string

def build_verbose(args, response):
    #print repr(response)
    #return response

    if args.verbose == True:
        return response.split("\r\n\r\n", 1)[1]
    else:
        return response

def validate_url(url):
    if url.netloc == "":
        return False
    else:
        return True

#Build the argument parser
parser = argparse.ArgumentParser(description="httpc is a curl-like application but supports HTTP protocol only.")
subparsers = parser.add_subparsers(help='commands')
get_parser = subparsers.add_parser('get', help='Executes a HTTP GET request and prints the response.')
get_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="Prints the detail of the response such as protocol, status, and headers.")
get_parser.add_argument("-hd", action="store", nargs='*', dest="headers", default=[], help="Associates headers to HTTP Request with the format 'key:value'.")
get_parser.add_argument("-u", action="store", dest="url", type=urlparse, required=True, help="Requested URL")
get_parser.set_defaults(which='get')

post_parser = subparsers.add_parser('post', help='Executes a HTTP POST request and prints the response.')
post_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="Prints the detail of the response such as protocol, status, and headers.")
post_parser.add_argument("-hd", action="store", nargs='*', dest="headers", default=[], help="Associates headers to HTTP Request with the format 'key:value'.")
group = post_parser.add_mutually_exclusive_group(required=False)
group.add_argument("-d", action="store", dest="data", default="", type=json.loads, help="Associates an inline data to the body HTTP POST.")
group.add_argument("-f", action="store", dest="file", default="", help="Associates the content of a file to the body HTTP.")
post_parser.add_argument("-u", action="store", dest="url", type=urlparse, required=True, help="Requested URL")
post_parser.set_defaults(which='post')

args = parser.parse_args()
run_client(args)
