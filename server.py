from tkinter import *
import socket
import threading

class ChatServer:
    def __init__(self, window):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.GUI_setup(window)

        self.server_socket.bind(("127.0.0.1", 3333))
        self.server_socket.listen(5)

        self.clients = []
        self.client_num = []

        print("Server ready to receive")

        # Thread for accepting client connections
        threading.Thread(target=self.accept_clients).start()

    def GUI_setup(self, window):
        window.title("Chat Server")
        window.geometry("400x300")

        self.messages_text = Text(window)
        self.messages_text.pack(fill=BOTH, expand=True)

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()

            # Add the new client to the list
            self.clients.append(client_socket)

            print(f"Connection from {client_address}")

            
         

            #here we need to assign each client their #s
            for client in self.clients:

                print(f"client is {client} and len is {len(self.clients)}\n")
        
                self.client_num.append(self.clients.index(client) + 1)

                #send client # to each client
                message = f"(special_code) Client {self.clients.index(client) + 1}"
                
                client.send(message.encode('utf-8'))




            # Start a thread to handle messages from this client
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8') #get message from a client


                #deliver that message to the OTHER client 
                for client in self.clients:
                    if client != client_socket: #other client
                        try:
                            client.send(message.encode('utf-8'))
                        except socket.error:
                            # If the send operation fails, remove the client
                            self.clients.remove(client)

                # Update the GUI with the received message
             

                self.messages_text.insert(END, f"Client {self.client_num[self.clients.index(client_socket) + 1]}: {message}\n")
               

            except Exception as e:
                print(f"Error handling client: {e}")
                break

def main():
    window = Tk()
    ChatServer(window)
    window.mainloop()

if __name__ == '__main__':
    main()
