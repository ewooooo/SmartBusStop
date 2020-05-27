import socket
import time
class mySocket:
    HOST = '192.168.0.15'
    PORT = 12345

    sendBuffer = []
    recvBuffer = []
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST,self.PORT))

    def RecvLoop(self):
        while True:

            # self.main.listTest.append("SocketCheck")
            # time.sleep(1)
            #print(self.sendBuffer)
            if self.sendBuffer:
                command = self.sendBuffer[0]
                self.s.send(command.encode())
                del self.sendBuffer[0]
                reply = self.s.recv(1024)
                reply= reply.decode()
                if reply == 'Terminating':
                    quit()
                print(reply)
            #time.sleep(0.0001)

            # command = input('Enter your command: ')
            # self.s.send(command.encode())
            
            

    def Send(self, data):
        self.sendBuffer.append(data)

    # def checkBuffer(self):
    #     value = self.buffer
    #     self.buffer.clear()
    #     return value

if __name__ == "__main__":
    print("start")

    st= mySocket()
    st.RecvLoop()

