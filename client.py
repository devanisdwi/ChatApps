from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

"""
CONSTANTS
"""
BUFFERSIZE = 1024
FORMAT = "utf8"

def receive():
    #infinity loop yang akan terus menangkap pesan
    while True:
        try:    #error handling
            #get the message from the server
            message = user_socket.recv(BUFFERSIZE).decode(FORMAT)
            #add it to the message list, end agar tersusun kebawah
            message_list.insert(tkinter.END, message)
        except OSError:
            break

def send(event=None):
    #parameter memang built in tkinter for now just ignore
    #function kirim ke orang lain

    #ambil message yang mau dikirim dari input field
    message = my_message.get()

    #clear input fieldnya untuk message lain
    my_message.set("")

    #kirim message ke server untuk dibroadcast ke user lain
    user_socket.send(bytes(message, FORMAT))

    #handling if the user want to {quit}
    if message == "{quit}":
        user_socket.close()
        root.destroy()

def on_closing(event = None):
    #helper function kalau user mau exit chat dari X button
    print("Bubay")

#inisialisasi tkinter dan pembuatan box
root = tkinter.Tk()

#judul pada box
root.title("Please, Chat Me!")

#tata letak pesan
message_frame = tkinter.Frame(root)
#function untuk menyusun seluruh komponen GUI
message_frame.pack()

scrollbar = tkinter.Scrollbar(message_frame)
#penempatan scrollbar dikanan
scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)

#message list
message_list = tkinter.Listbox(message_frame, height=15, width = 50, yscrollcommand = scrollbar.set)
message_list.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
message_list.pack()

#handle X (exit) button
root.protocol("WM_DELETE_WINDOW", on_closing)

#input field untuk user
my_message = tkinter.StringVar()
my_message.set("Type in here..")

input_field = tkinter.Entry(root, textvariable = my_message)
#connecting {return key to command send using press enter}
input_field.bind("<Return>", send)
input_field.pack()

#tombol kirim
send_button = tkinter.Button(root, text = "Send!", command = send)
send_button.pack()

#bikin socket untuk client
HOST = input("Enter Host: ") #untuk testing coba pakai 0.0.0.0
PORT = input("Enter Port: ") #untuk testing coba 33000
#Error Handling untuk Port
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

#socket untuk client
ADDR = (HOST, PORT)
user_socket = socket(AF_INET, SOCK_STREAM)
user_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop() # mulai GUI execution