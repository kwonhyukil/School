import socket

# 서버 설정
HOST = '127.0.0.1'  # 서버가 바인딩할 IP 주소 (로컬호스트)
PORT = 12345        # 사용할 포트 번호

# 소켓 생성 (IPv4, TCP 방식)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# IP 및 포트 바인딩
server_socket.bind((HOST, PORT))

# 클라이언트의 접속 요청을 받을 수 있도록 대기 상태 설정 
# (최대 5개의 대기 큐 크기 설정)
server_socket.listen(5)
print(f"서버가 {HOST}:{PORT}에서 대기 중...")

while True:
    # 클라이언트의 연결 요청을 수락하고, 
    # 새로운 소켓과 클라이언트 주소 반환 (블로킹 상태)
    client_socket, addr = server_socket.accept()
    print(f"클라이언트 {addr} 연결됨")
    
    while True:
        # 클라이언트로부터 데이터 수신 
        # (최대 1024 바이트, 블로킹 상태)
        data = client_socket.recv(1024)
        
        # 클라이언트가 연결을 종료하면 루프 탈출
        if not data:
            break
        
        # 받은 데이터를 문자열로 변환하여 출력
        print(f"받은 데이터: {data.decode()}")  
        
        # 받은 데이터를 클라이언트에게 그대로 다시 전송 (에코 서버)
        # 블로킹 상태 (모든 데이터 전송 후 다음 코드 실행)
        client_socket.sendall(data)  

    # 클라이언트 소켓 종료
    client_socket.close()
