# test_server.py

import socket
import threading

HOST = "127.0.0.1" # 서버의 IP 주소 -> 문자형
PORT = 12345 # 포트 주소 -> 정수형


is_active = [True]

# 데이터 전송
def handler_tx(client_socket:socket.socket):
    while is_active[0]:
        send_msg = input("Text : ")
        
        if send_msg.lower() == "exit":
            client_socket.close()
            is_active[0] = False
            break
        
        client_socket.sendall(send_msg.encode('utf-8'))

# 데이터 수신
def handler_rx(client_socket:socket.socket):
    while is_active[0]:
        rcvd_msg = client_socket.recv(1024).decode('utf-8')
        
        if not rcvd_msg:
            break
        
        print(f"Received msg: {rcvd_msg}")
        
    is_active[0] = False
    
    
# socket 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind
server_socket.bind((HOST, PORT))

# listen
server_socket.listen(1)

print(f"[Listen] {HOST}, {PORT}")

client_socket, client_addr = server_socket.accept() 

thread_tx = threading.Thread(target=handler_tx, args=(client_socket,))
thread_rx = threading.Thread(target=handler_rx, args=(client_socket,))

thread_tx.start()
thread_rx.start()

thread_rx.join()
thread_tx.join()
