#Author: C M Khaled Saifullah
#SR Lab, Department of Computer Science
#University of Saskatchewan
#Fall 2017
#Date: 22/11/2017

import socket,User


class Room:
    def __init__(self, name):
        self.users = [] # a list of sockets
        self.name = name
        self.previousMsg = ''

    def welcome_new(self, from_user):
        msg = self.name + " welcomes: " + from_user.name + '\n'
        self.previousMsg = self.previousMsg + msg
        from_user.socket.sendall(self.previousMsg.encode())
        for user in self.users:
            if user.name != from_user.name:
                user.socket.sendall(msg.encode())

    def broadcast(self, from_user, msg):
        msg = from_user.name + ": " + msg
        self.previousMsg = self.previousMsg + str(msg)
        for user in self.users:
            user.socket.sendall(msg.encode())

    def remove_user(self, user):
        self.users.remove(user)
        leave_msg = user.name + " has left the room \n"
        self.broadcast(user, leave_msg)
