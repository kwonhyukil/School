import socket       # 네트워크 소켓 통신을 위한 라이브러리
import threading    # 멀티스레드 처리를 위한 라이브러리

# 서버의 IP 주소와 포트 번호 (서버 코드와 동일하게 설정)
HOST = "127.0.0.1"
PORT = 12345

# 서버로부터 메시지를 수신하는 함수
def receive_messages(client_socket):
    while True:
        try:
            # 서버로부터 메시지 수신 및 출력
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                print("서버 연결이 종료되었습니다.")
                break
            print(msg)
        except Exception as e:
            print(f"[ERROR] 메시지 수신 오류: {e}")
            break

# 서버에 연결
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # 서버에 연결 요청
    print(f"서버에 연결되었습니다: {HOST}:{PORT}")

    # 서버로부터 메시지를 수신하는 스레드 시작
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    recv_thread.start()

    # 사용자로부터 메시지를 입력받아 서버로 전송
    while True:
        msg_to_send = input()  # 사용자 입력
        if msg_to_send.lower() == "exit":  # "exit" 입력 시 종료
            print("서버와의 연결을 종료합니다.")
            break
        client_socket.sendall(msg_to_send.encode('utf-8'))  # 서버에 메시지 전송

except Exception as e:
    print(f"[ERROR] 서버에 연결할 수 없습니다: {e}")

finally:
    # 소켓 닫기
    client_socket.close()
    print("클라이언트가 종료되었습니다.")
