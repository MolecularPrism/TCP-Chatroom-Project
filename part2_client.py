from tkinter import *
import socket
import threading

class ChatClient:
    def __init__(self, window):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.client_socket.connect(('127.0.0.1', 3333))

        # Start a thread to handle receiving messages
        threading.Thread(target=self.receive_messages, args=(window,)).start()
        
        self.client_num = int()
        self.client_addr = int()
        self.GUI_setup(window)
        window.bind('<Return>', self.send_message)

    def GUI_setup(self, window):
        window.title(f"Chat Client {self.client_num + 1}")

        self.messages_text = Text(window, font=("Arial", 12))
        self.messages_text.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.addr_label = Label(window, text=f" ", font=("Arial", 14))
        self.addr_label.pack(side=TOP, anchor='w', padx=10)
        
        # Create a frame for message label and entry
        self.message_frame = Frame(window)
        self.message_frame.pack(side=TOP, anchor='w', padx=10, pady=5)
        
        self.message_label = Label(self.message_frame, text="Chat message: ", font=("Arial", 14))
        self.message_label.pack(side=LEFT)
        
        # This is the entry for where the client can enter messages 
        self.entry = Entry(self.message_frame, width=50)
        self.entry.pack(side=LEFT)
        
        self.history_label = Label(window, text="Chat History:", font=("Arial", 14))
        self.history_label.pack(side=TOP, anchor='sw', padx=10)

    def receive_messages(self, window):
        while True:
            try:
                message = self.client_socket.recv(4096).decode("utf-8")

                #check if message is valid, if it is we display on the log
                if(message != None and "(special_code)" not in message):
                    if(self.client_num == 1):
                        self.messages_text.insert(END, f"Client 2: {message}\n")
                        
                    else:
                        self.messages_text.insert(END, f"Client 1: {message}\n")

                elif("(special_code)" in message):
                    self.client_num = int(message[22])
                    self.client_addr = int(message[29:])
                    print(f"client number is {self.client_num} and client address is {self.client_addr}\n")
                    window.title(f"Chat Client {self.client_num}")

                    # self.client_num_label.config(text=f"Client {self.client_num}")
                    self.addr_label.config(text=f"Client{self.client_num} @port #{self.client_addr}")

            except:
                print("error in receiving message")
                self.client_socket.close()


    def send_message(self, e):
        message = self.entry.get()
        if (len(message) > 0):
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.entry.delete(0, END)
                self.messages_text.insert(END, f"                            Client {self.client_num}: {message}\n")
                self.messages_text.see(END)  # Scroll to the end
            except:
                print("ERROR in send")
                self.client_socket.close()

def main():
    window = Tk()
    ChatClient(window)
    window.mainloop()

if __name__ == '__main__':
    main()
