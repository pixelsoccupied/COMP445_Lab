#!/usr/bin/python
import socket
import datetime

class Receiver:
    def __init__(self, address, port):
        self.start(address, port)

    def start(self, address, port):
        print "Receiver using: " + address + ":" + str(port)
        receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiverSocket.bind((address, port))
        while 1:
            message, clientAddress = receiverSocket.recvfrom(2048)
            modifiedMessage = self.parse_message(message)
            receiverSocket.sendto(modifiedMessage, clientAddress);

    def parse_message(self, message):
        message_split = message.split("\n")
        user_name = message_split[0].split(":")[1]
        message_content = message_split[1].split(":")[1]
        print "Received: " + message_content;
        now = datetime.datetime.now()
        return str(now) + " [" + user_name + "]: " + message_content
