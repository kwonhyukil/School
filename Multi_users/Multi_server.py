import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

client_list = []
client_list_lock = threading.Lock()

def handler_client(client_socket: socket.socket, lient_addr):
    """ 클라이언트와 메시지를 주고받고, 연결이 종료되면 목록에서 제거하는 함수"""
    try:
        while True:
            rcvd_msg = client_socket.recv(1024).decode('utf-8')

            if not rcvd_msg:
                break

            rcvd_msg = f"{client_addr}: {rcvd_msg}"

            with client_list_lock:
                for socket_item in client_list:
                    if socket_item != client_socket:
                        try:
                            socket_item.sendall(rcvd_msg.encode("utf-8"))
                        except:
                            client_list.remove(socket_item)
                            socket_item.close()
        
    except Exception as e:
        print(f"[ERROR] Client {client_addr} error: {e}")

    finally:
        with client_list_lock:
            if client_socket in client_list:
                client_list.remove(client_socket)

        client_socket.close()
        print(f"Client {client_addr} disconnected")

# 서버 소켓 생성 및 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        print(f"Connected clients: {len(client_list)}")

        client_socket, client_addr = server_socket.accept()
        print(f"Client connected: {client_addr}")

        with client_list_lock:
            client_list.append(client_socket)

        # 클라이언트 전용 스레드 실행
        client_thred = threading.Thread(target=handler_client, args=(client_socket, client_addr), daemon=True)

except KeyboardInterrupt:
    print("\n[INFO] Server shutting down...")

finally:
    with client_list_lock:
        for client_socket in client_list:
            client_socket.close()

    server_socket.close()
    print("[INFO] Server closed")
