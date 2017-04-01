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
        self.send_message(clientSocket, "", username, "JOIN")
        self.send_message(clientSocket, "", username, "PING")

        while self.thread_on == True:
            message = raw_input('')
            if message == "/leave":
                self.thread_on = False
                self.send_message(clientSocket, "", username, "LEAVE")
                self.send_message(clientSocket, "", username, "QUIT")
            elif message == "/who":
                self.send_message(clientSocket, "", username, "WHO")
            else:
                self.send_message(clientSocket, message, username, "TALK")
            # serverMessage, serverAddress = clientSocket.recvfrom(2048)
            # print serverMessage
        # print "Closing Sender"
        clientSocket.close()

    def send_message(self, clientSocket, message, username, command):
        messageaddress = self.address
        if command == "WHO" or command == "QUIT":
            messageaddress = "127.0.0.1"

        modifiedMessage = self.build_message(username, message, command)
        clientSocket.sendto(modifiedMessage,(messageaddress, self.port))

    def build_message(self, username, message, command):
        user_message = "user:" + username + "\n"
        user_message += "command:" + command + "\n"
        user_message += "message:" + message + "\n\n"
        return user_message
