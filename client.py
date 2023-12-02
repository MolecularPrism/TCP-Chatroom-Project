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
        self.GUI_setup(window)
        window.bind('<Return>', self.send_message)

        

        
        

    def GUI_setup(self, window):
        window.title(f"Chat Client {self.client_num}")

        self.messages_text = Text(window)
        self.messages_text.pack(fill=BOTH, expand=True)

        self.entry = Entry(window)
        self.entry.pack()

        send_btn = Button(window, text="Send", command=self.send_message)
        send_btn.pack()
        




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
                    self.client_num = int(message[-1])
                    print(f"client number is {self.client_num}")
                    window.title(f"Chat Client {self.client_num}")
            except:
                print("error in receiving message")
                self.client_socket.close()


    def send_message(self, e):
        message = self.entry.get()
        if (message != None):
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.entry.delete(0, END)
                self.messages_text.insert(END, f"                   Client {self.client_num}: {message}\n")
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
