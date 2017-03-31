#!/usr/bin/python
import socket
import datetime
import argparse

def start(args):
    receiverPort = args.port
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiverSocket.bind((args.address, receiverPort))

    while 1:
        message, clientAddress = receiverSocket.recvfrom(2048)
        modifiedMessage = parse_message(message)
        receiverSocket.sendto(modifiedMessage, clientAddress);

def parse_message(message):
    message_split = message.split("\n")
    user_name = message_split[0].split(":")[1]
    message_content = message_split[1].split(":")[1]
    now = datetime.datetime.now()
    return str(now) + " [" + user_name + "]: " + message_content

parser = argparse.ArgumentParser()
parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parser.add_argument("-a", action="store", dest="address", help="Set Server Name", default='')
args = parser.parse_args()

start(args)
