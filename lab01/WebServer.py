# encode(): str -> bytes
# decode(): bytes -> str

# import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
# 将套接字绑定到本地地址，地址是一个元组
# 对于IP套接字，地址是一对(主机、端口)
# 主机必须引用本地主机
serverSocket.bind(("localhost", 6789))
# 使服务器能够接受连接
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    # 返回一个表示连接的新套接字和客户端地址
    connectionSocket, addr = serverSocket.accept()
    try:
        # 从套接字接收最多缓冲大小的字节,返回的是 bytes 类型
        message = connectionSocket.recv(1024)
        # 分割 bytes,到各个 list,其中 index = 1 是请求文件地址
        filename = message.split()[1]
        # filename[1:] 去除了斜杠： b'/HelloWorld.html' -> b'HelloWorld.html'
        f = open(filename[1:])
        outputdata = f.read()
        # Send one HTTP header line into socket
        # 注意： 最后一定要两个\n
        #       Connection 一定要设置为 close
        header = 'HTTP/1.1 200 OK\nConnection:close\nContent-type:text/html\nContent-length:%d\n\n' % len(outputdata)
        # 向套接字发送一个数据字符串
        connectionSocket.send(header.encode())
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        f.close()
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        header = 'HTTP/1.1 404 Not Found'
        # encode(): str -> bytes
        connectionSocket.send(header.encode())
        # Close client socket
        # 不能使用 serverSocket.close() 因为会直接关闭 socket
        connectionSocket.close()

serverSocket.close()
