import socket
from busCarNumberDetect import *

class ServerSocket:
    def __init__(self,HOST,PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((HOST, PORT))
            print("bind ok")
        except socket.error:
            print('Bind failed ')
        s.listen(5)
        print('Socket awaiting messages')
        (self.conn, self.addr) = s.accept()
        print('Connected')
        self.__busSystem = busCarNumberDetect(0)

    def Send_Recv(self):
        while True:
            data = self.conn.recv(1024).decode()
            data = data.replace('_','')
            print(data)
            replyData = []
            if data == '0':
                replyData.append('1')

                #imageRetrunData = input("입력1 :") # 카메라 정보에서 리턴
                imageReturnData = (self.__busSystem.detect())
                for data in imageReturnData:
                    replyData.append(data)

            reply = ''
            for r in replyData:
                reply = reply + r +"|"
            self.conn.send(reply.encode())  # Sending reply

        self.clientsocket.close()           # Close connections


if __name__ == "__main__":
    server = ServerSocket('192.168.86.128',12345)
    server.Send_Recv()
