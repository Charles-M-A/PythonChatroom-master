from chatServer import conn


def getList():
    return conn()

def getSocket(msg):
    connList = conn()
    for user in connList:
        if user.name == msg.split()[1]:
            return user.socket
