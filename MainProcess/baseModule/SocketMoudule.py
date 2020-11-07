import socket
import time

class baseSocket:
    def __init__(self,HOST,PORT):
        print((HOST,PORT))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.s.connect((HOST,PORT))
                print("Connected")
                break
            except:
                print("re test socket")
                time.sleep(1)
                continue

    def Send_Recv(self,command):
        
        self.s.send(command.encode())
        mode = self.s.recv(10).decode("UTF-8")

        return mode
    
    def End_Socket(self):
        self.s.close()