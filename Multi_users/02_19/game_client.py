import socket
import pygame
import threading

# 클라이언트 설정
SERVER_IP = "210.101.236.198"
PORT = 4561

# Pygame 설정
pygame.init()
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# UDP 소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 화면 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("네트워크 탁구 게임")
clock = pygame.time.Clock()

# 초기 값
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
player1_x = WIDTH // 2 - PADDLE_WIDTH // 2
player2_x = WIDTH // 2 - PADDLE_WIDTH // 2
player_role = None  # P1인지 P2인지 서버에서 전달받음
score_p1, score_p2 = 0, 0  # 점수 저장

def receive_data(client_socket):
    global ball_x, ball_y, player1_x, player2_x, score_p1, score_p2, player_role
    
    BUFFER_SIZE = 1024

    while True:
        try:
            if client_socket.fileno() == -1:  # 소켓이 닫혔는지 확인
                print("⚠️ 클라이언트 소켓이 닫혔습니다. 데이터 수신을 중단합니다.")
                break
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            game_state = data.decode().split(",")

            if len(game_state) == 1:  # 처음 연결 시 P1 또는 P2 역할을 받음
                player_role = game_state[0]
                print(f"🎮 역할 할당됨: {player_role}")
                continue

            print(game_state)
            ball_x, ball_y = int(game_state[0]), int(game_state[1])
            player1_x, player2_x = int(game_state[2]), int(game_state[3])
            score_p1, score_p2 = int(game_state[4]), int(game_state[5])
        
        except BlockingIOError:
            continue
        except OSError as e:
            print(f"❌ 데이터 수신 오류: {e}")
            break  # 오류 발생 시 스레드 종료

# 서버에 연결 시작
client_socket.sendto("hello".encode('utf-8'), (SERVER_IP, PORT))

# 수신 스레드 시작
threading.Thread(target=receive_data, daemon=True, args=(client_socket,)).start()

running = True
while running:
    screen.fill(BLACK)

    # 이벤트 처리 (창 닫기)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 🎯 연속적인 키 입력 처리 (키가 계속 눌려있으면 지속 실행)
    keys = pygame.key.get_pressed()
    if player_role == "P1":  # 플레이어 1이면
        if keys[pygame.K_LEFT]:
            client_socket.sendto("LEFT_P1".encode(), (SERVER_IP, PORT))
        if keys[pygame.K_RIGHT]:
            client_socket.sendto("RIGHT_P1".encode(), (SERVER_IP, PORT))
    elif player_role == "P2":  # 플레이어 2이면
        if keys[pygame.K_LEFT]:
            client_socket.sendto("LEFT_P2".encode(), (SERVER_IP, PORT))
        if keys[pygame.K_RIGHT]:
            client_socket.sendto("RIGHT_P2".encode(), (SERVER_IP, PORT))

    # 🎾 공과 패들 그리기
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)  # 공
    pygame.draw.rect(screen, RED, (player1_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))  # P1 패들
    pygame.draw.rect(screen, RED, (player2_x, 0, PADDLE_WIDTH, PADDLE_HEIGHT))  # P2 패들 (위쪽)

    # 점수 표시
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"P1: {score_p1}  P2: {score_p2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 50, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
client_socket.close()
