import socket

HOST = '192.168.0.15'
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
    data1 = conn.recv(1024)
    data2 = data1.decode()

    print('I sent a message back in response to: ' + data2)
    reply = ''

    # process your message
    if data2 == 'Hello':
        reply = 'Hi, back!'
    elif data2 == 'This is important':
        reply = 'OK, I have done the important thing you have asked me!'
    #and so on and on until...
    elif data2 == 'quit':
        conn.send('Terminating'.encode())
        break
    else:
        reply = 'Unknown command'

    # Sending reply
    conn.send(reply.encode())
conn.close()
# Close connections
