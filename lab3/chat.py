#!/usr/bin/python

from receiver import Receiver
from sender import Sender
import argparse
from threading import Thread

def start(args):
    receiver = Receiver('', args.port)
    sender = Sender(args.address, args.port)
    receiver.start()
    sender.start()
    receiver.join()
    sender.join()

parser = argparse.ArgumentParser()
parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parser.add_argument("-a", action="store", dest="address", help="Set Server Name", default='255.255.255.255')
args = parser.parse_args()
start(args)
