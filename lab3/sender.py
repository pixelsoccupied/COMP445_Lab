#!/usr/bin/python
import socket
import argparse

def start(args):
    serverName = args.address
    serverPort = args.port
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    user_name = raw_input('Enter your name: ')
    while 1:
        message = raw_input('')
        modifiedMessage = build_message(user_name, message)
        clientSocket.sendto(modifiedMessage,(serverName, serverPort))
        serverMessage, serverAddress = clientSocket.recvfrom(2048)
        print serverMessage
    clientSocket.close()

def build_message(username, message):
    user_message = "user:" + username + "\n"
    user_message += "message:" + message + "\n\n"
    return user_message

parser = argparse.ArgumentParser()
parser.add_argument("-p", action="store", dest="port", help="Set server port", type=int, default=8080)
parser.add_argument("-a", action="store", dest="address", help="Set Server Name", default="127.0.0.1")
args = parser.parse_args()

start(args)
