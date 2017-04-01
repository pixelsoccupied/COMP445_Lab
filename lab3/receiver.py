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
        receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiverSocket.bind((self.address, self.port))
        self.socket_address = socket.gethostbyname(socket.gethostname())

        while self.thread_on == True:
            message, clientAddress = receiverSocket.recvfrom(2048)
            message_content = self.split_message(message)
            modifiedMessage = self.parse_message(receiverSocket, message_content, clientAddress)

            if modifiedMessage is not None:
                print modifiedMessage
            elif message_content[1] == "QUIT":
                self.thread_on = False

    def split_message(self, message):
        message_split = message.split("\n")
        user_name = message_split[0].split(":")[1:]
        command = message_split[1].split(":")[1]
        message_content = message_split[2].split(":")[1]
        return (user_name, command, message_content)

    def parse_message(self, receiverSocket, message_content, ip_address):
        now = datetime.datetime.now()
        command = message_content[1]
        if command == "JOIN":
            return str(now) + " " + message_content[0][0] + " joined!"
        elif command == "TALK":
            return str(now) + " [" + message_content[0][0] + "]: " + message_content[2]
        elif command == "LEAVE":
            self.remove_from_users(ip_address)
            return str(now) + " " + message_content[0][0] + " leaved!"
        elif command == "WHO":
            return str(now) + " Connected users: " + str([i[1] for i in self.users])
        elif command == "PING":
            self.users.append((ip_address, message_content[0][0]))
            return None
        elif command == "PRIVATE-TALK" and ip_address[0] == self.socket_address:
            user = self.find_user_by_name(message_content[0][1])
            self.send_to_private_user(now, receiverSocket, user[0], message_content)
            return None
        elif command == "PRIVATE-TALK" and ip_address[0] != self.socket_address:
            return str(now) + " [" + message_content[0][0] + "] (PRIVATE): " + message_content[2]
        else:
            return None

    def remove_from_users(self, ip_address):
        for user in self.users:
            if user[0] == ip_address:
                self.users.remove(user)
                break

    def find_user_by_name(self, username):
        userfound = None
        for user in self.users:
            if user[1] == username:
                userfound = user
                break
        return userfound

    def send_to_private_user(self, now, receiverSocket, ipaddress, message_content):
        message = self.build_message(message_content[0][0], message_content[2], message_content[1])
        receiverSocket.sendto(message, (ipaddress[0], self.port));

    def build_message(self, username, message, command):
        user_message = "user:" + username + "\n"
        user_message += "command:" + command + "\n"
        user_message += "message:" + message + "\n\n"
        return user_message
