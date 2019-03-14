import socket
import time
PORT = 9002
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("", PORT)
server_socket.bind(address)
flag = False
now = lambda: int(round(time.time()*1000))
startTime = now()
endTime = now()
datalength = 0
while True:
    receive_data, client_address = server_socket.recvfrom(1024)
    if len(receive_data) <= 0 :
        continue

    if flag == False :
        flag = True
        startTime = now()
        datalength = 0
    
    datalength += len(receive_data)
    endTime = now()
    if endTime == startTime :
        continue

    speed = datalength*8.0/(endTime - startTime)
    print("speed %d Kb/s" %speed )

    if endTime - startTime > 180000 :
        break

server_socket.close()