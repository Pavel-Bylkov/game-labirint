import pygame as pg

from time import time

WHITE = (255, 255, 255)
BLUE = (45, 62, 202)
GREEN = (50, 200, 60)
RED = (150, 30, 30)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)

win_width, win_height = 1200, 900  # задаем размеры экранной поверхности

pg.init()  # настройка pygame на наше железо, в том числе видео карта, звуковая и установленные шрифты
pg.font.init()

window = pg.display.set_mode((win_width, win_height))

# background = pg.image.load("fon0.jpg")
# # растягиваем или сжимаем картинку до нужного размера
# background = pg.transform.scale(background, (win_width, win_height))

font = pg.font.SysFont("Arial", 120)  # подключаем модуль font из pygame и создаем объект Шрифт
win = font.render("You WIN!!!", True, GREEN)
lose = font.render("You LOSE!!!", True, RED)

clock = pg.time.Clock()
FPS = 30  # частота срабатывания таймера 30 кадров в секунду

timer_freeze = None
timer = False
