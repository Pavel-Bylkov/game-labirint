import pygame as pg
from random import randint

# ToDo Доделать расстановку стен
# ToDo Добавить охранников
# Todo Загрузить музыку для фона, и эффектов - поймал охранник, собрал предмет, Геемовер и Победа

directions = {"up": 0, "down": 180, "left": -90, "right": 90}


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
        pos = self.rect.x, self.rect.y
        if keys[pg.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < win_width - 5:
            self.rect.x += self.speed
        if keys[pg.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN] and self.rect.bottom < win_height - 5:
            self.rect.y += self.speed
        if pg.sprite.spritecollide(self, walls, dokill=False):
            self.rect.x, self.rect.y = pos


class Guard(GameSprite):
    def __init__(self, img, x, y, size_x, size_y, speed, direction, start, end):
        super().__init__(img, x, y, size_x, size_y, speed)
        self.direction = direction
        self.start = start  # граница сверху или слева
        self.end = end  # граница снизу или справа

    def update(self):
        if self.direction == directions["up"] and self.rect.y < self.start:
            self.direction = directions["down"]
        elif self.direction == directions["down"] and self.rect.y > self.end:
            self.direction = directions["up"]
        elif self.direction == directions["left"] and self.rect.x < self.start:
            self.direction = directions["right"]
        elif self.direction == directions["right"] and self.rect.x > self.end:
            self.direction = directions["left"]

        if self.direction == directions["up"]:
            self.rect.y -= self.speed
        elif self.direction == directions["down"]:
            self.rect.y += self.speed
        elif self.direction == directions["left"]:
            self.rect.x -= self.speed
        elif self.direction == directions["right"]:
            self.rect.x += self.speed


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, color):
        super().__init__()
        self.image = pg.Surface((size_x, size_y))
        self.image.fill(color)
        self.rect = self.image.get_rect()  # рамка вокруг картинки
        self.rect.x = x
        self.rect.y = y


pg.init()  # настройка pygame на наше железо, в том числе видео карта, звуковая и установленные шрифты
win_width, win_height = 1200, 900  # задаем размеры экранной поверхности
window = pg.display.set_mode((win_width, win_height))

background = pg.image.load("fon0.jpg")
# растягиваем или сжимаем картинку до нужного размера
background = pg.transform.scale(background, (win_width, win_height))

BLUE = (45, 62, 172)

hero = Player(img="шар.png", x=45, y=45, size_x=50, size_y=50, speed=10)
guards = pg.sprite.Group()
guards.add(
    Guard(img="шар.png", x=win_width - 100, y=win_height//2, size_x=50, size_y=50,
              speed=7, direction=-90, start=500, end=win_width - 100)
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
    Wall(x=win_width - 35, y=0, size_x=35, size_y=win_height, color=BLUE),
    Wall(x=112, y=0, size_x=15, size_y=375, color=BLUE),
)
# window.fill(BLUE)   # заливка экрана одним цветом

clock = pg.time.Clock()
FPS = 30  # частота срабатывания таймера 30 кадров в секунду

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    window.blit(background, (0, 0))  # копирование изображения на экранную поверхность
    hero.update()
    guards.update()
    hero.reset()
    aurum.reset()
    guards.draw(window)
    walls.draw(window)  # вызываем групповой метод копирования изображения каждой стены на экранную поверхность
    pg.display.update()
    clock.tick(FPS)

