import socket
import time

class mySocket:
    def __init__(self,HOST,PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.s.connect((HOST,PORT))
                print("Connected")
                break
            except:
                print("re test socket")
                continue

    def Send_Recv(self,command):

        self.s.send(command.encode())
        mode = self.s.recv(1024).decode()
        SList = mode.split('|')

        return SList

# if __name__ == "__main__":
#     print("start")
#
#     st= mySocket()
#     st.RecvLoop()

