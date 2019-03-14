import socket
import time
import random
import threading

def action(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("39.96.192.32", 30005) 
    client_socket.bind(("",15002+args))
    tempdata = bytes(1280)
    while True:
        client_socket.sendto(tempdata, server_address)
        # addr = client_socket.getsockname()
        # print("send port:",addr[1])
        # time.sleep(0.001*random.randint(1,999))
        time.sleep(0.002)
        # print("send thread:%s",args)

for i in range(1,2):
    t =threading.Thread(target=action,args=(i,))
    t.start()

print("main thread end");





