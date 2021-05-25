import pygame as pg

from time import time

# ToDo Добавить охранникам сканер - если попадаем в поле зрения, бегут за нами
# Todo Загрузить музыку для фона, и эффектов - поймал охранник, собрал предмет, Геемовер и Победа

WHITE = (255, 255, 255)
BLUE = (45, 62, 202)
GREEN = (50, 200, 60)
RED = (150, 30, 30)

win_width, win_height = 1200, 900  # задаем размеры экранной поверхности


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


class Scanner(pg.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        super().__init__()
        self.image = pg.Surface((size_x, size_y))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()  # рамка вокруг картинки
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y


class Guard(GameSprite):
    # ToDo В дальнейшем добавить разделение на разные маршруты
    # ToDo Проверить сброс генератора случайных чисел - при создание спрайта
    position = [(60, 60), (win_width - 110, 60), (win_width//2, win_height//2),
                (60, win_height - 110), (win_width - 110, win_height - 110),
                (60, win_height//2), (win_width - 110, win_height//2),
                (win_width//2, 60), (win_width//2, win_height - 110)]

    def __init__(self, img, x, y, size_x, size_y, speed):
        super().__init__(img, x, y, size_x, size_y, speed)
        from random import choice
        self.choice = choice
        self.end_x, self.end_y = self.choice(Guard.position)
        self.last_x, self.last_y = None, None
        self.scanner = Scanner(x=self.rect.centerx, y=self.rect.centery, size_x=size_x*50, size_y=size_x*50)
        self.scanner_walls = Scanner(x=self.rect.centerx, y=self.rect.centery,
                                     size_x=size_x, size_y=size_x)

    def update(self, player):
        if pg.sprite.collide_rect(self.scanner, player):
            self.scanner_walls.rect = pg.draw.line(window, GREEN,
                                                   (self.rect.centerx, self.rect.centery),
                                                   (player.rect.centerx, player.rect.centery))
            for wall in walls:
                if pg.sprite.collide_rect(self.scanner_walls, wall):
                    break
            else:
                self.end_x, self.end_y = player.rect.x, player.rect.y
        while self.rect.collidepoint(self.end_x, self.end_y):
            self.end_x, self.end_y = self.choice(Guard.position)
        self.last_x, self.last_y = self.rect.x, self.rect.y

        x, y = self.rect.x, self.rect.y
        if self.last_y > self.end_y - 3:  # делаем +/- 5 из за зависаний в разных точках
            self.rect.y -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if self.last_y < self.end_y + 3:
            self.rect.y += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if self.last_x > self.end_x - 3:
            self.rect.x -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if self.last_x < self.end_x + 3:
            self.rect.x += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if self.last_x == self.rect.x and self.last_y == self.rect.y:
            self.end_x, self.end_y = self.choice(Guard.position)
        self.scanner.update(x=self.rect.centerx, y=self.rect.centery)
        self.scanner_walls.update(x=self.rect.centerx, y=self.rect.centery)


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
    Guard(img="шар.png", x=win_width - 100, y=win_height//2, size_x=50, size_y=50, speed=4),
    Guard(img="шар.png", x=win_width//2, y=win_height//2, size_x=50, size_y=50, speed=4)
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
setka = pg.sprite.Group()
for y in range(50, win_height, 50):
    setka.add(Wall(x=0, y=y, size_x=win_width, size_y=2, color=RED))
for x in range(50, win_width, 50):
    setka.add(Wall(x=x, y=0, size_x=2, size_y=win_height, color=RED))
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
    guards.update(hero)
    hero.reset()
    aurum.reset()

    guards.draw(window)
    walls.draw(window)  # вызываем групповой метод копирования изображения каждой стены на экранную поверхность
    setka.draw(window)
    timer.update(window)

    if timer.is_end():
        window.blit(lose, (win_width//2 - 100, win_height//2 - 50))
    pg.display.update()

    clock.tick(FPS)



