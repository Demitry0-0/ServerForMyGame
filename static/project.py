import pygame
import os
import sys
from random import randint
import random
import time
import sqlite3
import map
from requests import post, get, put

ip = 'http://127.0.0.1:5000'
name_ip = input('Введите адресную строку или просто нажмите Enter.\nПример http://04991447.ngrok.io \n')
f_f_f = True
if name_ip:
    ip = name_ip
FPS = 60
size = WIDTH, HEIGHT = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
up, down, left, right = ([119, 275], [115, 273], [97, 274], [100, 276])
clock = pygame.time.Clock()
name = 'map\\map1.html'
pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey == 2:
        image = pygame.image.load(fullname).convert()
    return image


class Button:
    def __init__(self):
        self.word = ["играть", "загрузить карту", "рекорды", "выйти"]
        self.flag = True
        self.draw()

    def draw(self):
        font = pygame.font.Font(None, 30)
        play = font.render(self.word[0], 1, (100, 255, 100))
        self.play = font.size(self.word[0])
        new_map = font.render(self.word[1], 1, (100, 255, 100))
        self.new_map = font.size(self.word[1])
        records = font.render(self.word[2], 1, (100, 255, 100))
        self.records = font.size(self.word[2])
        bye = font.render(self.word[3], 1, (100, 255, 100))
        self.bye = font.size(self.word[3])
        screen.blit(play, (30, 300))
        screen.blit(new_map, (30, 340))
        screen.blit(records, (30, 380))
        screen.blit(bye, (30, 420))

    def chunks(self, lst, chunk_size):
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    def map(self):
        self.flag = False
        screen.fill((0, 0, 0))
        path = r'map'
        files = os.listdir(path)
        font = pygame.font.Font(None, 30)
        lst = self.chunks(files, 20)
        i = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    p = event.pos
                    if 10 <= p[0] <= font.size('назад')[0] + 10 and 30 <= p[1] <= font.size('назад')[1] + 30:
                        if i:
                            i -= 1
                        else:
                            self.flag = True
                            screen.fill((0, 0, 0)), screen.blit(FON, (0, 0))
                            return
                    elif 920 <= p[0] <= font.size('далее')[0] + 920 and 30 <= p[1] <= font.size('далее')[1] + 30:
                        if i + 1 < len(lst):
                            i += 1
                    for _ in range(len(lst[i])):
                        if 400 <= p[0] <= font.size(lst[i][_])[0] + 400 and \
                                30 * _ + 30 <= p[1] <= font.size(lst[i][_])[1] + 30 + 30 * _:
                            global name
                            name, self.flag = 'map\\' + lst[i][_], True
                            screen.fill((0, 0, 0)), screen.blit(FON, (0, 0))
                            return
            self.render(lst[i])
            screen.blit(font.render('назад', 1, (255, 255, 255)), (10, 30))
            screen.blit(font.render('далее', 1, (255, 255, 255)), (920, 30))
            pygame.display.flip()

    def render(self, lst):
        screen.fill((0, 0, 0))
        for i in range(len(lst)):
            font = pygame.font.Font(None, 30)
            screen.blit(font.render(lst[i], 1, (255, 255, 255)), (400, 30 * i + 30))

    def update(self, pos, flag=False):
        font = pygame.font.Font(None, 30)
        x, y = pos
        if 20 <= x <= 30 + self.play[0] + 10 and 300 <= y <= 300 + self.play[1] and self.flag:
            screen.blit(font.render(self.word[0], 1, (0, 0, 0)), (30, 300))
            if flag:
                return True
        elif 20 <= x <= 30 + self.new_map[0] + 10 and 340 <= y <= 340 + self.new_map[1] and self.flag:
            screen.blit(font.render(self.word[1], 1, (0, 0, 0)), (30, 340))
            if flag:
                self.map()
        elif 20 <= x <= 30 + self.records[0] + 10 and 380 <= y <= 380 + self.records[1] and self.flag:
            screen.blit(font.render(self.word[2], 1, (0, 0, 0)), (30, 380))
            if flag:
                self.score()
        elif 20 <= x <= 30 + self.bye[0] + 10 and 420 <= y <= 420 + self.bye[1] and self.flag:
            screen.blit(font.render(self.word[3], 1, (0, 0, 0)), (30, 420))
            if flag:
                terminate()
        elif self.flag:
            self.draw()

    def score(self):
        global name
        self.flag = False
        a = name[name.index('\\') + 1:]
        con = sqlite3.connect('data\\records.db')
        cur = con.cursor()
        result = cur.execute('''SELECT * from records where map="{}"'''.format(a)).fetchall()
        result = list(map(lambda x: x[1] + ' = ' + str(x[0]), sorted(result, key=lambda x: x[0])))[:10]
        self.render(result[::-1])
        font = pygame.font.Font(None, 30)
        screen.blit(font.render('назад', 1, (255, 255, 255)), (10, 30))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    p = event.pos
                    if 10 <= p[0] <= font.size('назад')[0] + 10 and 30 <= p[1] <= font.size('назад')[1] + 30:
                        self.flag = True
                        screen.fill((0, 0, 0)), screen.blit(FON, (0, 0))
                        return


class Anime(pygame.sprite.Sprite):
    kadrs = [load_image('packman_1.png'),
             load_image('packman_2.png'),
             load_image('packman_3.png'),
             load_image('packman_4.png')]

    def __init__(self, group, pos):
        super().__init__(group)
        self.index = 0
        self.angle = 0
        self.image = pygame.transform.rotate(Anime.kadrs[0], self.angle)
        self.cimage = self.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = 'down'

    def update(self):
        a = [0, 1, 2, 3, 2, 1]
        self.index += 1
        self.index %= 6
        self.cimage = Anime.kadrs[a[self.index]]
        self.rotate(self.dir)

    def resize(self, size):
        for i in range(len(Anime.kadrs)):
            Anime.kadrs[i] = pygame.transform.scale(Anime.kadrs[i], (size, size))

    def rotate(self, dir):
        if dir == 'up':
            self.angle = 90
        if dir == 'down':
            self.angle = -90
        if dir == 'left':
            self.angle = -180
        if dir == 'right':
            self.angle = 0
        self.image = pygame.transform.rotate(self.cimage, self.angle)


class Player:
    def __init__(self, screen, anime, board, pos):
        self.anime = anime
        self.screen = screen
        self.board = board
        self.x, self.y = pos
        self.dir = 'down'
        self.new_dir = '_'
        self.speed = 0.7
        self.board_pos = self.get_board_pos()
        self.spos = self.board_pos

    def reverse_dir(self):
        if self.dir == 'up':
            return 'down'
        if self.dir == 'down':
            return 'up'
        if self.dir == 'left':
            return 'right'
        if self.dir == 'right':
            return 'left'

    def set_dir(self, dir):
        self.new_dir = dir

    def check_change(self):
        if self.board_pos != self.get_board_pos():
            self.board_pos = self.get_board_pos()
            self.x, self.y = self.get_board_pos(5, 5)[0] * self.board.cell_size + self.board.left, \
                             self.get_board_pos(5, 5)[1] * self.board.cell_size + self.board.top
            self.spos = self.get_board_pos(5, 5)
            if self.board.board[self.spos[0]][self.spos[1]].collectable:
                self.board.board[self.spos[0]][self.spos[1]].collected = True
            return True
        return False

    def get_board_pos(self, offsetx=0, offsety=0):
        return self.board.get_cell((self.x + offsetx, self.y + offsety))

    def get_possibles(self):
        a = []
        if self.board.wall_map[self.spos[1] + 1][self.spos[0]] == 0:
            a.append('down')
        if self.board.wall_map[self.spos[1] - 1][self.spos[0]] == 0:
            a.append('up')
        if self.board.wall_map[self.spos[1]][self.spos[0] - 1] == 0:
            a.append('left')
        if self.board.wall_map[self.spos[1]][self.spos[0] + 1] == 0:
            a.append('right')
        return a  # ['up', 'down', 'right', 'left']

    def move(self, possibles):
        if self.check_change():
            possibles = self.get_possibles()
            if self.dir not in possibles:
                self.dir = random.choice(possibles)
                self.anime.rotate(self.dir)
            if self.new_dir in possibles:
                self.dir = self.new_dir
                self.anime.rotate(self.dir)
        self.anime.dir = self.dir
        if self.dir == 'up':
            self.y -= self.speed
        if self.dir == 'down':
            self.y += self.speed
        if self.dir == 'left':
            self.x -= self.speed
        if self.dir == 'right':
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(self.screen, (200, 200, 10), (self.x, self.y, self.board.cell_size, self.board.cell_size))


class Cell:
    def __init__(self, x, y, color="black"):
        self.x = x
        self.y = y
        self.check = None
        self.color = color
        self.collectable = True if color == "black" else False
        self.collected = False

    def change_color(self):
        if self.color == "white":
            self.color = "black"
        if self.color == "black":
            self.color = "white"

    def draw(self, *args):
        # args = (self.top + i * self.cell_size,
        # self.left + j * self.cell_size, self.cell_size,
        # self.cell_size)

        if self.color == "black" and self.collectable and self.collected:
            pygame.draw.rect(screen, (0, 0, 0), args)
            self.check = args[:2]
        elif self.color == "black" and self.collectable and not self.collected:
            # draw collectable sprite
            pygame.draw.rect(screen, (0, 0, 0), args)
            pygame.draw.circle(screen, (255, 255, 255), (args[0] + args[2] // 2, args[1] + args[2] // 2), args[2] // 6)
        elif self.color == "white" and not self.collectable:
            pygame.draw.rect(screen, (200, 200, 255), args)


class Board:
    # создание поля
    def __init__(self, width, height, wall_map=[[1, 1, 1, 1, 1],
                                                [1, 0, 0, 0, 1],
                                                [1, 0, 1, 0, 1],
                                                [1, 0, 0, 0, 1],
                                                [1, 0, 1, 0, 1],
                                                [1, 0, 0, 0, 1],
                                                [1, 1, 1, 1, 1]]):
        self.width = width
        self.count = 0
        self.height = height
        self.wall_map = wall_map
        self.board = []
        self.hero = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        self.check_points = {None}
        self.cells = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.fill_cells()
        self.create_cells()

    def create_cells(self):
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                if self.wall_map[j][i] == '0':
                    self.wall_map[j][i] = 0
                    self.board[i].append(Cell(i, j))
                elif self.wall_map[j][i] == '1':
                    self.wall_map[j][i] = 1
                    self.board[i].append(Cell(i, j, color='white'))
                elif self.wall_map[j][i] == '@':
                    self.hero[0] = (i * 30 + 30, j * 30 + 30)
                    self.wall_map[j][i] = 0
                    self.board[i].append(Cell(i, j))
                elif self.wall_map[j][i] == '#':
                    self.hero[1] = (i * 30 + 30, j * 30 + 30)
                    self.wall_map[j][i] = 0
                    self.board[i].append(Cell(i, j))
                elif self.wall_map[j][i] == '*':
                    self.hero[2] = (i * 30 + 30, j * 30 + 30)
                    self.wall_map[j][i] = 0
                    self.board[i].append(Cell(i, j))
                elif self.wall_map[j][i] == '$':
                    self.hero[3] = (i * 30 + 30, j * 30 + 30)
                    self.wall_map[j][i] = 0
                    self.board[i].append(Cell(i, j))

    def are_left(self):
        checked = True
        for rd in self.board:
            for cell in rd:
                if cell.collectable and not cell.collected:
                    checked = False
                    break
        return not checked

    def reset(self):
        for rd in self.board:
            for cell in rd:
                if cell.collectable:
                    cell.collected = False
                    time.sleep(0.1)
                    self.render()
                    pygame.display.flip()
                else:
                    time.sleep(0.1)
        self.count += len(self.check_points) - 1
        self.check_points.clear()

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.fill_cells()

    def render(self):
        for i in range(self.height - 1):
            for j in range(self.width - 1):
                self.board[i][j].draw(self.top + i * self.cell_size,
                                      self.left + j * self.cell_size, self.cell_size,
                                      self.cell_size)
                if not len(self.check_points):
                    self.board[i][j].check = None
                else:
                    self.check_points.add(self.board[i][j].check)
                if self.board[i][j].color == "white" and False:
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size))
                if self.board[i][j].color == "black" and False:
                    pygame.draw.rect(screen, (0, 0, 0), (
                        self.top + i * self.cell_size,
                        self.left + j * self.cell_size, self.cell_size,
                        self.cell_size))

    def fill_cells(self):
        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j] = [self.top + i * self.cell_size,
                                    self.left + j * self.cell_size,
                                    self.cell_size,
                                    self.cell_size]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def on_click(self, cell):
        return

    def load_map(self, file_adr):
        with open(file_adr, 'r') as f:
            _map = list(f.read().split('\n'))
            wall_map = [x.split() for x in _map]
            x = len(wall_map)
            y = len(wall_map[0])
        a = Board(x, y, wall_map)
        a.wall_map = wall_map
        return a

    def get_cell(self, pos):
        pos = int(pos[0] + 0), int(pos[1] + 0)
        i, j = -1, -1
        for cell_row in self.cells:
            i += 1
            if cell_row[0][0] <= pos[0] < cell_row[0][0] + self.cell_size:
                for cell in cell_row:
                    j += 1
                    if cell[1] <= pos[1] < cell[1] + self.cell_size:
                        return [i, j]
        return [-1, -1]

    def get_coords(self, ij):
        return (30 * ij[0] + 30, 30 * ij[1] + 30)

    def change_color(self, i):
        if self.board[i[0]][i[1]].color == "black":
            self.board[i[0]][i[1]].color = "white"
        elif self.board[i[0]][i[1]].color == "white":
            self.board[i[0]][i[1]].color = "black"

    def open_map(self, i):
        self.board[i[0]][i[1]].change_color()

    def get_color(self, i):
        return self.board[i[0]][i[1]].color


mersz = load_image('mersz.jpg')
bb = load_image('bomb.jpg')
leg_img = load_image('leg.png')
lob_img = load_image('lob.png', None)


class Tverdolobiy(pygame.sprite.Sprite):
    def __init__(self, group, pos, board, player):
        super().__init__(group)
        self.image = lob_img
        pos_x, pos_y = pos
        self.board = board
        self.player = player
        self.speed = 0.1
        self.chek_lst = []
        self.wall = []
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def payment(self, player, lob):
        n = 200
        if abs(player[0] - lob[0]) > n or abs(player[1] - lob[1]) > 150:
            return True
        return False

    def move(self):
        board, player = self.board, self.player
        lob_cell = (self.rect.x, self.rect.y)
        player_cell = (int(player.x), int(player.y))
        if not len(self.chek_lst) and self.payment(player_cell, lob_cell):
            self.chek_lst.append(player_cell)
        elif len(self.chek_lst) and self.payment(player_cell, self.chek_lst[-1]):
            self.chek_lst.append(player_cell)
        if len(self.chek_lst):
            if self.chek_lst[0][0] > lob_cell[0]:
                self.rect = self.rect.move(1, 0)
            elif self.chek_lst[0][0] < lob_cell[0]:
                self.rect = self.rect.move(-1, 0)
            elif self.chek_lst[0][1] > lob_cell[1]:
                self.rect = self.rect.move(0, 1)
            elif self.chek_lst[0][1] < lob_cell[1]:
                self.rect = self.rect.move(0, -1)
            self.rect = self.rect.move(0, 0)
            if self.chek_lst[0] == lob_cell:
                del self.chek_lst[0]
        ls = board.get_cell((self.rect.x, self.rect.y))
        if board.get_color(ls) == 'white':
            board.open_map(ls)
            self.wall.append(ls)
            self.board.board[ls[0]][ls[1]].color = 'black'
        elif len(self.wall) and ls != self.wall[0]:
            board.open_map(self.wall[0])
            self.board.board[self.wall[0][0]][self.wall[0][1]].color = 'white'
            del self.wall[0]

    def die(self):
        self.kill()


class Merzopakostniy(pygame.sprite.Sprite):
    def __init__(self, group, pos, board, player):
        super().__init__(group)
        self.group = group
        self.image = mersz
        self.board = board
        self.player = player
        pos_x, pos_y = pos
        self.x = self.y = 0
        self.chek_lst = []
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.time = self.step = 0
        self.list_bomb = []

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def move(self):
        b = self.board
        self.step += 1
        i, ln = 0, len(self.chek_lst)
        while i < ln and ln:
            self.chek_lst[i] -= 1
            if not self.chek_lst[i]:
                self.list_bomb[i].die()
                del self.list_bomb[i], self.chek_lst[i]
                ln = len(self.chek_lst)
            i += 1
        if self.step == 240:
            bx, by = b.get_coords((b.get_cell((self.rect.x, self.rect.y))))
            bomb = Bomb(self.group, bx, by)
            bomb.resize(30)
            self.list_bomb.append(bomb)
            self.chek_lst.append(randint(300, 390))
            self.step = 0
        if not self.y and not self.x:
            while True:
                self.y = randint(1, (len(self.board.wall_map) - 3))
                self.x = randint(1, (len(self.board.wall_map[0]) - 3))
                if not self.board.wall_map[self.y][self.x]:
                    self.x, self.y = self.board.get_coords((self.x, self.y))
                    break
        ls = (self.rect.x, self.rect.y)
        if self.y == self.rect.y and self.rect.x == self.x:
            self.x = self.y = 0
        elif self.y == self.rect.y:
            if self.x > self.rect.x:
                if 'black' == b.get_color(b.get_cell((ls[0] + 30, ls[1]))):
                    self.rect = self.rect.move(1, 0)
                else:
                    self.x = self.rect.x
            elif self.x < self.rect.x:
                if 'black' == b.get_color(b.get_cell((ls[0] - 1, ls[1]))):
                    self.rect = self.rect.move(-1, 0)
                else:
                    self.x = self.rect.x
        else:
            if self.y > self.rect.y:
                if 'black' == b.get_color(b.get_cell((ls[0], ls[1] + 30))):
                    self.rect = self.rect.move(0, 1)
                else:
                    self.y = self.rect.y
            elif self.y < self.rect.y:
                if 'black' == b.get_color(b.get_cell((ls[0], ls[1] - 1))):
                    self.rect = self.rect.move(0, -1)
                else:
                    self.y = self.rect.y

    def num_bomb(self):
        return self.list_bomb


class Legushka(pygame.sprite.Sprite):
    def __init__(self, group, pos, board, player):
        super().__init__(group)
        pos_x, pos_y = pos
        self.image = leg_img
        self.board = board
        self.player = player
        self.speed = 0.5
        self.x = self.y = 0
        self.chek_lst = []
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def payment(self, leg_cell):
        lst = [self.chek_lst[0], leg_cell]
        count = 1
        x = (lst[0][0] - lst[1][0])
        y = (lst[0][1] - lst[1][1])
        while True:
            if 0 != abs(x / (count + 1)) < 1 or 0 != abs(y / (count + 1)) < 1:
                x, y = x / count, y / count
                break
            count += 1
        if not int(x) and not int(y):
            y = x = 1
        return (x, y)

    def move(self):
        x, y = self.x, self.y
        board, player = self.board, self.player
        leg_cell = (self.rect.x, self.rect.y)
        player_cell = (int(player.x), int(player.y))
        if not len(self.chek_lst) and board.get_color(board.get_cell(player_cell)) \
                and player_cell[0] % 30 == 0 and player_cell[1] % 30 == 0:
            self.chek_lst.append(player_cell)
            self.x, self.y = x, y = self.payment(leg_cell)
        elif len(self.chek_lst) and (leg_cell[0], leg_cell[1]) == self.chek_lst[0]:
            if abs(leg_cell[0] - player_cell[0]) >= 150 or \
                    abs(leg_cell[1] - player_cell[1]) >= 150:
                del self.chek_lst[0]
            else:
                x = y = 0
        if len(self.chek_lst):
            if leg_cell[0] == self.chek_lst[0][0]:
                self.rect = self.rect.move(0, y)
            elif leg_cell[1] == self.chek_lst[0][1]:
                self.rect = self.rect.move(x, 0)
            else:
                self.rect = self.rect.move(x, y)

    def die(self):
        self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, group, pos_x, pos_y):
        super().__init__(group)
        self.image = bb
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def resize(self, size):
        self.image = pygame.transform.scale(self.image, (size, size))

    def die(self):
        self.kill()


class Finish(pygame.sprite.Sprite):
    def __init__(self, group, record):
        super().__init__(group)
        self.image = load_image('die.jpg')
        self.rect = self.image.get_rect().move(-1000, 0)
        # pygame.mixer.music.load('data\\probitie.wav')
        # pygame.mixer.music.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 20 <= x <= 230 and 320 <= y <= 350:
                        return
                    elif 20 <= x <= 195 and 455 <= y <= 485:
                        global name
                        a = name[name.index('\\') + 1:]
                        con = sqlite3.connect('data\\records.db')
                        cur = con.cursor()
                        hero = input('Введите ник: ')
                        result = cur.execute('''SELECT * from records where map="{}" 
                        AND name="{}"'''.format(a, hero)).fetchall()
                        if len(result):
                            if result[0][0] < int(record):
                                cur.execute('''UPDATE records SET point = {}
                                 WHERE name = "{}"'''.format(int(record), hero)).fetchall()
                        else:
                            cur.execute('''INSERT INTO records 
                            VALUES ({},"{}","{}")'''.format(int(record), hero, a)).fetchall()
                            con.commit()
                        global f_f_f
                        if f_f_f:
                            try:
                                maps = a[:a.find('.')]
                                glaf = True
                                if maps in [i['name_map'] for i in get(ip + '/api/maps').json()['maps']]:
                                    users = get(ip + '/api/user').json()['users']
                                    for user in users:
                                        if hero == user['name']:
                                            for rec in get(ip + '/api/records/' + maps).json()['records']:
                                                if user['id'] == rec['user_id']:
                                                    print(3.1)
                                                    if rec['points'] < int(record):
                                                        print(post(f"{ip}/api/records/{rec['id']}",
                                                                   json={'points': int(record)}).json())
                                                    glaf = False
                                                    break
                                            if glaf:
                                                print(post(ip + '/api/records',
                                                           json={'points': int(record),
                                                                 'map_name': maps,
                                                                 'user_id': user['id']}).json())

                                            break
                            except:
                                f_f_f = False
                    elif 20 <= x <= 125 and 545 <= y <= 575:
                        terminate()
            if self.rect.x < 0:
                self.rect.x += 2
            time.sleep(0.00001)
            group.draw(screen)
            group.update()
            pygame.display.flip()


class Check:
    def __init__(self, player, lst):
        self.lst = lst
        self.player = player

    def checkaed(self):
        x, y = int(self.player.x), int(self.player.y)
        x, y = set(range(x, x + 30)), set(range(y, y + 30))
        for name in self.lst:
            name_x = set(range(name.rect.x + 7, name.rect.x + 23))
            name_y = set(range(name.rect.y + 7, name.rect.y + 23))
            if name_x & x and name_y & y:
                return True


def draw(txt):
    if 6 - len(txt) < 0:
        txt = '999999'
    else:
        txt = (6 - len(txt)) * '0' + txt
    font = pygame.font.Font(None, 30)
    text = font.render("hight score " + txt, 1, (100, 255, 100))
    screen.blit(text, (30, 0))


def game():
    global name
    group = pygame.sprite.Group()
    player_anim = Anime(group, (228, 288))
    board = Board.load_map(None, name)
    board.set_view(30, 30, 30)
    lst = []
    if sum(board.hero[0]):
        player = Player(screen, player_anim, board, board.hero[0])
        player_anim.resize(30)
    if sum(board.hero[1]):
        tverdolobiy = Tverdolobiy(group, board.hero[1], board, player)
        tverdolobiy.resize(30)
        lst.append(tverdolobiy)
    if sum(board.hero[2]):
        merzopakostniy = Merzopakostniy(group, board.hero[2], board, player)
        merzopakostniy.resize(30)
    if sum(board.hero[3]):
        legushka = Legushka(group, board.hero[3], board, player)
        legushka.resize(30)
        lst.append(legushka)
    running = True
    c = 0
    while running:
        c += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key in up:
                    player.set_dir('up')
                if event.key in down:
                    player.set_dir('down')
                if event.key in left:
                    player.set_dir('left')
                if event.key in right:
                    player.set_dir('right')
                if event.key == pygame.K_LEFT:
                    player.set_dir('left')
                if event.key == pygame.K_RIGHT:
                    player.set_dir('right')
                if event.key == pygame.K_UP:
                    player.set_dir('up')
                if event.key == pygame.K_DOWN:
                    player.set_dir('down')
        screen.fill((0, 0, 0))
        board.render()
        if not len(board.check_points):
            board.check_points.add(None)
        if not board.are_left():
            board.reset()
        player.move([])
        player_anim.rect.x, player_anim.rect.y = player.x, player.y
        if sum(board.hero[2]):
            merzopakostniy.move()
        if not c % 2:
            if sum(board.hero[3]):
                legushka.move()
            if sum(board.hero[1]):
                tverdolobiy.move()
        group.draw(screen)
        if c % 20 == 0:
            player_anim.update()
        if sum(board.hero[2]):
            check = Check(player, merzopakostniy.num_bomb() + lst)
        elif sum(board.hero[0]):
            check = Check(player, lst)
        if check.checkaed():
            running = False
        draw(str(len(board.check_points) - 1 + board.count))
        pygame.display.flip()
        clock.tick(FPS * 3)
    Finish(group, str(len(board.check_points) - 1 + board.count))


FON = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))


def load_screen():
    if True:
        p = (-1, -1)
        f = False
        group = pygame.sprite.Group()
        b = Button()
        screen.blit(FON, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEMOTION:
                    p = event.pos
                    group.update(event.pos, False)
                    b.update(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if b.update(event.pos, True):
                        game()
                        return
            group.update(p, f)
            group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


while True:
    load_screen()
