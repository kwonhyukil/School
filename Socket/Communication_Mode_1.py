import socket
import threading

HOST = "210.101.236.164"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))



is_active = [True] # 전역 변수

# 전역변수
# is_active[0] = True

# Tx
# 전역변수의 값을 공유 받음
# 전역 변수의 값을 공유 하기 때문에 Rx에서 False 로 바뀌게 되면 똑같이 바뀌게 된다.


# Rx
# 전역변수의 값을 공유 받음
# break가 실행 되면 공유 받은 is_active의 값이 False 로 바뀌게 된다.

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
        # recv = 블로킹 함수 .. 상대방으로부터 데이터가 올 때까지
        rcvd_msg = client_socket.recv(1024).decode('utf-8')

        if not rcvd_msg:
            break
        
        print(f"Received msg: {rcvd_msg}")
        
    is_active[0] = False



thread_tx = threading.Thread(target=handler_tx, args=(client_socket,))
thread_rx = threading.Thread(target=handler_rx, args=(client_socket,))

thread_tx.start()
thread_rx.start()

thread_rx.join()
thread_tx.join()
