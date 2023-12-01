#Content of main.py; use as is
from tkinter import *
import multiprocessing

import client
import server

if __name__ == "__main__":
    server = multiprocessing.Process(target=server.main)
    client1 = multiprocessing.Process(target=client.main, name="Client1")
    client2 = multiprocessing.Process(target=client.main, name="Client2")
    server.start()
    client1.start()
    client2.start()

    server.join()
    client1.join()
    client2.join()

    