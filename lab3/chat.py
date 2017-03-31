#!/usr/bin/python

from receiver import Receiver
from sender import Sender
import argparse
from multiprocessing import Process

def start(args):
    #How do I get to run both sender and receiver at the same time ?
    #Essentially, every client has a sender and receiver that is shared on the same terminal.. How?
    Process(target = Receiver('', args.port))
    Process(target = Sender(args.address, args.port))


parser = argparse.ArgumentParser()
parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parser.add_argument("-a", action="store", dest="address", help="Set Server Name", default='255.255.255.255')
args = parser.parse_args()
start(args)
