import pygame as pg
from random import randint
from time import time

# ToDo Добавить охранникам сканер - если попадаем в поле зрения, бегут за нами
# Todo Загрузить музыку для фона, и эффектов - поймал охранник, собрал предмет, Геемовер и Победа


WHITE = (255, 255, 255)
BLUE = (45, 62, 202)
GREEN = (50, 200, 60)
RED = (150, 30, 30)


class GameSprite(pg.sprite.Sprite):
    def __init__(self, img, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(img), (size_x, size_y))
        self.rect = self.image.get_rect()  # рамка вокруг картинки
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self) -> None:
        keys = pg.key.get_pressed()  # получаем словарь со всеми клавишами и их состоянием
        x, y = self.rect.x, self.rect.y
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if keys[pg.K_UP]:
            self.rect.y -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if keys[pg.K_DOWN]:
            self.rect.y += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y



class Guard(GameSprite):
    def __init__(self, img, x, y, size_x, size_y, speed):
        super().__init__(img, x, y, size_x, size_y, speed)
        self.end_x = randint(10, win_width//5 - 10) * 5  # случайное положение по оси х
        self.end_y = randint(10, win_height//5 - 10) * 5  # случайное положение по оси у
        self.last_x, self.last_y = x, y


    def update(self):
        if self.rect.collidepoint(self.end_x, self.end_y):
            self.end_x = randint(10, win_width // 5 - 10) * 5  # случайное положение по оси х
            self.end_y = randint(10, win_height // 5 - 10) * 5

        if self.last_y == self.rect.y and self.last_y - self.end_y < 0:
            self.up_down = "down"
        elif self.last_y == self.rect.y and self.last_y - self.end_y > 0:
            self.up_down = "up"
        if self.last_x == self.rect.x and self.last_x - self.end_x < 0:
            self.left_right = "right"
        elif self.last_x == self.rect.x and self.last_x - self.end_x > 0:
            self.left_right = "left"
        x, y = self.rect.x, self.rect.y
        if self.up_down == "up":
            self.rect.y = self.rect.y - self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        elif self.up_down == "down":
            self.rect.y += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if self.left_right == "left":
            self.rect.x -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        elif self.left_right == "right":
            self.rect.x += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, color):
        super().__init__()
        self.image = pg.Surface((size_x, size_y))
        self.image.fill(color)
        self.rect = self.image.get_rect()  # рамка вокруг картинки
        self.rect.x = x
        self.rect.y = y


class Text:
    def __init__(self, text, x, y, fsize=30, color=WHITE):
        self.text = text
        self.color = color
        self.fsize = fsize
        self.font = pg.font.SysFont("Arial", fsize)
        self.image = self.font.render(self.text, True, self.color)
        self.x = x
        self.y = y

    def set_text(self, text):
        self.text = text
        self.render()

    def render(self):
        self.image = self.font.render(self.text, True, self.color)

    def set_color(self, color):
        self.color = color
        self.render()

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window2):
        window2.blit(self.image, (self.x, self.y))

    def text_update(self, text, window2):
        self.set_text(text)
        self.draw(window2)


class Timer(Text):
    def __init__(self, text, start_time, x, y, fsize, color):
        super().__init__(text, x, y, fsize, color)
        self.start_time = start_time
        self.last_time = time()
        self.text_prefix = text  # чтобы не перезаписывать каждый раз Тест до значения таймера

    def update(self, window2):
        if self.start_time > 0 and time() - self.last_time > 1:
            self.start_time -= 1
            self.last_time = time()
        self.text_update(self.text_prefix + str(self.start_time), window2)

    def is_end(self):
        return self.start_time == 0


pg.init()  # настройка pygame на наше железо, в том числе видео карта, звуковая и установленные шрифты
pg.font.init()
win_width, win_height = 1200, 900  # задаем размеры экранной поверхности
window = pg.display.set_mode((win_width, win_height))

background = pg.image.load("fon0.jpg")
# растягиваем или сжимаем картинку до нужного размера
background = pg.transform.scale(background, (win_width, win_height))

font = pg.font.SysFont("Arial", 120)  # подключаем модуль font из pygame и создаем объект Шрифт
win = font.render("You WIN!!!", True, GREEN)
lose = font.render("You LOSE!!!", True, RED)


hero = Player(img="шар.png", x=45, y=45, size_x=50, size_y=50, speed=10)
guards = pg.sprite.Group()
guards.add(
    Guard(img="шар.png", x=win_width - 100, y=win_height//2, size_x=50, size_y=50, speed=7),
    Guard(img="шар.png", x=win_width//2, y=win_height//2, size_x=50, size_y=50, speed=7)
)
aurum = GameSprite(img="treasure.png", x=win_width - 100, y=win_height - 100, size_x=60, size_y=60, speed=10)
walls = pg.sprite.Group()
walls.add(
    # горизонтальные
    Wall(x=0, y=0, size_x=win_width, size_y=43, color=BLUE),
    Wall(x=0, y=win_height - 40, size_x=win_width, size_y=40, color=BLUE),
    Wall(x=0, y=525, size_x=375, size_y=15, color=BLUE),
    # вертикальные
    Wall(x=0, y=0, size_x=45, size_y=win_height, color=BLUE),
    Wall(x=win_width//2, y=0, size_x=15, size_y=win_height//2, color=BLUE),
    Wall(x=win_width - 35, y=0, size_x=35, size_y=win_height, color=BLUE),
    Wall(x=112, y=0, size_x=15, size_y=375, color=BLUE),
)
# window.fill(BLUE)   # заливка экрана одним цветом

timer = Timer(text="Time: ", start_time=30, x=win_width - 150, y=10, fsize=30, color=WHITE)

clock = pg.time.Clock()
FPS = 30  # частота срабатывания таймера 30 кадров в секунду

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    # обновляем координаты и накладываем на экранную поверхность фон и всех спрайтов
    # window.blit(background, (0, 0))  # копирование изображения на экранную поверхность
    window.fill(GREEN)
    hero.update()
    guards.update()
    hero.reset()
    aurum.reset()

    guards.draw(window)
    walls.draw(window)  # вызываем групповой метод копирования изображения каждой стены на экранную поверхность
    timer.update(window)

    if timer.is_end():
        window.blit(lose, (win_width//2 - 100, win_height//2 - 50))
    pg.display.update()

    clock.tick(FPS)



