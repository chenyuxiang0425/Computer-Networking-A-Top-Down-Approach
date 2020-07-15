# test: enter in the address field with
# http://localhost:8888/http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html

from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(10)

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    # 返回一个表示连接的新套接字和客户端地址
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print(message)
    # Extract the filename from the given message
    filename = message.split()[1].partition("//")[2].replace('/', '_')
    fileExist = "false"

    try:
        # Check whether the file exist in the cache
        f = open(filename, "r")
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        # send cache data
        header = 'HTTP/1.1 200 OK\nConnection:close\nContent-type:text/html\nContent-length:%d\n\n' % len(outputdata)
        tcpCliSock.send(header.encode())
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        f.close()
        tcpCliSock.close()
        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)# Fill in start. # Fill in end.
            try:
                # Connect to the socket to port 80
                # Fill in start.
                hostn = message.split()[1].partition("//")[2].partition("/")[0]
                askFile = '/'+message.split()[1].partition("//")[2].partition("/")[2]
                serverPort = 80
                # Fill in end.
                c.connect((hostn,serverPort))
                c.sendall("GET ".encode() + askFile.encode() + " HTTP/1.1\r\nHost: ".encode() + hostn.encode() + "\r\n\r\n".encode())
                # Read the response into buffer
                buff = c.recv(1024)
                c.close()
                # 向初始服务器发送
                tcpCliSock.sendall(buff)
                tcpCliSock.close()
                save_file = buff.split(b'\r\n\r\n')[1]  # 保存的文件不需要字节头
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"w")
                tmpFile.write(save_file.decode())
                tmpFile.close()
            except:
                print("Illegal request")

        else:
            # HTTP response message for file not found
            print("NET ERROR")
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()
