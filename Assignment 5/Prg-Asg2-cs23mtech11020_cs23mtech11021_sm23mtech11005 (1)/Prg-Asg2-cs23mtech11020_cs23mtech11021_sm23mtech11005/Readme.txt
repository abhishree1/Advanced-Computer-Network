To run the the different python programs included in the zip file traverse to the directory where the zip file is extracted(make sure it is an empty directory initially) using following command:
	cd path_of_directory/

How to run the various scripts:
1. Client.py:
If you want to fetch data from the server without using web proxy, run the below command:

	python3 Client.py ip-address port_number path_of_file 

Examples:
	python3 Client.py 192.168.137.85 12000 /index.html
	python3 Client.py cse.iith.ac.in 443 /

If you want to include web proxy then run the below command:

	python3 Client.py ip-address port_number path_of_file proxy_address proxy_port_number
	python3 Client.py cse.iith.ac.in 443 / 192.168.137.85 12001

2. Proxy.py:
To run web proxy run the below command:

python3 Proxy.py

If you want to connect your browser to web proxy, then follow these steps:
	a. Open web browser 
	b. Open Setting
	c. Search for proxy and open the proxy setting
	d. Choose Set up manual proxy
	e. Enter proxy ip address and port number in http and https setting
	f. Click Save/ok
	
This proxy server does not work with web servers which don’t host the file using http and exclusively use https.
	
To change the ip address and port number to which proxy server binds, change the values assigned to variables HOST and PORT respectively in file Proxy.py.

3. Server.py
To run web server enter the below command:
	python3 Server.py

To change the ip address and port number to which server binds, change the values assigned to variables HOST and PORT respectively in file Server.py.


4. ExtendedClient.py:
If you want to fetch data from the server without using web proxy, run the below command:

	python3 ExtendedClient.py ip-address port_number path_of_file

If you want to include web proxy the run the below command:

	python3  ExtendedClient.py ip-address port_number path_of_file proxy_address proxy_port_number

