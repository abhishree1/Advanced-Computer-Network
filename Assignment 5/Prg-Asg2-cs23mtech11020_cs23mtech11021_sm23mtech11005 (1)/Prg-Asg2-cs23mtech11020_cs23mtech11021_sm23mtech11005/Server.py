from socket import *
import os #used to check if file asked is present in the server
import threading #this library will help us make a multithreaded proxy

# Define the server's host and port
HOST = '127.0.0.1'
PORT = 12002

#client thread functions to handle various clients
def client_thread(client_socket):
	# Receive the client's request
	request = client_socket.recv(1024).decode()
	print(f"Received request:\n{request}")

    # Parse the request to get the requested file path
	try:
        # Extract the requested filename from the GET request
		file_path = request.split()[1]
		if file_path[0] == '/':
			file_path = file_path[1:]  # Remove the leading '/' character
		if file_path == '':
			file_path = 'index.html'
	except Exception as e:
		print(f"Failed to parse request: {e}")

    # Check if the requested file exists
	if os.path.isfile(file_path):
		fi=open(file_path, 'rb')
		content = fi.read()
		response = "HTTP/1.0 200 OK\r\nContent-Length: {len(content)}\r\n\r\n" #to be sent back to requesting client
		client_socket.send(response.encode())
		while content:
			client_socket.send(content)
			content = fi.read()
		fi.close()	
	else:
		not_found_response = "HTTP/1.0 404 Not Found\r\n\r\n"
		client_socket.send(not_found_response.encode())

    # Close the client connection
	client_socket.close()


# Create a socket to listen for incoming connections
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Listen for incoming connection

print(f"\nServer listening on {HOST}:{PORT}")


while True:
    # Accept a client connection
	client_socket, client_address = server_socket.accept()
	print(f"Accepted connection from {client_address}")
	threading._start_new_thread(client_thread, (client_socket,))
    

# Close the server socket
server_socket.close()
