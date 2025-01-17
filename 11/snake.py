import random
import pygame  # 파이게임 모듈 임포트하기
from datetime import datetime
from datetime import timedelta

# 여러 가지 색
RED = 255, 0, 0  # 적색:   적 255, 녹   0, 청   0
GREEN = 0, 255, 0  # 녹색:   적   0, 녹 255, 청   0
BLUE = 0, 0, 255  # 청색:   적   0, 녹   0, 청 255
PURPLE = 127, 0, 127  # 보라색: 적 127, 녹   0, 청 127
BLACK = 0, 0, 0  # 검은색: 적   0, 녹   0, 청   0
GRAY = 127, 127, 127  # 회색:   적 127, 녹 127, 청 127
WHITE = 255, 255, 255  # 하얀색: 적 255, 녹 255, 청 255

# 블록을 그리는 함수 정의하기
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 440
BLOCK_SIZE = 20

# 뱀 게임에서 사용할 데이터 모델 정의하기


class Snake:
    """뱀 클래스"""
    color = GREEN  # 뱀의 색

    def __init__(self):
        self.positions = [(9, 6), (9, 7), (9, 8), (9, 9)]  # 뱀의 위치
        self.direction = 'north'  # 뱀의 방향

    def draw(self, screen):
        """뱀을 화면에 그린다."""
        for position in self.positions:  # 뱀의 몸 블록들을 순회하며
            draw_block(screen, self.color, position)  # 각 블록을 그린다

    def crawl(self):
        """뱀이 현재 방향으로 한 칸 기어간다."""
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'north':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'south':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'west':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'east':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def turn(self, direction):
        """뱀의 방향을 바꾼다."""
        if (self.direction == 'north') and (direction == 'south'):
            pass
        elif (self.direction == 'south') and (direction == 'north'):
            pass
        elif (self.direction == 'west') and (direction == 'east'):
            pass
        elif (self.direction == 'east') and (direction == 'west'):
            pass
        else:
            self.direction = direction

    def grow(self):
        """뱀이 한 칸 자라나게 한다."""
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'north':
            self.positions.append((y - 1, x))
        elif self.direction == 'south':
            self.positions.append((y + 1, x))
        elif self.direction == 'west':
            self.positions.append((y, x - 1))
        elif self.direction == 'east':
            self.positions.append((y, x + 1))


class Apple:
    """사과 클래스"""
    color = RED  # 사과의 색

    def __init__(self, position=(random.randint(2, 21), random.randint(0, 19))):
        self.position = position  # 사과의 위치

    def draw(self, screen):
        """사과를 화면에 그린다."""
        draw_block(screen, self.color, self.position)


class PoisonApple(Apple):
    """독사과 클래스"""
    color = BLUE             # 독사과의 색
    num_of_poison_apple = 0  # 독사과의 개수
    positions = []           # 독사과의 위치들

    def __init__(self, point):
        self.positions = []
        self.num_of_poison_apple = point
        for i in range(self.num_of_poison_apple):
            self.positions.append((random.randint(2, 21), random.randint(0, 19)))  # 독사과의 위치들

    def add_poison_apple(self, screen):
        """독사과들을 화면에 그린다."""
        for position in self.positions:               # 독사과들을 순회하며
            draw_block(screen, self.color, position)  # 각 블록을 그린다

class GameBoard:
    """게임판 클래스"""
    width = 20                     # 게임판의 너비
    height = 20                    # 게임판의 높이
    speed = 0.3                    # 게임의 속도 (second)
    point = 0                      # 사과를 먹은 개수
    poison_point = 0               # 독사과를 먹은 개수
    poison_apple_on = False

    def __init__(self):
        self.snake = Snake()                            # 게임판 위의 뱀
        self.apple = Apple()                            # 게임판 위의 사과
        self.poison_apple = PoisonApple(self.point)     # 게임판 위의 독사과
        self.speed = 0.3                                # 게임의 속도 (second)
        self.point = 0                                  # 사과를 먹은 개수

    def draw(self, screen):
        """화면에 게임판의 구성요소를 그린다."""
        self.apple.draw(screen)                         # 게임판 위의 사과를 그린다
        self.snake.draw(screen)                         # 게임판 위의 뱀을 그린다
        self.poison_apple.add_poison_apple(screen)      # 게임판 위의 독사과를 그린다

    def put_new_apple(self):
        """게임판에 새 사과를 놓는다."""
        self.apple = Apple((random.randint(2, 21), random.randint(0, 19)))
        for position in self.snake.positions:    # 뱀 블록을 순회하면서
            if self.apple.position == position:  # 사과가 뱀 위치에 놓인 경우를 확인해
                self.put_new_apple()             # 사과를 새로 놓는다
                break

    def put_new_poison_apple(self):
        """게임판에 새 독사과를 놓는다."""
        self.poison_apple = PoisonApple(self.point)
        for position in self.snake.positions:            # 뱀 블록을 순회하면서
            if self.poison_apple.positions == position:  # 독사과가 뱀 위치에 놓인 경우를 확인해
                self.put_new_poison_apple()              # 독사과를 새로 놓는다
                break

    def update_point(self):
        """점수를 증가시킨다."""
        self.point = self.point + 1                # 점수를 올린다

    def down_point(self):
        """점수를 감소시킨다."""
        self.point = self.point - 1                # 점수를 낮춘다
        self.poison_point = self.poison_point + 1  # 점수를 올린다

    def update_speed(self):
        """속도를 증가시킨다."""
        if self.speed > 0.1:
            self.speed = self.speed - 0.05  # 속도를 올린다

    def process_turn(self):
        """게임을 한 차례 진행한다."""
        self.snake.crawl()

        # 뱀의 머리와 사과가 닿았으면
        if self.snake.positions[0] == self.apple.position:
            self.snake.grow()                   # 뱀을 한 칸 자라게 한다
            self.put_new_apple()                # 사과를 새로 놓는다
            self.update_point()                 # 점수를 올린다

            if self.point % 3.0 == 0.0:         # 점수가 3점 증가한 시점이라면
                self.update_speed()             # 속도를 올린다

            self.poison_apple = PoisonApple(self.point)

        # 뱀의 머리와 독사과가 닿았으면
        if self.snake.positions[0] in self.poison_apple.positions:
            self.put_new_poison_apple()         # 독사과를 새로 놓는다
            self.down_point()                   # 점수를 낮춘다

        # 뱀이 독사과를 3개 먹었다면
        if self.poison_point == 3:
            raise SnakeDeathException()  # 뱀 사망 예외를 일으킨다

        # 뱀의 머리가 뱀의 몸과 부딛혔으면
        if self.snake.positions[0] in self.snake.positions[1:]:
            raise SnakeCollisionException()  # 뱀 충돌 예외를 일으킨다

        if self.snake.positions[0] == self.apple.position:
            self.snake.grow()
            self.put_new_apple()

        # 뱀의 머리가 게임판 밖으로 나갔다면
        if self.snake.positions[0][0] > self.height + 2 or self.snake.positions[0][0] < 2:
            raise SnakeOutException()  # 뱀 게임판 벗어남 예외를 일으킨다
        if self.snake.positions[0][1] > self.width or self.snake.positions[0][1] < 0:
            raise SnakeOutException()  # 뱀 게임판 벗어남 예외를 일으킨다


class SnakeCollisionException(Exception):
    """뱀 충돌 예외"""
    pass


class SnakeOutException(Exception):
    """뱀 게임판 벗어남 예외"""
    pass


class SnakeDeathException(Exception):
    """뱀 사망 예외"""
    pass


def draw_background(screen):
    """게임의 배경을 그린다."""
    background = pygame.Rect((0, 40), (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, background)


def draw_block(screen, color, position):
    """position 위치에 color 색깔의 블록을 그린다."""
    block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE),
                        (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, block)


def update_points(field, point):
    font = pygame.font.Font(None, 30)
    input_box = pygame.Rect((0, 0), (SCREEN_WIDTH, 40))
    pygame.draw.rect(field, BLACK, input_box)
    txt_surface = font.render("Points : " + str(point), True, pygame.Color('lightskyblue3'))
    field.blit(txt_surface, (input_box.x + 10, input_box.y + 10))


def play_again():
    text = bigfont.render('Play again?', 13, (0, 0, 0))
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(screen, (255, 255, 255), ((textx - 5, texty - 5),
                                               (textx_size + 10, texty_size +
                                                10)))

    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                       SCREEN_HEIGHT / 2 - text.get_height() / 2))

    clock = pygame.time.Clock()
    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx - 5 and x <= textx + textx_size + 5:
                    if y >= texty - 5 and y <= texty + texty_size + 5:
                        in_main_menu = False
                        break

    return True


pygame.init()

# 지정한 크기의 게임 화면 창을 연다.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

draw_background(screen)
draw_block(screen, GREEN, (12, 10))
draw_block(screen, GREEN, (12, 11))
draw_block(screen, GREEN, (12, 12))
draw_block(screen, GREEN, (12, 13))
pygame.display.update()

block_position = [0, 0]  # 블록의 위치 (y, x)
last_moved_time = datetime.now()  # 마지막으로 블록을 움직인 때

# font 정의
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)

# 종료 이벤트가 발생할 때까지 게임을 계속 진행한다
# 방향키 입력에 따라 바꿀 블록의 방향
DIRECTION_ON_KEY = {
    pygame.K_UP: 'north',
    pygame.K_DOWN: 'south',
    pygame.K_LEFT: 'west',
    pygame.K_RIGHT: 'east',
}
block_direction = 'east'  # 블록의 방향
block_position = [0, 0]
last_turn_time = datetime.now()

game_board = GameBoard()  # 게임판 인스턴스를 생성한다

while True:
    TURN_INTERVAL = timedelta(seconds=game_board.speed)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:  # 화살표 키가 입력되면 뱀의 방향을 바꾼다
            if event.key in DIRECTION_ON_KEY:
                game_board.snake.turn(DIRECTION_ON_KEY[event.key])

    # 시간이 TURN_INTERVAL만큼 지날 때마다 게임을 한 차례씩 진행한다
    if TURN_INTERVAL < datetime.now() - last_turn_time:
        try:
            update_points(screen, game_board.point)
            game_board.process_turn()
        except SnakeCollisionException:
            if play_again():
                game_board = GameBoard()
        except SnakeOutException:
            if play_again():
                game_board = GameBoard()
        except SnakeDeathException:
            if play_again():
                game_board = GameBoard()
        last_turn_time = datetime.now()

    draw_background(screen)
    game_board.draw(screen)
    pygame.display.update()