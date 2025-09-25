import socket

SERVER_IP = "192.168.1.2"  
SERVER_PORT = 55005          
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send Name + Family Name
    message = "Arthur Hittinger"  
    sock.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))

    # Receive response
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print("Received:", data.decode("utf-8"))

    # Send the response back
    sock.sendto(data, addr)

    #  Receive and print the last response
    final_data, _ = sock.recvfrom(BUFFER_SIZE)
    print("Last Response:", final_data.decode("utf-8"))

finally:
    sock.close()


# I couldn't link with server, " IP and PORT  => No route to host", even no ping with the IP
