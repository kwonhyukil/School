import socket
import threading


# HOST 주소, PORT 주소 입력
HOST = "127.0.0.1"
PORT = 12345
# 클라이언트 소켓 생성, 소켓의 주소체계, TCP 프로토콜 사용
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# HOST 주소, PORT 주소 연결
client_socket.connect((HOST, PORT))
# 데이터 전송
def handler_TX():
    while True:
        pass
# 데이터 수신
def handler_RX():
    while True:
        pass
# 데이터 전송 Thread

# 데이터 수신 Thread

# 전송 Thread 시작

# 수신 Thread 시작


# 쓰레드가 좋료되기 전에 프로그램이 종료되지 않도록 보장장
# 전송 Thread 대기

# 수신 Thread 대기기