import pygame
import sys
import random
import time

# 초기화
pygame.init()

# 화면 설정
screen_width = 3000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout Game')

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# 폰트 설정
font_large = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 24)

# 공 설정
ball_radius = 8
ball_speed = 4
ball_color = WHITE
ball_speed_multiplier = 1

# 패들 설정
paddle_width = 3000
paddle_height = 15
paddle_speed = 6

# 벽돌 설정
brick_width = 30
brick_height = 10
brick_gap = 5
space_above_paddle = 150

# 게임 상태 변수
items = []  # 아이템 리스트 추가
game_over = False
game_success = False

# 공 리스트
balls = []

class Item:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.color = YELLOW
        self.speed_y = 2

    def move(self):
        self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def generate_random_bricks():
    global bricks
    bricks = []
    num_bricks = random.randint(3000, 3200 )
    rows = (screen_height - space_above_paddle) // (brick_height + brick_gap)
    cols = screen_width // (brick_width + brick_gap)
    placed_bricks = 0
    while placed_bricks < num_bricks:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        brick_rect = pygame.Rect(col * (brick_width + brick_gap) + 15, row * (brick_height + brick_gap) + 15, brick_width, brick_height)
        if brick_rect.bottom <= screen_height - (paddle_height + 10):
            if not any(brick.colliderect(brick_rect) for brick in bricks):
                bricks.append(brick_rect)
                placed_bricks += 1

def reset_game():
    global paddle_x, balls, items
    paddle_x = (screen_width - paddle_width) // 2
    generate_random_bricks()
    items = []  # 아이템 초기화
    balls = [{'x': screen_width // 2, 'y': screen_height - 30, 'speed_x': ball_speed * random.choice((1, -1)), 'speed_y': -ball_speed, 'radius': ball_radius}]

def split_ball():
    """ 공을 2배로 늘리는 기능 """
    new_balls = []
    for ball in balls:
        new_balls.append({'x': ball['x'], 'y': ball['y'], 'speed_x': ball['speed_x'], 'speed_y': ball['speed_y'], 'radius': ball_radius})
        new_balls.append({'x': ball['x'], 'y': ball['y'], 'speed_x': -ball['speed_x'], 'speed_y': -ball['speed_y'], 'radius': ball_radius})
    return new_balls

reset_game()

# 메인 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if game_over or game_success:
                    reset_game()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed
    
    if not game_over and not game_success:
        for ball in balls:
            ball['x'] += ball['speed_x'] * ball_speed_multiplier
            ball['y'] += ball['speed_y'] * ball_speed_multiplier
            if ball['x'] - ball['radius'] <= 0 or ball['x'] + ball['radius'] >= screen_width:
                ball['speed_x'] = -ball['speed_x']
            if ball['y'] - ball['radius'] <= 0:
                ball['speed_y'] = -ball['speed_y']
            
            paddle_rect = pygame.Rect(paddle_x, screen_height - paddle_height - 10, paddle_width, paddle_height)
            if paddle_rect.collidepoint(ball['x'], ball['y'] + ball['radius']):
                ball['speed_y'] = -ball['speed_y']
            
            for brick in bricks:
                if brick.collidepoint(ball['x'], ball['y']):
                    ball['speed_y'] = -ball['speed_y']
                    bricks.remove(brick)
                    if random.random() < 0.01:  # 20% 확률로 아이템 생성
                        items.append(Item(brick.x, brick.y))
        
        for item in items[:]:
            item.move()
            if paddle_rect.colliderect(item.rect):
                items.remove(item)
                balls.extend(split_ball())

        if len(bricks) == 0:
            game_success = True
        if all(ball['y'] > screen_height for ball in balls):
            game_over = True
    
    screen.fill(BLACK)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)
    for ball in balls:
        pygame.draw.circle(screen, ball_color, (int(ball['x']), int(ball['y'])), ball['radius'])
    pygame.draw.rect(screen, BLUE, (paddle_x, screen_height - paddle_height - 10, paddle_width, paddle_height))
    for item in items:
        item.draw()
    
    if game_over:
        screen.blit(font_large.render('Game Over', True, WHITE), (screen_width // 2 - 60, screen_height // 2))
    elif game_success:
        screen.blit(font_large.render('Success', True, WHITE), (screen_width // 2 - 60, screen_height // 2))
    
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
