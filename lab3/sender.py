#!/usr/bin/python
import socket

class Sender:
    def __init__(self, address, port):
        self.start(address, port)

    def start(self, address, port):
        print "Sender using: " + address + ":" + str(port)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        user_name = raw_input('Enter your name: ')

        while 1:
            message = raw_input('')
            modifiedMessage = self.build_message(user_name, message)
            clientSocket.sendto(modifiedMessage,(address, port))
            serverMessage, serverAddress = clientSocket.recvfrom(2048)
            print serverMessage
        clientSocket.close()

    def build_message(self, username, message):
        user_message = "user:" + username + "\n"
        user_message += "message:" + message + "\n\n"
        return user_message
