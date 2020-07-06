from socket import *
import time

service_name = 'localhost'
service_port = 12000

# SOCK_DGRAM is used for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
address = (service_name, service_port)

for i in range(10):
    send_time = time.time()
    message = ('Ping %d %s' % (i+1, send_time)).encode()
    clientSocket.sendto(message, address)
    # Receive the client packet along with the address it is coming from
    try:
        receive_message, receive_address = clientSocket.recvfrom(1024)
        receive_message = receive_message.upper()
        receive_time = time.time()
        rtt = receive_time - send_time
        print('Sequence %d: Reply from %s, address = %s, RTT = %.5FS' % (i+1, receive_message.decode(), receive_address, rtt))
    except Exception as socket_timeout:
        print('Sequence %d: Reply time out' % (i+1))

clientSocket.close()