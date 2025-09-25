import socket
import threading
import logging

def handle_client(client_socket, address, lock):
    with client_socket:
        request = client_socket.recv(1024).decode('utf-8')
        
        # Log request 
        with lock:
            logging.info(f"Received request from {address}:")
            logging.info(request)
        
        # Check request and extract numbers and operation
        try:
            lines = request.split("\r\n")
            if len(lines) > 0:
                operator, operand1, operand2 = lines[-1].split()
                operand1, operand2 = int(operand1), int(operand2)
                
                # Compute
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
            else:
                compute = "Error compute"
        except Exception:
            result = "Error"
        #result
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str(result))}\r\n\r\n{result}"
        client_socket.sendall(response.encode('utf-8'))

def start_server(host='127.0.0.1', port=55000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)  # up to 10 connections
    
    print(f"Server listening on {host}:{port}")
    logging.basicConfig(level=logging.INFO, format='%(threadName)s - %(message)s')
    lock = threading.Lock()
    
    while True:
        client_socket, address = server.accept()
        print(f"Accepted connection from {address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address, lock))
        client_handler.start()

if __name__ == "__main__":
    start_server()
