from socket import *
import threading #this library will help us make a multithreaded proxy
import ssl  #used to create ssl sockets for https connection

# Define the proxy_server's host and port
HOST = '172.16.163.218'  
PORT = 12001

#creating socket
def create_socket(addr, port):
	clientSocket=socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((addr, int(port)))
	if port=='443':
		context_ssl=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		clientSocket=context_ssl.wrap_socket(clientSocket, server_hostname=addr)
	return clientSocket


#client thread functions to handle various clients
def client_thread(client_socket):
	request = client_socket.recv(1024).decode()
	print(f"Received request:\n{request}")
	serverPort=''

	#assigning appropriate port for further connection to server
	if 'CONNECT' in request:
		serverPort='443'
	
	if len(request.split('Host: ')[1].split('\r\n')[0].split(':'))>1:
		serverPort = request.split('Host: ')[1].split('\r\n')[0].split(':')[1]
	
	if serverPort=='':
		serverPort='80'
	serverAddress=request.split('Host: ')[1].split('\r\n')[0].split(':')[0]
	
	#creating socket for client
	clientSocket=create_socket(serverAddress, serverPort)
	print("\nconnection established to server: "+serverAddress)
	message=request
	message=message.encode()
	clientSocket.send(message)
	message= clientSocket.recv(1024)
	
	reply=b''
	while(len(message)):
		reply+=message
		message= clientSocket.recv(1024)
	clientSocket.close()
	print("\nReply from server",reply.decode())
	# save received file
	f=open('buffered_file', 'wb')
	f.write(reply)
	f.close()

	fi=open('buffered_file', 'rb')
	content = fi.read()
	while content:
		
		client_socket.send(content)
		content = fi.read()
	fi.close()	
	
    # Close the client connection
	client_socket.close()


# Create a socket to listen for incoming connections
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Listen for one incoming connection

print(f"Proxy server listening on {HOST}:{PORT}")


while True:
    # Accept a client connection
	client_socket, client_address = server_socket.accept()
	print(f"Accepted connection from {client_address}")
	threading._start_new_thread(client_thread, (client_socket,))
    

# Close the server socket
server_socket.close()
