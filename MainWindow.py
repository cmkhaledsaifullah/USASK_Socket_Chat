#Author: C M Khaled Saifullah
#SR Lab, Department of Computer Science
#University of Saskatchewan
#Fall 2017
#Date: 22/11/2017


import socket
from Room import Room
from User import User


class MainWindow:

    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.roomUserMap = {} # {userName : roomName}
        self.QUIT_STRING = '$quit$'
        self.commands = b'Commands:\n'\
            + b'[list] to see the list of all rooms\n'\
            + b'[join room_name] to join an existing room\n' \
            + b'[create room_name] to create a new room\n' \
            + b'[switch room_name] to switch to another room\n' \
            + b'[leave] to leave the existing room\n' \
            + b'[commands] to see the available COmmands\n' \
            + b'[quit] to quit from the system\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'

    def welcome_new(self, new_user):
        new_user.socket.sendall(b'Welcome to USASK ChatRoom.\nEnter the name you want to display: \n')

    def handle_msg(self, user, msg):

        print(user.name + " says: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            user.name = name
            print("New connection from:", user.name)
            user.socket.sendall(self.commands)

        elif "join" in msg:
            self.joinRoom(user,msg)

        elif "create" in msg:
            self.createRoom(user,msg)

        elif "switch" in msg:
            self.switchRoom(user,msg)

        elif "leave" in msg:
            self.leaveRoom(user)

        elif "list" in msg:
            self.list_rooms(user)

        elif "commands" in msg:
            user.socket.sendall(self.commands)

        elif "quit" in msg:
            user.socket.sendall(self.QUIT_STRING.encode())
            self.remove_user(user)

        else:
            # check if in a room or not first
            if user.name in self.roomUserMap:
                self.rooms[self.roomUserMap[user.name]].broadcast(user, msg)
            else:
                msg = self.noRoomMessage()
                user.socket.sendall(msg.encode())

    def remove_user(self, user):
        if user.name in self.roomUserMap:
            self.rooms[self.roomUserMap[user.name]].remove_user(user)
            del self.roomUserMap[user.name]
        print("user: " + user.name + " has left\n")

    def createRoom(self,user,msg):
        if len(msg.split()) >= 2:
                roomName = msg.split()[1]
                if not roomName in self.rooms:
                    if user.name in self.roomUserMap:
                        old_room = self.roomUserMap[user.name]
                        self.rooms[old_room].remove_user(user)
                    newRoom = Room(roomName)
                    self.rooms[roomName] = newRoom
                    self.addToRoom(user,roomName)
                else:
                    user.socket.sendall(roomName.encode() + b" is already exist \n");
                    self.list_rooms(user)
        else:
            user.socket.sendall(self.commands)


    def switchRoom(self,user,msg):
        sameRoom = False
        if len(msg.split()) >= 2:
            roomName = msg.split()[1]
            if roomName in self.rooms:
                if user.name in self.roomUserMap:
                    if self.roomUserMap[user.name] == roomName:
                        user.socket.sendall(b'You are already in room: ' + roomName.encode() +b'\n')
                        sameRoom = True
                    # Switch the user to the new Room
                    else:
                        old_room = self.roomUserMap[user.name]
                        self.rooms[old_room].remove_user(user)
                else:
                    msg = self.noRoomMessage()
                    user.socket.sendall(msg.encode())
                    sameRoom = True

                if sameRoom == False:
                    self.addToRoom(user,roomName)
            else:
                msg = self.roomUnavailableMessage(roomName)
                user.socket.sendall(msg.encode())
        else:
            user.socket.sendall(self.commands)

    def joinRoom(self,user,msg):
        sameRoom = False
        if len(msg.split()) >= 2: # error check
            roomName = msg.split()[1]
            if user.name in self.roomUserMap: # user is in a room
                msg = self.switchMessage(roomName)
                user.socket.sendall(msg.encode())
            else:
                if roomName in self.rooms:
                    self.addToRoom(user,roomName)
                else:
                    msg = self.roomUnavailableMessage(roomName)
                    user.socket.sendall(msg.encode())
        else:
            user.socket.sendall(self.commands)

    def leaveRoom(self,user):
        if user.name in self.roomUserMap: # user is in a room
            old_room = self.roomUserMap[user.name]
            self.rooms[old_room].remove_user(user)
            self.roomUserMap.pop(user.name, None)
            user.socket.sendall(" ".encode())
        else:
            msg = self.noRoomMessage()
            user.socket.sendall(msg.encode())

    def addToRoom(self,user,roomName):
        if roomName == "":
            msg = self.commandMessage()
            user.socket.sendall(msg.encode())
        else:
            self.rooms[roomName].users.append(user)
            self.rooms[roomName].welcome_new(user)
            self.roomUserMap[user.name] = roomName

    def list_rooms(self, user):
        if len(self.rooms) == 0:
            msg = 'There is no active room now. Please create your own to Continue!\n' \
                + 'Use [create room_name] to create a room.\n'
            user.socket.sendall(msg.encode())
        else:
            msg = 'List of current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].users)) + " user(s)\n"
            user.socket.sendall(msg.encode())

    def noRoomMessage(self):
        msg = 'You are currently not in any room! \n' \
            + 'Use [list] to see available rooms! \n' \
            + 'Use [join room_name] to join a room! \n'\
            + 'Use [create room_name] to create a room! \n'
        return msg

    def roomUnavailableMessage(self,roomName):
        msg = roomName+' is not available now. \n' \
                + 'Use [list] to see available rooms! \n' \
                + 'Use [join room_name] to join a room! \n'\
                + 'Use [create room_name] to create a room! \n'
        return msg

    def switchMessage(self,roomName):
        msg = 'Currently you are at  '+roomName+ ' Room \n' \
                + 'Use [list] to see available rooms! \n' \
                + 'Use [switch room_name] to go to another room! \n'\
                + 'Use [create room_name] to create a room! \n'
        return msg

    def commandMessage(self):
        msg = 'Wrong Command Syntex. Please use following suntex\n' \
                + 'Use [join room_name] to join a room! \n' \
                + 'Use [switch room_name] to go to another room! \n'\
                + 'Use [create room_name] to create a room! \n'
        return msg



