import pygame
import random
import time

blank = 7
shape = [
    [
        [(0, -1), (0, 1), (0, 2)], # ----
        [(-1, 0), (1, 0), (2, 0)],
        [(0, -1), (0, 1), (0, 2)],
        [(-1, 0), (1, 0), (2, 0)],
    ],
    [
        [(0, -1), (-1, -1), (0, 1)],
        [(-1, 0), (-1, 1), (1, 0)],
        [(0, -1), (0, 1), (1, 1)],
        [(1, 0), (1, -1), (-1, 0)]
    ],
    [
        [(0, -1), (0, 1), (-1, 1)],
        [(-1, 0), (1, 0), (1, 1)],
        [(0, -1), (1, -1), (0, 1)],
        [(-1,-1), (-1, 0), (1, 0)]
    ],
    [
        [(0, 1), (1, 0), (1,1)],
        [(0, 1), (1, 0), (1,1)],
        [(0, 1), (1, 0), (1,1)],
        [(0, 1), (1, 0), (1,1)]
    ],
    [
        [(0, -1), (-1, 0), (-1, 1)],
        [(-1, 0), (0, 1), (1, 1)],
        [(0, 1), (1, 0), (1, -1)],
        [(0, -1), (-1, -1), (1, 0)]
    ],
    [
        [(0, -1), (0, 1), (-1, 0)],
        [(-1, 0), (1, 0), (0, 1)],
        [(0, 1), (1, 0), (0, -1)],
        [(0, -1), (-1, 0), (1, 0)]
    ],
    [
        [(-1, -1), (-1, 0), (0, 1)],
        [(1, 0), (0, 1), (-1, 1)],
        [(0, -1), (1, 0), (1, 1)],
        [(-1, 0), (0, -1), (1, -1)]
    ]
]
start_x = 4
start_y = 1

class Tetromino:
    def __init__(self):
        self.x = start_x
        self.y = start_y
        self.rotation = 0
        self.piece_num = random.randint(0, 6)
        self.left = 2000
        self.right = -2000
        self.up = 2000
        self.down = -2000

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def get_shape(self):
        return 0

class Tetris:
    def __init__(self, num):
        self.font = pygame.font.Font(None, 36)
        self.key_states = {
            'left': False,
            'right': False,
            'down': False
        }
        self.running = True
        self.board = [[blank for i in range(10)] for j in range(20)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.line = 0
        self.colors = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 0), (152, 0, 203), (255, 0, 0), (255, 255, 255)]
        self.block_size = 40
        self.next_board = [[blank for i in range(5)] for j in range(5)]
        self.next_board_start = (num * self.block_size * 10) + self.block_size
        self.score_x = self.next_board_start
        self.score_y = self.block_size
        self.fps = 20

    def erase_cur(self):
        # 현재 칸 지우기
        self.board[self.current_piece.y][self.current_piece.x] = blank
        for (dy, dx) in shape[self.current_piece.piece_num][self.current_piece.rotation]:
            next_y = self.current_piece.y + dy
            next_x = self.current_piece.x + dx
            self.board[next_y][next_x] = blank
    
    def erase_next_board(self):
        self.next_board = [[blank for i in range(5)] for j in range(5)]

    def update_board(self):
        # 다시 그리기
        self.board[self.current_piece.y][self.current_piece.x] = self.current_piece.piece_num
        for (dy, dx) in shape[self.current_piece.piece_num][self.current_piece.rotation]:
            next_y = self.current_piece.y + dy
            next_x = self.current_piece.x + dx
            self.board[next_y][next_x] = self.current_piece.piece_num
    
    def update_next_board(self):
        self.erase_next_board()
        center = 2
        self.next_board[center][center] = self.next_piece.piece_num
        for (dy, dx) in shape[self.next_piece.piece_num][self.next_piece.rotation]:
            next_y = center + dy
            next_x = center + dx
            self.next_board[next_y][next_x] = self.next_piece.piece_num

    def check(self, command):
        if command == 'U':
            for (dy,dx) in shape[self.current_piece.piece_num][(self.current_piece.rotation + 1) % 4]:
                next_y = self.current_piece.y + dy
                next_x = self.current_piece.x + dx
                if next_x < 0 or next_x > 9 or next_y < 0 or next_y >19:
                    return False
                elif self.board[next_y][next_x] != blank and self.board[next_y][next_x] != self.current_piece.piece_num:
                    return False
                else: continue
            return True
        for (dy, dx) in shape[self.current_piece.piece_num][self.current_piece.rotation]:
            cur_y = self.current_piece.y
            cur_x = self.current_piece.x
            next_y = cur_y + dy
            next_x = cur_x + dx
            if command == 'L':
                if next_x <= 0 or cur_x <= 0:
                    return False
                elif self.board[cur_y][cur_x-1] != blank \
                    and self.board[cur_y][cur_x-1] != self.current_piece.piece_num:
                    return False
                elif self.board[next_y][next_x-1] != blank \
                    and self.board[next_y][next_x-1] != self.current_piece.piece_num:
                    return False
                else: continue
            elif command == 'R':
                if next_x >= 9 or cur_x >= 9:
                    return False
                elif self.board[cur_y][cur_x+1] != blank \
                    and self.board[cur_y][cur_x+1] != self.current_piece.piece_num:
                    return False
                elif self.board[next_y][next_x+1] != blank \
                    and self.board[next_y][next_x+1] != self.current_piece.piece_num:
                    return False
                else: continue
            elif command == 'D':
                if next_y >= 19 or cur_y >= 19:
                    return False
                elif self.board[cur_y+1][cur_x] != blank \
                    and self.board[cur_y+1][cur_x] != self.current_piece.piece_num:
                    return False
                elif self.board[next_y+1][next_x] != blank \
                    and self.board[next_y+1][next_x] != self.current_piece.piece_num:
                    return False
                else: continue
        return True

    def freeze(self):
        self.board[self.current_piece.y][self.current_piece.x] = self.current_piece.piece_num + 8
        for (dy, dx) in shape[self.current_piece.piece_num][self.current_piece.rotation]:
            next_y = self.current_piece.y + dy
            next_x = self.current_piece.x + dx
            self.board[next_y][next_x] = self.current_piece.piece_num + 8
    
    def check_end(self):
        if self.current_piece.y == start_y or self.current_piece == start_x:
            self.running = False
        
    def print_board(self):
        for i in range(20):
            stringng = ""
            for j in range(10):
                stringng += str(self.board[i][j])
            print(stringng)

    def rotate(self):
        if self.check('U'):
            self.erase_cur()
            self.current_piece.rotate()

    def down(self):
        if self.check('D'):
            self.erase_cur()
            self.current_piece.y += 1
            self.current_piece.y = min(19, self.current_piece.y)
        else:
            self.freeze()
            self.check_end()
            self.check_line()
            self.current_piece = self.next_piece
            self.next_piece = Tetromino()

    def check_line(self):
        cleared_lines = []
        for y in range(20):
            cnt = 0
            for x in range(10):
                if self.board[y][x] != blank:
                    cnt += 1
            if cnt == 10:
                cleared_lines.append(y)
        
        if cleared_lines:
            # print(f"{cleared_lines[0]}부터 {len(cleared_lines)}줄을 삭제해야 합니다.")
            self.line += len(cleared_lines)
            self.clear_line(cleared_lines)

    def clear_line(self, cleared_lines):
        for y in cleared_lines:
            del self.board[y]
            self.board.insert(0, [blank for _ in range(10)])

    def left(self):
        if self.check('L'):
            self.erase_cur()
            self.current_piece.x -= 1
            self.current_piece.x = max(0, self.current_piece.x)

    def right(self):
        if self.check('R'):
            self.erase_cur()
            self.current_piece.x += 1
            self.current_piece.x = min(9, self.current_piece.x)

    def draw_score(self):
        # 이전 점수 텍스트를 지우기 위해 점수 영역을 검정색으로 채움
        pygame.draw.rect(screen, (0, 0, 0), (self.score_x, self.score_y, 200, 50))
        text = self.font.render("Score: " + str(self.line), True, (255, 255, 255))
        screen.blit(text, (self.score_x, self.score_y))
    
    def drop(self):
        while self.check('D'):
            self.down()
        self.down()
    
    def draw_board(self):
        for i in range(20):
            for j in range(10):
                pygame.draw.rect(screen, self.colors[self.board[i][j] % 8], (j*self.block_size + 1, i*self.block_size + 1, self.block_size-2, self.block_size-2))

    def draw_next_board(self):
        for i in range(5):
            for j in range(5):
                pygame.draw.rect(
                    screen, 
                    self.colors[self.next_board[i][j] % 8], 
                    (
                        self.next_board_start + j*self.block_size + 1, 
                        self.next_board_start + i*self.block_size + 1, 
                        self.block_size-2, 
                        self.block_size-2
                    )
                )

    def main(self):
        timer = 0
        flag = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.key_states['left'] = True
                    elif event.key == pygame.K_RIGHT:
                        self.key_states['right'] = True
                    elif event.key == pygame.K_DOWN:
                        self.key_states['down'] = True
                    elif event.key == pygame.K_SPACE:
                        self.drop()
                    elif event.key == pygame.K_UP:
                        self.rotate()
                    elif event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_p:
                        flag = not flag
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.key_states['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        self.key_states['right'] = False
                    elif event.key == pygame.K_DOWN:
                        self.key_states['down'] = False

            # 방향키 상태에 따라 함수 호출
            if self.key_states['left']:
                self.left()
            elif self.key_states['right']:
                self.right()
            elif self.key_states['down']:
                self.down()

            self.update_board()
            self.update_next_board()
            self.draw_board()
            self.draw_next_board()
            pygame.display.flip()
            self.draw_score()
            # pygame.display.update()
            clock.tick(self.fps)

            timer += clock.get_time()
            if timer > 1000 and not flag:
                self.down()
                timer = 0

        print("Game over!")
        print("Your score is", self.line)      

if __name__ == "__main__":
    pygame.init()
    size = (width, height) = (1200, 800)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    game = Tetris(1)
    game.main()
    pygame.quit()