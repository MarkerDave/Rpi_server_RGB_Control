import serial
import socket
import queue
import sys
import threading


class serialConnect:
    comPort = 'COM8'
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

    def serial_stop(self):
        self.myserial.close()

    def serial_read(self):
        data = self.myserial.read(16)
        data.decode('UTF-8')
        return data

    def serial_write(self, data):
        data += '\n'        #the arduino needs a \n after each command.
        data_bytes = data.encode('UTF-8')
        self.myserial.write(data_bytes)
        print('send data: ', data_bytes)

    def data_check(self,data):
        # check if the data has been received correctly.
        #startbyte < and end byte >
        for i in data:
            if i == '<':


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
                    print('A connection closed.')
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

    #data checking fuction
    def data_check(self, input_data):
        #data must be in this form <,1,2,3,4,> anything else is wrong.
        #if correct data has been found, it wil be returned as a string, else it returns False
        state = 0
        buffer = ''
        count = 0
        input_data = input_data.split(',')
        return_data = False

        for i in input_data:
            if state == 0 and i == '<':
                print('state 0')
                buffer += ('<')
                state += 1
            elif state == 1 and i != '<':
                print('state 1')
                buffer += (',' + i)
                if i == '>':
                    print('Data received correctly')
                    return_data = buffer
                    state += 1
                elif count >= (len(input_data) - 1) and i != '>':
                    print('No end byte found')
                    return_data = False
            elif state == 1 and i == '<':
                return_data = False
                break
            elif count >= (len(input_data) - 1) and i != '>' and state == 0:
                print('No end byte found')
                return_data = False
            elif state == 2:
                break
        return return_data

def Main():
    server = socketServer()
    arduino_conn = serialConnect()
    accept_thread = threading.Thread(target=server.socket_accept_thread)

    while True:
        if not accept_thread.is_alive():
            accept_thread.daemon = True
            accept_thread.start()

        arduino_conn.serial_run()
        data_received = server.get_data()
        arduino_conn.serial_write(data_received)
        arduino_conn.serial_stop()
        print('-------------------------------- \n')
        #Features needed to be added
        #begin and end of message byte.
        #Dilluting blue color between set times.



if __name__ == '__main__':
    Main()
