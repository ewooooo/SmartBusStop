import socket

class status:
    status_1_ActivateCamera = '1'
    status_0_EndCamera = '0'
    status_2_BusWaiting = '2'
    status_3_BusStop = '3'
    status_5_checkState = '5'

import time

HOST = '192.168.0.21'
# Server IP or Hostname
PORT = 12345
# Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')


#managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed ')

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')

# awaiting for message
while True:
    data = conn.recv(1024).decode()
    if data == status.status_1_ActivateCamera:
        replyData = [status.status_1_ActivateCamera]
        # 카메라 시작
    elif data == status.status_0_EndCamera:
        replyData = [status.status_0_EndCamera]
        # 모든 프로세스 종료
    elif data == status.status_2_BusWaiting:
        replyData = [status.status_2_BusWaiting]
        # 카운팅 시작
    elif data == status.status_3_BusStop:
        replyData = [status.status_3_BusStop]
        # 카운팅만 종료 카메라 유지
    elif data == status.status_5_checkState:
        replyData = [status.status_5_checkState]
        # 상태 체크



    print('I sent a message back in response to: ' + data2)
    #process your message
    reply = data

    # Sending reply
    conn.send('2'.encode())
    print("send")
conn.close()
# Close connections
