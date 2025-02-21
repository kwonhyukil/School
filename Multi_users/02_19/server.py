import socket
import threading
import time
import random

# 서버 설정
SERVER_IP = "210.101.236.203"
PORT = 3572
BUFFER_SIZE = 1024
TICK_RATE = 1/60  # 60FPS

# 게임 설정
WIDTH, HEIGHT = 800, 600
BALL_SPEED = [5, 5]
PADDLE_SPEED = 8
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10

# 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))

print(f"🎮 UDP 네트워크 탁구 서버 실행 중... {SERVER_IP}:{PORT}")

# 게임 상태
clients = {}
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = BALL_SPEED
player1_x, player2_x = WIDTH // 2 - PADDLE_WIDTH // 2, WIDTH // 2 - PADDLE_WIDTH // 2

# 점수
score_p1, score_p2 = 0, 0

def reset_ball():
    """공을 중앙으로 리셋하고 속도를 랜덤 방향으로 설정"""
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = random.choice([(5, 5), (-5, 5), (5, -5), (-5, -5)])  # 무작위 방향 설정
    time.sleep(3)  # 3초 대기 후 재시작

def game_loop():
    global ball_x, ball_y, ball_dx, ball_dy, player1_x, player2_x, score_p1, score_p2

    while True:
        time.sleep(TICK_RATE)

        # 공 이동
        ball_x += ball_dx
        ball_y += ball_dy

        # 벽 충돌 (좌우)
        if ball_x <= 0 or ball_x >= WIDTH:
            ball_dx *= -1

        # 공이 위아래 경계를 벗어나면 점수 반영 후 리셋
        if ball_y < 0:  # P1 득점
            score_p1 += 1
            print(f"🎉 P1 득점! 현재 점수: P1 {score_p1} - P2 {score_p2}")
            reset_ball()
        elif ball_y > HEIGHT:  # P2 득점
            score_p2 += 1
            print(f"🎉 P2 득점! 현재 점수: P1 {score_p1} - P2 {score_p2}")
            reset_ball()

        # 패들과 충돌 (공이 패들에 닿았을 때 반사)
        if (ball_y >= HEIGHT - PADDLE_HEIGHT - 10 and player1_x < ball_x < player1_x + PADDLE_WIDTH):
            ball_dy *= -1  # 공 방향 반전

        if (ball_y <= PADDLE_HEIGHT + 10 and player2_x < ball_x < player2_x + PADDLE_WIDTH):
            ball_dy *= -1  # 공 방향 반전

        # 클라이언트에게 게임 상태 전송
        game_state = f"{ball_x},{ball_y},{player1_x},{player2_x},{score_p1},{score_p2}"
        for addr in clients.keys():
            server_socket.sendto(game_state.encode(), addr)

def handle_clients():
    global player1_x, player2_x
    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        
        # 새로운 클라이언트 연결 (P1, P2 배정)
        if addr not in clients:
            if len(clients) == 0:
                clients[addr] = "P1"
                server_socket.sendto("P1".encode(), addr)
                print(f"🎮 클라이언트 {addr} 연결됨 - 역할: P1")
            elif len(clients) == 1:
                clients[addr] = "P2"
                server_socket.sendto("P2".encode(), addr)
                print(f"🎮 클라이언트 {addr} 연결됨 - 역할: P2")
            else:
                print(f"❌ 클라이언트 {addr} 접속 거부 - 사용자 초과")
                server_socket.sendto("FULL".encode(), addr)
                continue

        # 클라이언트 입력 처리
        command = data.decode().strip()
        if command == "LEFT_P1":
            player1_x = max(0, player1_x - PADDLE_SPEED)
        elif command == "RIGHT_P1":
            player1_x = min(WIDTH - PADDLE_WIDTH, player1_x + PADDLE_SPEED)
        elif command == "LEFT_P2":
            player2_x = max(0, player2_x - PADDLE_SPEED)
        elif command == "RIGHT_P2":
            player2_x = min(WIDTH - PADDLE_WIDTH, player2_x + PADDLE_SPEED)

# 스레드 실행
threading.Thread(target=game_loop, daemon=True).start()
threading.Thread(target=handle_clients, daemon=True).start()

while True:
    time.sleep(1)  # 메인 스레드를 유지하기 위한 코드
