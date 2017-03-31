#!/usr/bin/python
import socket
from threading import Thread

class Sender(Thread):

    def __init__(self, address, port):
        Thread.__init__(self)
        self.port = port
        self.address = address
        self.thread_on = True

    def run(self):
        #print "Sender using: " + self.address + ":" + str(self.port) + "\n"
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        username = raw_input('Enter your name: ')

        while self.thread_on == True:
            message = raw_input('')
            if message == "BYE":
                self.thread_on = False
            modifiedMessage = self.build_message(username, message)
            clientSocket.sendto(modifiedMessage,(self.address, self.port))
            # serverMessage, serverAddress = clientSocket.recvfrom(2048)
            # print serverMessage
        print "Closing Sender"
        clientSocket.close()

    def build_message(self, username, message):
        user_message = "user:" + username + "\n"
        user_message += "message:" + message + "\n\n"
        return user_message
