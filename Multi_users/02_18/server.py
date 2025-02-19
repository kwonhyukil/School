import socket
import threading
import json

# 서버 설정
HOST = "127.0.0.1"  # 로컬 호스트 (내 컴퓨터에서만 실행할 경우)
PORT = 12345  # 사용할 포트 번호

clients = {}  # 클라이언트 목록 {닉네임: 소켓}

def broadcast_message(message, sender_nickname=None):
    """모든 클라이언트에게 메시지 전송"""
    message_data = json.dumps({
        "type": "message",
        "from": sender_nickname if sender_nickname else "서버",
        "content": message
    })
    for sock in clients.values():
        sock.sendall(message_data.encode("utf-8"))

def handle_client(client_socket, nickname):
    """클라이언트가 보낸 메시지 처리"""
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break  # 클라이언트 연결 종료

            message = json.loads(data)

            if message["type"] == "broadcast":
                broadcast_message(message["content"], sender_nickname=nickname)

            elif message["type"] == "private":
                recipient = message["recipient"]
                if recipient in clients:
                    private_msg = json.dumps({
                        "type": "private",
                        "from": nickname,
                        "content": message["content"]
                    })
                    clients[recipient].sendall(private_msg.encode("utf-8"))
                else:
                    error_msg = json.dumps({
                        "type": "notice",
                        "content": f"{recipient} 닉네임을 가진 사용자가 없습니다."
                    })
                    client_socket.sendall(error_msg.encode("utf-8"))

            elif message["type"] == "exit":
                break  # 클라이언트가 종료 명령을 보냄

        except Exception as e:
            print(f"[오류] {e}")
            break

    print(f"[퇴장] {nickname}님이 채팅을 떠났습니다.")
    del clients[nickname]
    client_socket.close()

def start_server():
    """서버 실행"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"🔵 서버가 {HOST}:{PORT}에서 실행 중...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"🔗 새 클라이언트 연결: {addr}")

        # 닉네임 요청
        client_socket.sendall(json.dumps({"type": "request", "content": "닉네임을 입력하세요"}).encode("utf-8"))
        data = client_socket.recv(1024).decode("utf-8")
        nickname_data = json.loads(data)

        if nickname_data["type"] == "nickname":
            nickname = nickname_data["content"]

            if nickname in clients:
                client_socket.sendall(json.dumps({"type": "error", "content": "닉네임이 이미 사용 중입니다."}).encode("utf-8"))
                client_socket.close()
                continue

            clients[nickname] = client_socket
            client_socket.sendall(json.dumps({"type": "success", "content": "연결 성공"}).encode("utf-8"))
            print(f"👤 {nickname}님이 입장했습니다.")

            # 클라이언트 스레드 시작
            client_thread = threading.Thread(target=handle_client, args=(client_socket, nickname))
            client_thread.start()

if __name__ == "__main__":
    start_server()
