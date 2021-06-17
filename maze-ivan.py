import pygame as pg

from time import time

# Todo Добавить телепорты по углам карты
# Todo Элексир заморозки - с определенным радиусом и суперсилы - на короткое время.
# Todo Загрузить музыку для фона, и эффектов - поймал охранник, собрал предмет, Геймовер и Победа

WHITE = (255, 255, 255)
BLUE = (45, 62, 202)
GREEN = (50, 200, 60)
RED = (150, 30, 30)

win_width, win_height = 1200, 900  # задаем размеры экранной поверхности
timer_freeze = None


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


class Guard(GameSprite): #! sdfsdfsfd
    # Todo Сделать рефакторинг update
    # ToDo В дальнейшем добавить разделение на разные маршруты
    # ToDo Проверить сброс генератора случайных чисел - при создание спрайта
    # ToDo Проверить алгоритм входа в коридор - чтобы не зависал на пол тела
    position = [(60, 60), (win_width - 110, 60), (win_width//2, win_height//2),
                (60, win_height - 110), (win_width - 110, win_height - 110),
                (60, win_height//2), (win_width - 110, win_height//2),
                (win_width//2, 60), (win_width//2, win_height - 110)]

    def __init__(self, img, x, y, size_x, size_y, speed):
        super().__init__(img, x, y, size_x, size_y, speed)
        self.choice()
        self.last_x, self.last_y = None, None
        self.scanner = Scanner(x=self.rect.centerx, y=self.rect.centery, size_x=size_x*50, size_y=size_x*50)
        self.scanner_walls = Scanner(x=self.rect.centerx, y=self.rect.centery,
                                     size_x=size_x, size_y=size_x)
        self.state = "Патруль"
        self.sled = []

    def choice(self):
        from random import choice
        self.end_x, self.end_y = choice(Guard.position)

    def update(self, player):
        global timer
        # Состояние прямой видимости
        self.go_to_goal_visible(player)

        while not self.state == "Прямая видимость" and self.rect.collidepoint(self.end_x, self.end_y):
            # выбор случайной точки в состоянии Патруль или Погоня
            if self.state == "Патруль":
                self.choice()
            if self.state == "Погоня":
                self.choice_random_point(player)
        self.last_x, self.last_y = self.rect.x, self.rect.y

        x, y = self.rect.x, self.rect.y
        if not timer and self.last_y > self.end_y - 3:  # делаем +/- 5 из за зависаний в разных точках
            self.rect.y -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if not timer and self.last_y < self.end_y + 3:
            self.rect.y += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if not timer and self.last_x > self.end_x - 3:
            self.rect.x -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if not timer and self.last_x < self.end_x + 3:
            self.rect.x += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if not timer and self.last_x == self.rect.x and self.last_y == self.rect.y:
            self.choice()
            self.state = "Патруль"
        self.scanner.update(x=self.rect.centerx, y=self.rect.centery)
        self.scanner_walls.update(x=self.rect.centerx, y=self.rect.centery)

    def go_to_goal_visible(self, player):
        if pg.sprite.collide_rect(self.scanner, player):
            self.scanner_walls.rect = pg.draw.line(window, GREEN,
                                                   (self.rect.centerx, self.rect.centery),
                                                   (player.rect.centerx, player.rect.centery))
            for wall in walls:
                if pg.sprite.collide_rect(self.scanner_walls, wall):
                    if self.state == "Прямая видимость":
                        self.state = "Погоня"
                        self.sled.append((player.rect.x, player.rect.y))
                    elif self.state == "Погоня":
                        self.sled.append((player.rect.x, player.rect.y))
                    break
            else:
                self.end_x, self.end_y = player.rect.x, player.rect.y
                self.state = "Прямая видимость"
                self.sled.clear()

    def choice_random_point(self, player):
        # Находится в состоянии Погоня, в точке где потерял из виду
        if len(self.sled) > 0:
            self.end_x, self.end_y = self.sled.pop(0)
        else:
            self.state = "Патруль"

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
        self.font.set_italic(True)  # Устанвливаем оформление шрифта в Курсив
        self.image = self.font.render(self.text, True, self.color)  # создаем картинку из текста
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

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def text_update(self, text, screen):
        self.set_text(text)
        self.draw(screen)


class Timer(Text):
    def __init__(self, start_time, x, y, fsize, color, text=""):
        super().__init__(text, x, y, fsize, color)
        self.start_time = start_time
        self.current_time = start_time
        self.last_time = time()  # получаем текущее значение в секундах с 1 янв 1970 года
        self.text_prefix = text  # чтобы не перезаписывать каждый раз Тест до значения таймера
        self.pause = False
        self.start_color = color

    def update(self, screen):
        if self.current_time > 0 and not self.pause and time() - self.last_time > 1:
            self.current_time -= 1
            self.last_time = time()
        elif self.pause and time() - self.last_time > 0.5:
            self.last_time = time()
            if self.color == self.start_color:
                self.set_color(RED)
            else:
                self.set_color(self.start_color)
        self.text_update(self.text_prefix + str(self.current_time), screen)

    def is_end(self):
        return self.current_time == 0

    def do_pause(self):
        if self.pause:
            self.pause = False
            self.last_time = time()
        else:
            self.pause = True

    def up_time(self, add_time):
        self.current_time += add_time

    def restart(self):
        self.current_time = self.start_time


def freeze():
    global timer_freeze, timer

    if timer_freeze is None:
        timer_freeze = Timer(text="Time freeze: ", start_time=10,
                             x=win_width - 250, y=10, fsize=30, color=WHITE)
    else:
        timer_freeze.up_time(10)
    timer = True


class Elexir(GameSprite):
    def __init__(self, img, x, y, size_x, size_y, mode):
        super().__init__(img, x, y, size_x, size_y, 0)
        self.mode = mode
        self.last_time = time()

    def update(self, player):
        if time() - self.last_time > 10:
            self.kill()
        if pg.sprite.collide_rect(self, player):
            self.action()
            self.kill()

    def action(self):
        if self.mode == 1:
            freeze()
        elif self.mode == 2:
            pass # для Силы

def add_elixir():
    from random import randint
    temp_el = Elexir(img="freeze.png", x=randint(10, win_width//5 - 10) * 5,
                     y=randint(10, win_height//5 - 10) * 5, size_x=40, size_y=40, mode=1)
    while (pg.sprite.spritecollide(temp_el, walls, dokill=False) or
            pg.sprite.collide_rect(temp_el, hero)):
        temp_el.rect.x = randint(10, win_width//5 - 10) * 5
        temp_el.rect.y = randint(10, win_height//5 - 10) * 5
    elixirs.add(temp_el)

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

elixirs = pg.sprite.Group()

timer = False

clock = pg.time.Clock()
FPS = 30  # частота срабатывания таймера 30 кадров в секунду

last_time_el = time()

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
    elixirs.update(hero)

    hero.reset()
    aurum.reset()

    guards.draw(window)
    walls.draw(window)  # вызываем групповой метод копирования изображения каждой стены на экранную поверхность
    setka.draw(window)
    elixirs.draw(window)

    if timer:
        timer_freeze.update(window)
        if timer_freeze.is_end():
            timer_freeze = None
            timer = False

    if time() - last_time_el > 35:
        add_elixir()
        last_time_el = time()

    pg.display.update()

    clock.tick(FPS)



