import socket
import keyData
class status:
    status_0_EndCamera ='0'
    status_1_ActivateCamera = '1'
    status_2_BusWaiting = '2'
    status_reset = '-1'

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
    def Send_Recv(self):
        while True:
            data = self.conn.recv(1024).decode()
            print("data:" +data)
            replyData = []
            if data == status.status_1_ActivateCamera or data == status.status_0_EndCamera:
                replyData.append(status.status_1_ActivateCamera)
                # 카메라 시작
                replyData.append("번호판")
                reply1 = input("입력 :")
            elif data == status.status_2_BusWaiting:
                replyData.append(status.status_1_ActivateCamera)
                # 카운팅 시작
                replyData.append("0_1_2_-1")  # [2, (0_버스 발견못함 1_버스 발견됨 2_버스 정차함 -1_대기 시간초과(버싀나감)), 버스번호]
                replyData.append("번호판")
                reply1 = input("입력 :")
            elif data == status.status_reset:
                replyData.append(status.status_reset)

            reply = ''
            for r in replyData:
                reply = reply + r +"|"
            print(reply)
            self.conn.send(reply.encode())  # Sending reply

        self.clientsocket.close()           # Close connections


if __name__ == "__main__":
    server = ServerSocket('192.168.0.5',12345)
    server.Send_Recv()