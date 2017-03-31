#!/usr/bin/python
import socket
import datetime
from threading import Thread

class Receiver(Thread):
    def __init__(self, address, port):
        Thread.__init__(self)
        self.address = address
        self.port = port
        self.thread_on = True

    def run(self):
        # print "Receiver using: " + self.address + ":" + str(self.port) + "\n"
        receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiverSocket.bind((self.address, self.port))

        while self.thread_on == True:
            message, clientAddress = receiverSocket.recvfrom(2048)
            message_content = self.split_message(message)
            modifiedMessage = self.parse_message(message_content)
            if message_content[1] == "BYE":
                self.thread_on = False
            else:
                print modifiedMessage
        print "Closing Receiver"
            # receiverSocket.sendto(modifiedMessage, clientAddress);
    def split_message(self, message):
        message_split = message.split("\n")
        user_name = message_split[0].split(":")[1]
        message_content = message_split[1].split(":")[1]
        return (user_name, message_content)

    def parse_message(self, message_content):
        now = datetime.datetime.now()
        return str(now) + " [" + message_content[0] + "]: " + message_content[1]
