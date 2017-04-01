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
        self.users = []

    def run(self):
        # print "Receiver using: " + self.address + ":" + str(self.port) + "\n"
        receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiverSocket.bind((self.address, self.port))
        self.socket_address = socket.gethostbyname(socket.gethostname())
        # print self.socket_address

        while self.thread_on == True:
            message, clientAddress = receiverSocket.recvfrom(2048)
            # print clientAddress
            message_content = self.split_message(message)
            modifiedMessage = self.parse_message(message_content)

            if modifiedMessage is not None:
                if message_content[1] == "QUIT":
                    self.thread_on = False
                print modifiedMessage

        # print "Closing Receiver"

    def split_message(self, message):
        # print message
        message_split = message.split("\n")
        user_name = message_split[0].split(":")[1]
        command = message_split[1].split(":")[1]
        message_content = message_split[2].split(":")[1]
        return (user_name, command, message_content)

    def parse_message(self, message_content):
        now = datetime.datetime.now()
        command = message_content[1]
        if command == "JOIN":
            self.users.append(message_content[0])
            return str(now) + " " + message_content[0] + " joined!"
        elif command == "TALK":
            return str(now) + " [" + message_content[0] + "]: " + message_content[2]
        elif command == "LEAVE":
            self.users.remove(message_content[0])
            return str(now) + " " + message_content[0] + " leaved!"
        elif command == "WHO":
            return str(now) + " Connected users: " + str(self.users)
        else:
            return None
