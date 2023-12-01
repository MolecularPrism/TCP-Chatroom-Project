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
            print(f"Connection from {client_address}")

            # Add the new client to the list
            self.clients.append(client_socket)

            # Start a thread to handle messages from this client
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')

                # Broadcast the message to all other clients
                for client in self.clients:
                    if client != client_socket:
                        try:
                            client.send(message.encode('utf-8'))
                        except socket.error:
                            # If the send operation fails, remove the client
                            self.clients.remove(client)

                # Update the GUI with the received message
                self.messages_text.insert(END, f"{message}\n")
                self.messages_text.see(END)  # Scroll to the end

            except Exception as e:
                print(f"Error handling client: {e}")
                break

def main():
    window = Tk()
    ChatServer(window)
    window.mainloop()

if __name__ == '__main__':
    main()
