import socket
import threading


HOST = "210.101.236.164" 
PORT = 12345       

# 🚀 메시지 송신 스레드 (귓속말 포함)
def send_message(sock, nickname):
    """클라이언트 → 서버 메시지 송신 (일반/귓속말)"""
    while True:
        try:
            # 사용자 입력
            msg = input(f"[{nickname}] ")

            # ▶ [종료 처리]: 사용자가 'exit' 입력 시 서버에 알림 후 종료
            if msg.lower() == "exit":
                sock.sendall("/exit".encode('utf-8'))
                break

            # ▶ [귓속말 처리]: '/pm 닉네임 메시지' 형식인 경우
            if msg.startswith("/pm"):
                parts = msg.split(' ', 2)  # "/pm", "닉네임", "메시지"로 분리
                if len(parts) < 3:
                    print("[사용법] /pm 닉네임 메시지 형식으로 입력하세요.")
                    continue

                target_nickname = parts[1]  # 수신자 닉네임
                private_msg = parts[2]     # 전달할 메시지
                
                # 서버로 귓속말 명령 송신
                # 예) "/pm Alice 안녕하세요"
                sock.sendall(f"/pm {target_nickname} {private_msg}".encode('utf-8'))
                print(f"[나 -> {target_nickname}] {private_msg}")

            # ▶ [일반 메시지 처리]: /pm 없이 일반 채팅
            else:
                sock.sendall(msg.encode('utf-8'))

        except Exception as e:
            print(f"[송신 오류] {e}")
            break

    sock.close()

# 🚀 메시지 수신 스레드 (귓속말 포함)
def receive_message(sock, nickname):
    """서버 → 클라이언트 메시지 수신 (일반/귓속말)"""
    while True:
        try:
            # 서버로부터 메시지 수신
            data = sock.recv(1024).decode('utf-8')

            # 서버 연결이 종료되었으면 루프 종료
            if not data:
                break

            # ▶ [귓속말 출력 처리]:
            #    - 서버에서 "[귓속말] 송신자: 메시지" 포맷으로 전송됨
            if data.startswith("[귓속말]"):
                print(f"\r💌 {data}\n[{nickname}] ", end="")
            elif data.startswith("[나 ->"):
                # 자신이 보낸 귓속말 송신 확인 메시지 출력
                print(f"\r📨 {data}\n[{nickname}] ", end="")
            else:
                # ▶ [일반 메시지 출력]
                print(f"\r{data}\n[{nickname}] ", end="")

        except Exception as e:
            print(f"[수신 오류] {e}")
            break

    print("[연결 종료] 서버와의 연결이 끊어졌습니다.")
    sock.close()

try:
    # ▶ [서버 연결]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # ▶ [닉네임 설정]
    nickname = input("닉네임을 입력하세요: ").strip()
    client_socket.sendall(nickname.encode('utf-8'))

    # ▶ [스레드 실행]
    #  1. 송신 스레드: send_message()
    #  2. 수신 스레드: receive_message()
    send_thread = threading.Thread(target=send_message,\
                                    daemon=True,\
                                    args=(client_socket, nickname))
    receive_thread = threading.Thread(target=receive_message,\
                                    daemon=True,\
                                    args=(client_socket, nickname))

    send_thread.start()
    receive_thread.start()

    send_thread.join()

except Exception as e:
    print(f"[클라이언트 오류] {e}")
    client_socket.close()
    
    

