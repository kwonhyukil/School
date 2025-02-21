import socket

# 서버 주소 및 포트 설정
HOST = '127.0.0.1'  # 접속할 서버의 IP 주소 (로컬호스트)
PORT = 12345        # 서버가 수신 대기하는 포트 번호

# TCP 소켓 생성 (IPv4, TCP 방식)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결 요청 (블로킹 상태, 서버가 응답할 때까지 대기)
client_socket.connect((HOST, PORT))

while True:
    # 사용자 입력을 받아 메시지를 전송 (블로킹 상태)
    message = input("메시지 입력 (종료: exit): ")
    
    # 사용자가 'exit'을 입력하면 연결 종료
    if message.lower() == "exit":
        break
    
    # 입력받은 문자열을 UTF-8로 인코딩하여 서버에 전송
    # 블로킹 상태 (모든 데이터 전송 후 다음 코드 실행)
    client_socket.sendall(message.encode())
    
    # 서버로부터 응답 데이터 수신 (최대 1024 바이트, 블로킹 상태)
    data = client_socket.recv(1024)
    
    # 수신한 데이터를 디코딩하여 출력
    print(f"서버 응답: {data.decode()}")

# 클라이언트 소켓 종료 (서버와의 연결 해제)
client_socket.close()

