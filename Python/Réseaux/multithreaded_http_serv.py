import socket
import re
import threading
import time

def parse_request(request):
    match = re.search(r'\r\n\r\n(\d+)([+\-*/])(\d+)', request)
    if match:
        operand1, operator, operand2 = match.groups()
        operand1, operand2 = int(operand1), int(operand2)
        if operator == "-":
            compute = operand1 - operand2
        elif operator == "+":
            compute = operand1 + operand2
        elif operator == "*":
            compute = operand1 * operand2
        elif operator == "/" and operand2 != 0:
            compute = operand1 // operand2
        else:
            compute = "Wrong operator"

def generate_response(result):
    result_str = str(result)
    response = (f"HTTP/1.1 200 OK\r\n"
                f"Date: {time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())}\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(result_str)}\r\n\r\n"
                f"{result_str}")
    return response

def handle_client(client_socket, addr, lock):
    request = client_socket.recv(1024).decode()
    with lock:
        print(f"Received request from {addr}:\n{request}")
    
    result = parse_request(request)
    response = generate_response(result)
    
    client_socket.sendall(response.encode())
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 55000))
    server_socket.listen(10)
    print("Server listening on port 55000...")
    
    lock = threading.Lock()
    
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr, lock))
        thread.start()

if __name__ == "__main__":
    start_server()
