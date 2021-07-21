from .constants import *


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
    def __init__(self, img, x, y, size_x, size_y, speed):
        super().__init__(img, x, y, size_x, size_y, speed)
        self.bag = Bag(x=50, y=2)
        self.life = LIFE_HERO
        self.life_img = Text(text=f"Life = {self.life}", x=300, y=10, fsize=30, color=WHITE)
        self.points = 0
        self.points_img = Text(text=f"Points = 0", x=450, y=10, fsize=30, color=WHITE)

    def update(self, walls, guards, control_timer, aurums):
        if not control_timer.flag and pg.sprite.spritecollide(self, guards, dokill=False):
            self.life -= 1
            control_timer.freeze(3)
        if self.life > 0:
            if pg.sprite.spritecollide(self, aurums, dokill=True):
                self.points += 1
                self.points_img.set_text(f"Points = {self.points}")
            self.life_img.set_text(f"Life = {self.life}")
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
            self.bag.update()
        else:
            self.life_img.set_text(f"Life = 0")

    def reset(self, screen):
        super().reset()
        self.bag.draw(screen)
        self.life_img.draw(screen)
        self.points_img.draw(screen)


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

    def update(self, player, walls, timer):
        # Состояние прямой видимости
        self.go_to_goal_visible(player, walls)

        while not self.state == "Прямая видимость" and self.rect.collidepoint(self.end_x, self.end_y):
            # выбор случайной точки в состоянии Патруль или Погоня
            if self.state == "Патруль":
                self.choice()
            if self.state == "Погоня":
                self.choice_random_point(player)
        self.last_x, self.last_y = self.rect.x, self.rect.y

        x, y = self.rect.x, self.rect.y
        if not timer.flag and self.last_y > self.end_y - 3:  # делаем +/- 5 из за зависаний в разных точках
            self.rect.y -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if not timer.flag and self.last_y < self.end_y + 3:
            self.rect.y += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.y = y
        if not timer.flag and self.last_x > self.end_x - 3:
            self.rect.x -= self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if not timer.flag and self.last_x < self.end_x + 3:
            self.rect.x += self.speed
            if pg.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = x
        if not timer.flag and self.last_x == self.rect.x and self.last_y == self.rect.y:
            self.choice()
            self.state = "Патруль"
        self.scanner.update(x=self.rect.centerx, y=self.rect.centery)
        self.scanner_walls.update(x=self.rect.centerx, y=self.rect.centery)

    def go_to_goal_visible(self, player, walls):
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


class ControlTimer:
    def __init__(self):
        self.timer_freeze = None
        self.flag = False

    def freeze(self, t):
        if self.timer_freeze is None:
            self.timer_freeze = Timer(text="Time freeze: ", start_time=t,
                                 x=win_width - 250, y=10, fsize=30, color=WHITE)
        else:
            self.timer_freeze.up_time(t)
        self.flag = True

    def update(self, screen):
        if self.flag:
            self.timer_freeze.update(screen)
            if self.timer_freeze.is_end():
                del self.timer_freeze
                self.timer_freeze = None
                self.flag = False


class Elexir(GameSprite):
    def __init__(self, img, x, y, size_x, size_y, mode, timer):
        super().__init__(img, x, y, size_x, size_y, 0)
        self.mode = mode
        self.last_time = time()
        self.visible = True
        self.control_timer = timer

    def update(self, player, elixirs):
        if self.visible and time() - self.last_time > 10:
            self.kill()
        if self.visible and pg.sprite.collide_rect(self, player):
            if player.bag.add_item(self):  # добавить в инвентарь
                self.hide()
        if not self.visible:
            elixirs.remove(self)

    def hide(self):
        self.visible = False

    def action(self):
        if self.mode == 1:
            self.control_timer.freeze(10)
        elif self.mode == 2:
            pass  # для Силы
        self.kill()


class Cell:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 40, 40)  # квадрат
        self.fill_color = BLUE

    def draw(self, mw):
        pg.draw.rect(mw, self.fill_color, self.rect)
        # обводка существующего прямоугольника
        pg.draw.rect(mw, DARK_BLUE, self.rect, 3)


# Значение в списке items - 0 - пусто, 1- зелье Зеленое, 2- зелье Желтое, 3 - зелье Красное
class Bag:
    def __init__(self, x, y):
        self.cells = [Cell(x + 40 * i, y) for i in range(5)]
        self.items = [None]*5
        self.images = [None, pg.transform.scale(pg.image.load("freeze.png"), (32, 32)),
                       pg.transform.scale(pg.image.load("yellow.png"), (32, 32)),
                       pg.transform.scale(pg.image.load("red.png"), (32, 32))]

    def add_item(self, item):
        for i in range(5):
            if self.items[i] is None:
                self.items[i] = item
                return True
        return False

    def activate_item(self, i):
        if self.items[i] is not None:
            self.items[i].action()
            self.items[i] = None

    def update(self):
        keys = pg.key.get_pressed()  # получаем словарь со всеми клавишами и их состоянием
        if keys[pg.K_1]:
            self.activate_item(0)
        if keys[pg.K_2]:
            self.activate_item(1)
        if keys[pg.K_3]:
            self.activate_item(2)
        if keys[pg.K_4]:
            self.activate_item(3)
        if keys[pg.K_5]:
            self.activate_item(4)

    def draw_item(self, item, screen, x, y):
        if item is not None:
            screen.blit(self.images[item.mode], (x, y))

    def draw(self, screen):
        for i in range(5):
            self.cells[i].draw(screen)
            self.draw_item(self.items[i], screen, self.cells[i].rect.x + 4, self.cells[i].rect.y + 4)


