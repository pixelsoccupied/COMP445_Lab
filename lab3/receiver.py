#!/usr/bin/python
import socket
import datetime
from threading import Thread

class Receiver(Thread):
    def __init__(self, address, broadcast, port):
        Thread.__init__(self)
        self.address = address
        self.broadcast = broadcast
        self.port = port
        self.thread_on = True
        self.users = []
        self.channel = "general"
        self.username = ""

    def run(self):
        receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        receiverSocket.bind((self.address, self.port))
        self.socket_address = socket.gethostbyname(socket.gethostname())

        while self.thread_on == True:
            message, clientAddress = receiverSocket.recvfrom(2048)
            message_content = self.split_message(message)
            modifiedMessage = self.parse_message(receiverSocket, message_content, clientAddress)

            if modifiedMessage is not None:
                print modifiedMessage
            elif message_content[1] == "QUIT":
                print "Bye now!"
                self.thread_on = False

    def split_message(self, message):
        message_split = message.split("\n")
        user_name = message_split[0].split(":")[1:]
        command = message_split[1].split(":")[1]
        message_content = message_split[2].split(":")[1]
        channel = message_split[3].split(":")[1]
        return (user_name, command, message_content, channel)

    def parse_message(self, receiverSocket, message_content, ip_address):
        now = datetime.datetime.now()
        command = message_content[1]
        if command == "JOIN":
            self.handle_join(ip_address[0], now, message_content[0][0], receiverSocket)
        elif command == "TALK":
            self.handle_talk(ip_address[0], now, message_content)
        elif command == "LEAVE"  and ip_address[0] != self.socket_address:
            self.remove_from_users(now, ip_address)
        elif command == "WHO":
            self.handle_who(now)
        elif command == "PING":
            self.add_user(ip_address[0],message_content[0][0])
        elif command == "PRIVATE-TALK":
            self.handle_private(ip_address[0], now, message_content, receiverSocket)
        else:
            return None

    def handle_join(self, ipaddress, now , username, receiverSocket):
        if ipaddress == self.socket_address:
            self.username = username
        if self.username:
            self.send_ping_as_broadcast(receiverSocket, self.username)
        print str(now) + " " +  username + " joined!"

    def handle_talk(self, ipaddress, now, message_content):
        if ipaddress == self.socket_address:
            self.channel = message_content[3]

        if self.channel == message_content[3]:
            print str(now) + " [" + message_content[0][0] + " #" + self.channel + "]: " + message_content[2]

    def remove_from_users(self, now, ip_address):
        for user in self.users:
            if user[0] == ip_address[0]:
                self.users.remove(user)
                print str(now) + " " + user[1] + " leaved!"
                break

    def handle_who(self, now):
        usersList = [i[1] for i in self.users]
        usersList.sort()
        print str(now) + " Connected users: " + str(usersList)

    def handle_private(self, ipaddress, now, message_content, receiverSocket):
        if ipaddress == self.socket_address:
            user = self.find_user_by_name(message_content[0][1])
            if user != None:
                self.send_to_private_user(now, receiverSocket, user[0], message_content)
            else:
                print "User could not be found."
        else:
            print str(now) + " [" + message_content[0][0] + "] (PRIVATE): " + message_content[2]

    def find_user_by_name(self, username):
        userfound = None
        for user in self.users:
            if user[1] == username:
                userfound = user
                break
        return userfound

    def send_ping_as_broadcast(self, receiverSocket, username):
        message = self.build_message(username, "", "PING")
        receiverSocket.sendto(message, (self.broadcast, self.port));

    def add_user(self, address, username):
        if self.find_user_by_name(username) == None:
            self.users.append((address, username))

    def send_to_private_user(self, now, receiverSocket, ipaddress, message_content):
        message = self.build_message(message_content[0][0], message_content[2], message_content[1])
        receiverSocket.sendto(message, (ipaddress, self.port));

    def build_message(self, username, message, command):
        user_message = "user:" + username + "\n"
        user_message += "command:" + command + "\n"
        user_message += "message:" + message + "\n"
        user_message += "channel:" + self.channel + "\n\n"
        return user_message
