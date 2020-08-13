# Import the required python components
import csv
import time

import PwdDecrypt
import PwdEncrypt
import socket
# Import required objects
from Room import Room
from User import User


# Create the Lobby class that holds all the chat rooms


class Lobby:

    # Create constructor
    def __init__(self):
        # Holds the rooms 
        self.rooms = {}
        # Define quit command
        self.QUITCOMMAND = '#quit'
        # Maps the users to the roomName
        self.roomUserMap = {}
        self.userCount = 0
        self.useerList = []
        # Lists all the commands to enforces bit literals 
        self.commands = b'Commands:\n' \
                        + b'[allUsers] used to display all users (usage restricted to admin\n)' \
                        + b'[commands] used to display all the possible commands\n' \
                        + b'[create RoomName] used to create a room\n' \
                        + b'[kick username] to kick a particular user belonging to any room (usage restricted to admin)\n' \
                        + b'[list] used to lists all available rooms\n' \
                        + b'[join RoomName] used for joining and switching rooms\n' \
                        + b'[leave] used to leave a room but stay in the lobby\n' \
                        + b'[private username] to send private messages\n' \
                        + b'[#quit] used to terminate the session (leave the lobby)\n' \
                        + b'\n'

    # Welcomes a new user
    def welcomeNewUser(self, newUser):
        newUser.socket.sendall(b'Welcome to the Lobby.\nEnter your screen name: \n')

    # Generates message for the server and execute commands based on the msg received
    def getMsg(self, user, msg):
        # Prints what the user types in their input
        # print(user.name + ": " + msg)
        flag = 0

        if "> name:" in msg:
            print(user.name + " tried to rename itself")
            user.socket.sendall(b"You cannot rename yourself.\nUse the following " + self.commands)
        # If "name:" is apart of the user's message (indicating a new user), add user
        elif "name:" in msg:
            self.useerList.append(user)
            self.userCount = self.userCount + 1
            # If the user does not enter a name, a username will be generated for them
            if len(msg.split()) <= 1:
                name = "Guest " + str(self.userCount)
            # Else, get user input
            else:
                name = msg.split(" ")[1]
                var1 = msg.split(" ")[2]
                var0 = PwdEncrypt.encrypt(var1)
            flag = 1
            with open("users.csv", 'r', newline='') as csvfile:
                read = csv.reader(csvfile)
                count = 0
                for row in read:
                    count = count + 1
                    text = row[0]
                    print(text)
                    if (name == text):
                        flag = 1
                        print(PwdDecrypt.decrypt(var0))
                        print(PwdDecrypt.decrypt(row[1].encode()))
                        if PwdDecrypt.decrypt(var0) == PwdDecrypt.decrypt(row[1].encode()):
                            user.name = name
                            print("New connection from:", user.name)
                            # print("Password: ",var0)
                            user.socket.sendall(self.commands)
                            break
                        else:
                            user.socket.sendall(b"Wrong password!!! Try again.")
                    else:
                        flag = 0;
                if flag == 0:
                    csvfile.close()
                    with open("users.csv", 'a', newline="\n") as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
                        print(var0.decode())
                        filewriter.writerow([name, var0.decode().rstrip()])
                        user.name = name
                        print("New connection from:", user.name)
                        # print("Password: ",var0)
                        user.socket.sendall(self.commands)
        # gAAAAABeWi3i5GJhXqyCO7hv9YEMuMMRGHhHZ2Re5k4gqLxc_XAIytQ9MnjBn5bSa4ZBaqERuQjM-yFAD5As_3YzCGwD-YMbIA==

        elif "->" in msg:
            user.socket.sendall(msg.encode())

        # Displays all the possible commands
        elif "commands" in msg:
            user.socket.sendall(self.commands)

        # Create a room
        elif "create" in msg:
            self.createRoom(user, msg)

        # List all the rooms
        elif "list" in msg:
            self.listRooms(user)

        # Join a room
        elif "join" in msg:
            self.joinRoom(user, msg)

        # Leave room
        elif "leave" in msg:
            self.leaveRoom(user)

        elif "kick" in msg:
            self.kick(user, msg)

        # Leave lobby
        elif "quit" in msg:
            user.socket.sendall(self.QUITCOMMAND.encode())
            self.removeUser(user)

        elif "private" in msg:
            self.privateMsg(user, msg)
            self.getMsg(user, "-->> ")

        elif "-->>" in msg:
            user.socket.sendall(b"PM sent.")

        else:
            # Check if user is in room
            if user.name in self.roomUserMap:
                self.rooms[self.roomUserMap[user.name]].broadcast(user, msg)
            else:
                msg = self.noRoomMessage()
                user.socket.sendall(msg)

    # Remove a user
    def removeUser(self, user):
        if user.name in self.roomUserMap:
            self.rooms[self.roomUserMap[user.name]].removeUser(user)
            del self.roomUserMap[user.name]
        print(user.name + " has left\n")

    # Parse room name
    def parseRoomName(self, msg):
        roomNameString = msg.split()
        # Delete the carret and the command
        del roomNameString[1]
        del roomNameString[0]
        roomNameString = " ".join(roomNameString)
        return roomNameString

    # Create a room
    def createRoom(self, user, msg):
        # Test if the input is long enough
        if len(msg.split()) >= 2:
            # Parse the room name
            roomName = self.parseRoomName(msg)

            # Checks if the room is already in the existing rooms
            if not roomName in self.rooms:
                # If the user is already in a room
                if user.name in self.roomUserMap:
                    # Get old room and remove user from old room
                    oldRoom = self.roomUserMap[user.name]
                    self.rooms[oldRoom].removeUser(user)
                # Create a new room and assign the user to the room
                newRoom = Room(roomName)
                self.rooms[roomName] = newRoom
                self.addToRoom(user, roomName)
            # If user tries to create a room that already exists
            else:
                # Send error message to client and print all the rooms
                user.socket.sendall(
                    b"The " + roomName.encode() + b" already exists. Join the following rooms or create a new room.\n")
                self.listRooms(user)
        else:
            user.socket.sendall(self.commands)

    # List the rooms
    def listRooms(self, user):
        # If there are no rooms in the rooms list
        if len(self.rooms) == 0:
            msg = 'There are no rooms.\n' \
                  + 'Create your own room with the [create RoomName] command.\n'
            user.socket.sendall(msg.encode())
        # List all the possible room
        else:
            # List all the rooms
            msg = 'The available roomes are... \n'
            for room in self.rooms:
                msg += room + " has " + str(len(self.rooms[room].users)) + " user(s)\n"
            user.socket.sendall(msg.encode())

    # Switches the user's room if they are already in a room
    def switchRoom(self, user, msg):
        # Checks if the user's input is correct
        if len(msg.split()) >= 2:
            # Parse room name
            roomName = self.parseRoomName(msg)

            # If the roomName exists in the rooms list
            if roomName in self.rooms:
                # If the user is in the roomUserMap
                if user.name in self.roomUserMap:
                    # If the user is switching to the current room, send no chang emessage
                    if self.roomUserMap[user.name] == roomName:
                        user.socket.sendall(
                            b'You were not moved since you request the same room:\nYou are currently in: '
                            + roomName.encode() + b'\n')
                    # Switch the user to a new room if current user is not assigned to room in roomUserMap
                    else:
                        # Get the old room of the user and remove the user from the room
                        oldRoom = self.roomUserMap[user.name]
                        self.rooms[oldRoom].removeUser(user)
                        self.addToRoom(user, roomName)
                # Handle the exception that the user is not in the roomUserMap
                else:
                    msg = self.noRoomMessage()
                    user.socket.sendall(msg)
            # The room does not exist in the room list
            else:
                msg = self.roomUnavailableMessage(roomName)
                user.socket.sendall(msg)
        # Send the user the list of available commands if input is incorrect
        else:
            user.socket.sendall(self.commands)

    # Allows the user to join a room
    def joinRoom(self, user, msg):
        # If the user enters a valid room
        if len(msg.split()) >= 2:
            # Parse the room name
            roomName = self.parseRoomName(msg)
            # If the user is already in a room, switch rooms
            if user.name in self.roomUserMap:
                print(msg)
                self.switchRoom(user, msg)
            # If the user is not in a room
            else:
                # If the roomName exists, add the user to the room
                if roomName in self.rooms:
                    self.addToRoom(user, roomName)
                # The room the user entered does not exist
                else:
                    msg = self.roomUnavailableMessage(roomName)
                    user.socket.sendall(msg)
        # Send all commands
        else:
            user.socket.sendall(self.commands)

    # Removes a user from a room
    def leaveRoom(self, user):
        # Checks if the user is in
        if user.name in self.roomUserMap:
            # Gets the old room that the user is in
            oldRoom = self.roomUserMap[user.name]
            # Remove the user from th room
            self.rooms[oldRoom].removeUser(user)
            # Update that the user is not in a room
            self.roomUserMap.pop(user.name, None)
            # Display message to user
            user.socket.sendall(b"You left room " + oldRoom.encode() + b"\n")

        # The user is not in any rooms and tries to leave
        else:
            # Send message to user that they cannot leave if not in room
            msg = self.noRoomMessage()
            user.socket.sendall(msg)

    def privateMsg(self, user, msg):
        if len(msg.split()) >= 2:
            name = msg.split()[2]
            for luser in self.useerList:
                if luser.name == name:
                    prefix = user.name + "> "
                    pmsg = prefix + msg
                    luser.socket.sendall(pmsg.encode())
        else:
            msg = b"Wrong command format!!!\n" + self.commands
            user.socket.sendall(msg)

    def kick(self, user, msg):
        print("k1")
        if len(msg.split()) >= 2:
            if (user.name == "admin"):
                print("k2")
                name = msg.split()[2]
                print(name)
                # Checks if the user is in
                for luser in self.useerList:
                    if luser.name == name:
                        # Gets the old room that the user is in
                        oldRoom = self.roomUserMap[name]
                        print(self.rooms[oldRoom].name)
                        # Remove the user from th room
                        self.rooms[oldRoom].removeUser(luser)
                        # Update that the user is not in a room
                        self.roomUserMap.pop(name, None)
                        # Display message to user
                        user.socket.sendall(b'Kicked ' + name.encode() + b' \n')
                        luser.socket.sendall(b"User: " + name.encode() + b" has been kicked.\n")

                # The user is not in any rooms and tries to leave
            else:
                # Send message to user that they cannot leave if not in room
                msg = b"user not found!!\n" + self.commands
                user.socket.sendall(msg)
        else:
            msg = b"Wrong command format!!!\n" + self.commands
            user.socket.sendall(msg)

    # Add a user to a room
    def addToRoom(self, user, roomName):
        # Verify there is a room name
        if roomName == "":
            # Resend possible commands
            msg = self.commandMessage()
            user.socket.sendall(msg)
        # Add the user to the room
        else:
            self.rooms[roomName].users.append(user)
            self.rooms[roomName].welcomeNewUser(user)
            self.roomUserMap[user.name] = roomName

    # Displays messages
    def noRoomMessage(self):
        msg = b"You are currently not in any room!\n"
        msg = msg + self.commands
        return msg

    def roomUnavailableMessage(self, roomName):
        msg = roomName.encode() + b" is not available now. \n"
        msg = msg + self.commands
        return msg

    def commandMessage(self):
        msg = b"In valid command, use the following commands only\n"
        msg = msg + self.commands
        return msg
