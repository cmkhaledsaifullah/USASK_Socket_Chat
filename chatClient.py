#Author: C M Khaled Saifullah
#SR Lab, Department of Computer Science
#University of Saskatchewan
#Fall 2017
#Date: 22/11/2017


import select, socket, sys

#Port number used for COmmunication
PORT = 1131
# Buffer Size is defined here
Buffer_Size = 4096
#Command for disconnecting
QUIT_STRING = '$quit$'

#Checking wheter user write correct command
if len(sys.argv) < 2:
    print("Wrong command, please write command as Python3 chatClient.py [host address]", file = sys.stderr)
    sys.exit(1)
else:
    #Connecting with the server using same port number
    server_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_con.connect((sys.argv[1], PORT))

def prompt():
    print('>', end=' ', flush = True)

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, server_con]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for aSocket in read_sockets:
        if aSocket is server_con: # Response from the server
            msg = aSocket.recv(Buffer_Size)
            if not msg:           # Server is not responding for some error
                print("Server is down! Sorry for your inconvinience!!!")
                sys.exit(2)
            else:
                # User wants to disconnect form the server
                if msg == QUIT_STRING.encode():
                    sys.stdout.write('Bye. Thanks for Using USASK Chat\n')
                    sys.exit(2)
                # New User
                else:
                    sys.stdout.write(msg.decode())
                    if 'Enter the name you want to display:' in msg.decode():
                        msg_prefix = 'name: ' # user name
                    else:
                        msg_prefix = ''
                    prompt()

        else:
            #User send some command or message
            msg = msg_prefix + sys.stdin.readline()
            server_con.sendall(msg.encode())
