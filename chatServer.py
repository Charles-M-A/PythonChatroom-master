# Import the required python components
import csv
import socket, select, sys
from Lobby import Lobby
from PwdEncrypt import encrypt
from User import User
import os
from datetime import datetime

# Port number is a constant
PORT = 3000
# Initilize buffersize
bufferSize = 4096
# Max num of clients is a constant
MAXCLIENTS = 10000
# Store the host IP
hostIP = ''

if os.name == "posix":
    sock = sys.stdin
else:
    sock = socket.socket()

def conn():
    return connectionList

# Implement a socket
def implementSocket(address):
    # Create a new socket using TCP
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Pass in socket options
    newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Set to non-blocking
    newSocket.setblocking(0)
    # Bind socket to (hostIP, PORT)
    newSocket.bind(address)
    # Listen for connection made to socket, with max num of queued connections
    newSocket.listen(MAXCLIENTS)
    # Print that the server is hosting to indicate success
    print("Hosting at ", address)
    return newSocket

# Validate user's command to run the client host
if len(sys.argv) < 2 :
    # Print invalid commend and standard error
    print("Invalid command! Write into cmd: Python3 chatServer.py [hostIP address]", file = sys.stderr)
    # Exit system because of improper command
    sys.exit(1)
# Set hostIP based on the user's command
else:
    hostIP = sys.argv[1]
    

# Create a listening socket using the address and port
listeningSocket = implementSocket((hostIP,PORT))

# Initilize the lobby object
lobby = Lobby()

# Create a list of connections and add listeningSocket to the list
connectionList = []
connectionList.append(listeningSocket)
userList = []

# Run server processes
while True:
    
    #Waiting until ready for reading, writing, wait for an "exceptional condition", talking turns on communication
    userRead, userWrite, socketErr = select.select(connectionList, [], [])

    # Iterate through the available users that needs to be read
    for user in userRead:
        # Test for new user
        if user is listeningSocket:
            newSocket, add = user.accept()
            newUser = User(newSocket)
            userList.append(newUser)
            connectionList.append(newUser)

            # Welcomes new user
            lobby.welcomeNewUser(newUser)

        # Add a message
        else: 
            msg = user.socket.recv(bufferSize)
            if msg:
                if ((user.name == "admin") & (b"allUsers" in msg)):
                    for luser in userList:
                        name = "-> " + luser.name
                        lobby.getMsg(user,name)
                msg = msg.decode().lower()
                print(msg)
                with open("convo.csv", 'a', newline="\n") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter='|', quotechar='', quoting=csv.QUOTE_NONE,escapechar=" ")
                    filewriter.writerow([msg, datetime.now()])
                with open("enc_convo.csv", 'a', newline="\n") as csvfile:
                    filewriter = csv.writer(csvfile, delimiter='|', quotechar='', quoting=csv.QUOTE_NONE,escapechar=" ")
                    filewriter.writerow([encrypt(msg), datetime.now()])
                lobby.getMsg(user, msg)
            # Client terminates connection
            else:
                user.socket.close()
                connectionList.remove(user)

    #Handle sockets with errors
    for sock in socketErr:
        # Close the socket and remove it form the connectionList
        sock.close()
        connectionList.remove(sock)