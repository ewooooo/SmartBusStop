import socket
import time

class baseSocket:
    def __init__(self,HOST,PORT):
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
    

class mySocket(baseSocket):

    def Send_Recv(self,command):
        #[2, (0_버스 발견못함 1_버스 발견됨 2_버스 정차함 -1_대기 시간초과(버싀나감)), 버스번호]
        buffer = '_________'
        buffer = command + buffer
        mode = super().Send_Recv(buffer[0:10])
        mode = mode[0:9]
        mode = mode.replace('_','')
        SList = mode.split('|')
        print(SList)

        return SList







if __name__ == "__main__":
    print("start")

    st= mySocket("127.0.0.1",12345)
    while True:
        a = input("입력 : ")
        print(st.Send_Recv(a))


