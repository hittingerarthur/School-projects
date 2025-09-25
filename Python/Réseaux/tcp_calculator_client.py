import socket

# Server details
SERVER_IP = "127.0.0.1"  
SERVER_PORT = 55000           


# Get user input
name = input("Enter your name: ")
operand1 = input("Enter first integer: ")
operator = input("Enter operator (+, -, *, /): ")
operand2 = input("Enter second integer: ")


if operator == "-" :
    compute = operand1 - operand2
elif operator == "+" :
    compute = operand1 + operand2
elif operator == "*" :
    compute = operand1 * operand2
elif operator == "/" and operand2 != 0:
    compute = operand1 / operand2 
else :
    print(" Impossible !")
    
compute = operand1 + operator + operand2

# Create POST request

post_data = f"{operand1}=3&{operator}=*&{operand2}=4&{compute}=txt"
post_request = f"POST /calculate HTTP/1.1\r\nHost: {SERVER_IP}\r\nContent-Length: {len(post_data)}\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{post_data}"

#  Send request using a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))
sock.sendall(post_request.encode("ascii"))

# Receive and print response
response = sock.recv(1024)
print("Response from server:\n", response.decode("ascii"))

sock.close()

