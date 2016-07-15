import socket
import time


def Main():
    host = '127.0.0.1'
    port = 5555

    message = "<,R,G,B,>"
    mySocket = socket.socket()
    mySocket.connect((host, port))

    while message != 'q':
        message = input(" -> ")
        if message != 'q':
            mySocket.send(message.encode())

    mySocket.close()




if __name__ == '__main__':
    Main()