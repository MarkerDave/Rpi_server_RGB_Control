import serial
import socket
import queue
import sys
import threading

class serialConnect:
    comPort = 'COM5'
    baudrate = 115200
    myserial = serial.Serial(comPort, baudrate)

    def serial_run(self):
       # self.comPort = input('Comport: ')
        try:
            if not self.myserial.isOpen():
                self.myserial.open()
            else:
                print('Port is already open!' )
        except IOError as e:
            print('Error: ', e)

    def serial_read(self):
        data = self.myserial.read(16)
        data.decode('UTF-8')
        return data

    def serial_write(self, data):
        data += '\n'        #the arduino needs a \n after each command.
        databytes = data.encode('UTF-8')
        self.myserial.write(databytes)
        print('send data: ', databytes)


class socketServer:
    host = ''
    port = 5555
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setblocking(1)
    data_queue = queue.Queue(1)

    def __init__(self):
        try:
            self.soc.bind((self.host, self.port))
        except:
            print('Bind error: ', sys.exc_info())
        self.soc.listen(5)

    def socket_accept_thread(self):
        while True:
            try:
                print('Waiting for a new connection')
                conn, addr = self.soc.accept()
                client_thread = threading.Thread(target=self.threaded_client, args=(conn, self.data_queue))
                client_thread.daemon = True
                client_thread.start()
            except:
                print('Accept thread Error: ', sys.exc_info())

    def threaded_client(self, conn, data_queue):
        # conn.send(str.encode('welcome, type your info \n'))
        try:
            while True:
                data = conn.recv(2048)
                if not data:
                    break
                # reply = 'server output: ' + data.decode('UTF-8')
                data_queue.put(data.decode('UTF-8'))
                print("Items in queue: ", data_queue.qsize())    #items in queue should never be > 1!!
                # conn.sendall(str.encode(reply))
                print("Received data in threaded_client: ", data.decode('UTF-8'))
        except:
            print("Error: ", sys.exc_info())
        conn.close()

    def get_data(self):
        data = self.data_queue.get()
        return data


def Main():
    server = socketServer()
    arduino_conn = serialConnect()
    accept_thread = threading.Thread(target=server.socket_accept_thread)

    data_received = 'Nothing received'

    while True:
        if not accept_thread.is_alive():
            accept_thread.daemon = True
            accept_thread.start()

        arduino_conn.serial_run()
        data_received = server.get_data()
        arduino_conn.serial_write(data_received)
        print('-------------------------------- \n')


if __name__ == '__main__':
    Main()