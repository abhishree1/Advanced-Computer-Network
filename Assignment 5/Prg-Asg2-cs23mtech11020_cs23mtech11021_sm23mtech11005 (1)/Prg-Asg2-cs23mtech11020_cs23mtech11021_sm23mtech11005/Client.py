#Client.py
from socket import *
import sys  #used to take arguments from command line
import re	#used to parse index file for paths
import ssl	#used to create ssl sockets for https connection
import time	#used to check latency

#function used to create a socket for the client based on the port(https or normal http)
def create_socket(addr, port):
	clientSocket=socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((addr, int(port)))
	if port=='443':
		context_ssl=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		clientSocket=context_ssl.wrap_socket(clientSocket, server_hostname=addr)
	return clientSocket

#parsing function to get object paths
def parse(in_file, tag, attr):
	objects=in_file.split(tag)
	paths=[]
	for obj in objects[1:]:
		obj_src=re.search(attr+b'="(.+?)"',obj)
		if(obj_src is None):
			obj_src=re.search(attr+b"='(.+?)'",obj)
		if(obj_src is not None):
			paths+=[obj_src.group(1)]
	return paths


#this function helps in getting the host and relative address separated out from the path we get from parse function
def find_host_path(path, Address):
	if(path.find('://')!=-1):
		path=path[path.find('://')+3:]
	if path.find('/')!=-1 and path.split('/')[0].find('.')!=-1 and len(path.split('/')[0])>2:
		host, rel_path=path.split('/',1)
	else:
		host=''
		if(len(path.split('/'))>1 and path.split('/')[0].find('.')!=-1):
			rel_path=path[len(path.split('/')[0])+1:]
		else:
			rel_path=path
	if host=='':
		host=Address
	if(len(rel_path)>0 and rel_path[0]!='/'):
		rel_path='/'+rel_path
	return host, rel_path

# for downloading the object, given its path, Hostname and portno for creating socket, and, serverPort and serverAddr for request message 
def objectDownloader(path, Hostname, portno, serverAddr, serverPort):
	clientSocket=create_socket(Hostname, portno)
	host, rel_path=find_host_path(path.decode(), serverAddr)

	#request message to be sent to server
	message = "GET "+rel_path + " HTTP/1.0\r\n"
	message += "Host: "+host+":"+serverPort+"\r\n\r\n"

	file_name=path.split(b'/')[-1]

	print("\nconnection established to get object at: "+host+rel_path)
	print("object name: "+file_name.decode())
	message=message.encode()
	clientSocket.send(message)
	message= clientSocket.recv(1024)
	reply=b''
	while(len(message)):
		reply+=message
		message= clientSocket.recv(1024)

	clientSocket.close()
	print("connection closed for object: "+file_name.decode())

	headers=reply.split(b'\r\n\r\n')[0]
	print("Header of reply from server:")
	print(headers.split(b'\r\n')[0].decode())
	img_file=reply[len(headers)+4:]
	#save object file
	if(file_name.decode()!=''):
		f=open("Downloads/"+file_name.decode(), 'wb')
		f.write(img_file)
		f.close()


#!!!the python script begins execution from here:

arglen=len(sys.argv) #this is the number of command line arguments

#checking if we get proxy address and port as input and setting up Hostname and portno as a logical consequence
if(arglen==4):
	Hostname=sys.argv[1]
	portno=sys.argv[2]
else:
	Hostname=sys.argv[4]
	portno=sys.argv[5]
exit_after_call1=False

#check if file asked by user is html or not
if(len(sys.argv[3])>1):
	user_file_name=sys.argv[3].split('/')[-1]
	user_file_extension=user_file_name.split('.')[-1]
	if(user_file_extension!="html"):
		exit_after_call1=True

print('no. of arguments passed: ', arglen)
clientSocket=create_socket(Hostname, portno)
if(exit_after_call1==True):
	print("\nconnection established to get object specified by user")
else:
	print("\nconnection established to get index file")

message = "GET "+sys.argv[3] + " HTTP/1.0\r\n"
message += "Host: "+sys.argv[1]+":"+sys.argv[2]+"\r\n\r\n"

message=message.encode()
clientSocket.send(message)
message= clientSocket.recv(1024)
reply=b''
while(len(message)):
	reply+=message
	message= clientSocket.recv(1024)

clientSocket.close()
#removing headers from received file:
headers=reply.split(b'\r\n\r\n')[0]
print(headers.decode()+"\n\n")
print("Header of reply from server:")
print(headers.split(b'\r\n')[0].decode())
htmlfile=reply[len(headers)+4:]

#save 1st file asked by user, no parsing is done if file is not html
if(exit_after_call1==True):
	f=open('Downloads/'+user_file_name, 'wb')
else:
	f=open('index.html', 'wb')
f.write(htmlfile)
f.close()

if(exit_after_call1==True):
	sys.exit(0)


#starting timer to calculate latency
start_time=time.time()
#getting images
img_paths=parse(in_file = htmlfile,tag = b'<img ', attr=b'src')
img_paths=img_paths+parse(in_file = htmlfile,tag = b'<img\n', attr=b'src')
i=0
while i<len(img_paths):
	objectDownloader(img_paths[i], Hostname, portno, sys.argv[1], sys.argv[2])
	i=i+1

#getting scripts
scripts_paths=parse(htmlfile, b'<script ', b'src')
i=0
while i<len(scripts_paths):
	objectDownloader(scripts_paths[i], Hostname, portno, sys.argv[1], sys.argv[2])
	i=i+1

#getting link objects(icons, css)

link_paths=parse(htmlfile, b'<link ', b'href')
i=0
while i<len(link_paths):
	objectDownloader(link_paths[i], Hostname, portno, sys.argv[1], sys.argv[2])
	i=i+1


completion_time=time.time()
print("Latency: "+str(completion_time-start_time)+"seconds")