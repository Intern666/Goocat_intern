from socket import socket,AF_INET,SOCK_STREAM

HOST = '211.82.83.135' # or 'localhost'
PORT = 50008
BUFSIZ =1024
ADDR = (HOST,PORT)


while True:
    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    data1 = input('>')
    #data = str(data)
    if not data1:
        break
    tcpCliSock.send(data1.encode())
    data1 = tcpCliSock.recv(BUFSIZ)
    if not data1:
        break
    print(data1.decode('utf-8'))
    tcpCliSock.close()

