import socket

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
            data = data.replace('_','')
            print(data)
            replyData = []
            if data == status.status_1_ActivateCamera or data == status.status_0_EndCamera:
                replyData.append(status.status_1_ActivateCamera)

                imageRetrunData = input("입력1 :") # 카메라 정보에서 리턴
                replyData.append(imageRetrunData)

            elif data == status.status_2_BusWaiting:
                replyData.append(status.status_2_BusWaiting)
                # 카운팅 시작
                imageRetrunData = str(input("입력2 :")) # 버스 번호 발견 94551 발견못한 9455 버스 정

                # [2, (0_버스 발견못함 1_버스 발견됨 2_버스 정차함 -1_대기 시간초과(버싀나감)), 버스번호]

                if len(imageRetrunData) == 4:
                    replyData.append('1')
                    replyData.append(imageRetrunData)
                elif len(imageRetrunData) == 5:
                    if imageRetrunData[0] == '-':
                        replyData.append('-1')
                        replyData.append(imageRetrunData[1:5])
                    elif imageRetrunData[4] == '1':
                        replyData.append('2')
                        replyData.append(imageRetrunData[0:4])
                    else:
                        replyData.append('0')
                elif imageRetrunData == '0':
                    replyData.append('0')
                else:
                    replyData.append('-')

            elif data == status.status_reset:
                replyData.append(status.status_reset)

            elif int(data) > 3:
                replyData.append(status.status_reset)

            reply = ''
            for r in replyData:
                reply = reply + r +"|"
            self.conn.send(reply.encode())  # Sending reply

        self.clientsocket.close()           # Close connections


if __name__ == "__main__":
    server = ServerSocket('127.0.0.1',12345)
    server.Send_Recv()