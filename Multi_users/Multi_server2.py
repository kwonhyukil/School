import socket       # 네트워크 소켓 통신을 위한 라이브러리
import threading    # 멀티스레드 처리를 위한 라이브러리

# 서버 IP 주소와 포트 번호 설정
HOST = "127.0.0.1"
PORT = 12345

# 연결된 클라이언트 소켓을 저장하는 리스트와 해당 리스트 보호를 위한 락
client_list = []
client_list_lock = threading.Lock()

# 클라이언트와 통신을 처리하는 함수
def handler_client(client_socket: socket.socket, client_addr):
    """ 
    클라이언트와 메시지를 주고받고, 연결이 종료되면 목록에서 제거하는 함수
    """
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            rcvd_msg = client_socket.recv(1024).decode('utf-8')

            # 메시지가 비어 있으면 (연결 종료), 루프 종료
            if not rcvd_msg:
                break

            # 메시지에 클라이언트 주소 추가하여 포맷팅
            rcvd_msg = f"{client_addr}: {rcvd_msg}"

            # 연결된 다른 클라이언트들에게 메시지 브로드캐스트 (락을 사용해 리스트 보호)
            with client_list_lock:
                for socket_item in client_list:
                    if socket_item != client_socket:  # 본인에게는 메시지 전송 안 함
                        try:
                            # 메시지 전송
                            socket_item.sendall(rcvd_msg.encode("utf-8"))
                        except:
                            # 전송 실패 시 해당 클라이언트 소켓을 목록에서 제거하고 닫기
                            client_list.remove(socket_item)
                            socket_item.close()

    except Exception as e:
        # 예외 발생 시 오류 메시지 출력
        print(f"[ERROR] Client {client_addr} error: {e}")

    finally:
        # 클라이언트 연결 종료 시 리스트에서 제거
        with client_list_lock:
            if client_socket in client_list:
                client_list.remove(client_socket)

        # 소켓 닫기
        client_socket.close()
        print(f"Client {client_addr} disconnected")

# 서버 소켓 생성 및 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))  # 서버 소켓 바인딩 (IP, 포트)
server_socket.listen(5)           # 최대 5개의 클라이언트 대기 설정

print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        # 현재 연결된 클라이언트 수 출력
        print(f"Connected clients: {len(client_list)}")

        # 클라이언트의 연결 요청 수락
        client_socket, client_addr = server_socket.accept()
        print(f"Client connected: {client_addr}")

        # 연결된 클라이언트를 리스트에 추가
        with client_list_lock:
            client_list.append(client_socket)

        # 클라이언트와의 통신을 처리할 스레드 생성 및 실행
        client_thread = threading.Thread(target=handler_client, args=(client_socket, client_addr), daemon=True)
        client_thread.start()  # 스레드 실행

except KeyboardInterrupt:
    # 키보드 인터럽트(Ctrl+C)로 서버 종료
    print("\n[INFO] Server shutting down...")

finally:
    # 모든 클라이언트 소켓 닫기
    with client_list_lock:
        for client_socket in client_list:
            client_socket.close()

    # 서버 소켓 닫기
    server_socket.close()
    print("[INFO] Server closed")
