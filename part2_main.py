#Content of main.py; use as is
from tkinter import *
import multiprocessing

import part2_client
import part2_server

if __name__ == "__main__":
    server = multiprocessing.Process(target=part2_server.main)
    client1 = multiprocessing.Process(target=part2_client.main, name="Client1")
    client2 = multiprocessing.Process(target=part2_client.main, name="Client2")
    server.start()
    client1.start()
    client2.start()

    # server.join()
    # client1.join()
    # client2.join()

    