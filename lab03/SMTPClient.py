from socket import *
import my_account

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.qq.com"
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
def do_with_email(operation, response_status):
    clientSocket.sendall(operation.encode())
    recv2 = clientSocket.recv(1024).decode()
    print(recv2)
    if recv2[:3] != str(response_status):
        print(str(response_status) + ' reply not received from server.')

if __name__ == '__main__':
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver,25))
    #Fill in end
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    do_with_email('HELO Alice\r\n', 250)

    do_with_email('AUTH LOGIN\r\n', 334)# Auth
    do_with_email(my_account.username + '\r\n', 334)# username
    do_with_email(my_account.authcode + '\r\n', 235)# password

    # Send MAIL FROM command and print server response.
    # Fill in start
    mail_from = 'MAIL FROM: <' + my_account.from_address + '>\r\n'
    do_with_email(mail_from, 250)
    # Fill in end

    # Send RCPT TO command and print server response.
    # Fill in start
    rcpt_to = 'RCPT TO: <' + my_account.to_address + '>\r\n'
    do_with_email(rcpt_to, 250)
    # Fill in end

    # Send DATA command and print server response.
    # Fill in start
    do_with_email('DATA\r\n', 354)
    # Fill in end

    # Send message data.
    # Fill in start
    message = 'from:' + my_account.from_address + '\r\n'
    message += 'to:' + my_account.to_address + '\r\n'
    message += 'subject:' + msg + '\r\n'
    message += 'Content-Type:' + "text/plain" + '\t\n'
    message += '\r\n' + msg
    clientSocket.sendall(message.encode())
    # Fill in end

    # Message ends with a single period.
    # Fill in start
    do_with_email(endmsg, 250)
    # Fill in end

    # Send QUIT command and get server response.
    # Fill in start
    clientSocket.sendall('QUIT\r\n'.encode())
    clientSocket.close()
    # Fill in end
