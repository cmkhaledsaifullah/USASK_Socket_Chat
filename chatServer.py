#Author: C M Khaled Saifullah
#SR Lab, Department of Computer Science
#University of Saskatchewan
#Fall 2017
#Date: 22/11/2017

import select, socket, sys, pdb
from MainWindow import MainWindow
from Room import Room
from User import User

#Port number used for COmmunication
PORT = 1131
# Buffer Size is defined here
Buffer_Size = 4096
#Highest number of CLient for our chat system
Max_Clients = 20
host = ''
if len(sys.argv) >= 2 :
    host = sys.argv[1]

def create_socket(address):
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    newSocket.setblocking(0)
    newSocket.bind(address)
    newSocket.listen(Max_Clients)
    print("The server is Runner at  ", address)
    return newSocket


listen_sock = create_socket((host,PORT))

main_window = MainWindow()
connection_list = []
connection_list.append(listen_sock)

while True:
    # User.fileno()
    read_users, write_users, error_sockets = select.select(connection_list, [], [])
    for user in read_users:
        if user is listen_sock: # new connection, user is a socket
            new_socket, add = user.accept()
            new_user = User(new_socket)
            connection_list.append(new_user)
            main_window.welcome_new(new_user)

        else: # new message
            msg = user.socket.recv(Buffer_Size)
            if msg:
                msg = msg.decode().lower()
                main_window.handle_msg(user, msg)
            else:
                user.socket.close()
                connection_list.remove(user)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)



