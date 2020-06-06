#import socket
#import time

class status:
    status_1_ActivateCamera = '1'
    status_2_BusWaiting = '2'

class ServerSocket:
    def __init__(self):
        pass
    def Send_Recv(self,data):

        # data = conn.recv(1024).decode()
        replyData = []
        if data == status.status_1_ActivateCamera:
            replyData.append(status.status_1_ActivateCamera)
            # 카메라 시작
            replyData.append("번호판")
        elif data == status.status_2_BusWaiting:
            replyData.append(status.status_1_ActivateCamera)
            # 카운팅 시작
            replyData.append("0_1_2_-1")  # [2, (0_버스 발견못함 1_버스 발견됨 2_버스 정차함 -1_대기 시간초과(버싀나감)), 버스번호]
            replyData.append("번호판")
        return replyData




# HOST = '192.168.0.21'
# # Server IP or Hostname
# PORT = 12345
# # Pick an open Port (1000+ recommended), must match the client sport
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('Socket created')
#
#
# #managing error exception
# try:
#     s.bind((HOST, PORT))
# except socket.error:
#     print('Bind failed ')
#
# s.listen(5)
# print('Socket awaiting messages')
# (conn, addr) = s.accept()
# print('Connected')
#
# awaiting for message
#
#
#
#
#     print('I sent a message back in response to: ' + data2)
#     #process your message
#     reply = data
#
#     # Sending reply
#     conn.send('2'.encode())
#     print("send")
# conn.close()
# Close connections
