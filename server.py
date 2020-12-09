"""
Server for multithreaded (asynchronous) chatbox 
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


"""
Dictionaries to store information of users
connected to the chatbox
"""

usernames = {}
addresses = {}

"""
Constant variables
"""
HOST = "127.0.0.1"
PORT = 33000
BUFFERSIZE = 1024 # buffer size in KB
FORMAT = "utf8" # Format of the content we're sending
ADDR = (HOST, PORT) # This is the socket, combo of host and port
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # Binding the address, meaning we're connecting the socket


"""
Function for server to accept incoming connections
"""
def accept_incoming_connections():
    # Continuously wait for a new connection
    while True:
        # Accept a new connection from a user
        user, user_address = SERVER.accept()
        print("%s:%s has connected." % user_address)
        
        # Respond to the user, ask for their name
        user.send(bytes("Welcome to the chat! What's your name?", FORMAT))

        # Save the user's address
        addresses[user] = user_address

        # Call handle_user function below
        Thread(target=handle_user, args=(user,)).start()

"""
Function to handle a connected user / connection
- Asks for the user's name and sends welcome message when user first joins chat
- Creates infinite loop to listen and handles messages sent by user
"""
def handle_user(user):
    # Get the user's name then send a welcome message
    name = user.recv(BUFFERSIZE).decode(FORMAT) 
    welcome = "Welcome %s! If you ever want to quit, type {quit} to exit.\n" % name
    user.send(bytes(welcome, FORMAT))

    # Tell everyone a user just joined chat
    message = "%s has joined the chat!" % name
    broadcast(bytes(message, FORMAT))

    # Store their name in our usernames database (DB)
    usernames[user] = name

    # This is the main loop that will wait for each user to send 
    # their messages and process it
    while True:
        message = user.recv(BUFFERSIZE)
        # Broadcast the message into the chat room
        if message != bytes("{quit}", FORMAT):
            broadcast(message, name + ": ")
        # If they send {quit}, close the connection.
        else:
            user.send(bytes("{quit}", FORMAT))
            user.close()

            # Grab the address that's disconnecting
            user_address = addresses[user]
            
            # Delete info about the user from DBs
            del usernames[user] 
            del addresses[user]

            broadcast(bytes("%s has left the chat :(" % name, FORMAT))
            print("%s:%s has disconnected." % user_address)
            
            break

"""
Function to broadcast a message to everyone in the chat room
"""
def broadcast(message, prefix=""):
    for sock in addresses:
        sock.send(bytes(prefix, FORMAT)+message)

"""
MAIN FUNCTION - This is where we start our server
Note: All classes have a main function
"""
if __name__ == "__main__":
    # listens for 5 connections at max
    SERVER.listen(5)

    # Prints in the server log that we are ready to accept connections 
    print("Waiting for a connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
    # Starts the thread 
    ACCEPT_THREAD.start()

    # This line waits until all operations are completed before jumping to next line which closes the server
    ACCEPT_THREAD.join()

    SERVER.close()
