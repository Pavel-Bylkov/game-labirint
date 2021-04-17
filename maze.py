import pygame as pg

# ToDo Найти картинки фона, персонажей, предметы
# Todo Загрузить музыку для фона, и эффектов - поймал охранник, собрал предмет, Геемовер и Победа


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
        if keys[pg.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < win_width - 5:
            self.rect.x += self.speed
        if keys[pg.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN] and self.rect.bottom < win_height - 5:
            self.rect.y += self.speed


pg.init()  # настройка pygame на наше железо, в том числе видео карта, звуковая и установленные шрифты
win_width, win_height = 1200, 900  # задаем размеры экранной поверхности
window = pg.display.set_mode((win_width, win_height))

background = pg.image.load("fon0.jpg")
# растягиваем или сжимаем картинку до нужного размера
background = pg.transform.scale(background, (win_width, win_height))

BLUE = (45, 62, 172)

hero = Player(img="шар.png", x=40, y=40, size_x=60, size_y=60, speed=10)
aurum = GameSprite(img="treasure.png", x=win_width - 100, y=win_height - 100, size_x=60, size_y=60, speed=10)

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
    hero.reset()
    aurum.reset()
    pg.display.update()
    clock.tick(FPS)
