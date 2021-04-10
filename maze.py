import pygame as pg

# ToDo Найти картинки фона, персонажей, предметы
# Todo Загрузить музыку для фона, и эффектов - поймал охранник, собрал предмет, Геемовер и Победа

pg.init()  # настройка pygame на наше железо, в том числе видео карта, звуковая и установленные шрифты
win_width, win_height = 1600, 900  # задаем размеры экранной поверхности
window = pg.display.set_mode((win_width, win_height))

BLUE = (45, 62, 172)

window.fill(BLUE)

clock = pg.time.Clock()
FPS = 30  # частота срабатывания таймера 30 кадров в секунду

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.display.update()
    clock.tick(FPS)
