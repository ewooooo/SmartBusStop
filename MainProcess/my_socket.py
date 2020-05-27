# import socket
import time
class mySocket:
    # HOST = '192.168.35.163'  # Server IP or Hostname
    # PORT = 12345  # Pick an open Port (1000+ recommended), must match the client sport

    # buffer = []
    def __init__(self,obj):
        self.SocketState = 0;

        print("makeSocket")
        self.main = obj
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     print('Socket created')

    #     # managing error exception
    #     try:
    #         s.bind((self.HOST, self.PORT))
    #     except socket.error:
    #         print('Bind failed ')
    #     s.listen(5)
    #     print('Socket awaiting messages')
    #     (self.clientsocket, self.address) = s.accept()
    #     print('Connected')

    def RecvLoop(self):
        while True:
            self.main.listTest.append("SocketCheck")
            time.sleep(1)

            #print("socket")
        #     data = self.clientsocket.recv(1024)
        #     print('I sent a message back in response to: ' + data)
        #     reply = ''
        #     # process your message
        #     if data == 'Hello':
        #         reply = 'Hi, back!'
        #     elif data == 'This is important':
        #         reply = 'OK, I have done the important thing you have asked me!'
        #     # and so on and on until...
        #     elif data == 'quit':
        #         self.clientsocket.send('Terminating')
        #         break
        #     else:
        #         reply = 'Unknown command'
        #     self.clientsocket.send(reply)   # Sending reply
        # self.clientsocket.close()           # Close connections

    # def Send(self):
    #     next()
    # def checkBuffer(self):
    #     value = self.buffer
    #     self.buffer.clear()
    #     return value