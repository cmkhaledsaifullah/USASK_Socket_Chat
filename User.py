#Author: C M Khaled Saifullah
#SR Lab, Department of Computer Science
#University of Saskatchewan
#Fall 2017
#Date: 22/11/2017

import socket,pdb

class User:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()
