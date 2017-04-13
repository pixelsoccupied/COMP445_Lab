#!/usr/bin/python
import socket
from threading import Thread
import re
import datetime

class Sender(Thread):

    def __init__(self, address, port):
        Thread.__init__(self)
        self.port = port
        self.broadcast = address
        self.thread_on = True
        self.channel = "general"

    def run(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket_address = socket.gethostbyname(socket.gethostname())
        username = raw_input('Enter your name: ')
        self.send_message(clientSocket, "", username.strip(), "JOIN")

        while self.thread_on == True:
            message = raw_input('')
            message = message.strip()

            if message == "/leave":
                self.thread_on = False
                self.send_message(clientSocket, "", username, "LEAVE")
                self.send_message(clientSocket, "", username, "QUIT")

            elif message == "/who":
                self.send_message(clientSocket, "", username, "WHO")

            elif re.match(r'^\/private\s.*$', message) is not None:
                user_to_send = message.replace("/private ", "").strip()
                message_to_send = raw_input('Private message to send to ' + user_to_send + ": ")
                user_string = username + ":" + user_to_send
                self.send_message(clientSocket, message_to_send, user_string, "PRIVATE-TALK")

            elif re.match(r'^\/channel\s.*$', message) is not None:
                self.channel = message.replace("/channel ", "").strip()
                print str(datetime.datetime.now()) + " Switched to channel " + self.channel

            else:
                self.send_message(clientSocket, message, username, "TALK")

        clientSocket.close()

    def send_message(self, clientSocket, message, username, command):
        messageaddress = self.broadcast
        if command == "WHO" or command == "QUIT" or command == "PRIVATE-TALK":
            messageaddress = self.socket_address

        modifiedMessage = self.build_message(username, message, command)
        clientSocket.sendto(modifiedMessage,(messageaddress, self.port))

    def build_message(self, username, message, command):
        user_message = "user:" + username + "\n"
        user_message += "command:" + command + "\n"
        user_message += "message:" + message + "\n"
        user_message += "channel:" + self.channel + "\n\n"
        return user_message
