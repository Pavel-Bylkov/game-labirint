from Source.game_classes import *

# ToDo Исправить отнимание жизней - давать три секунды убежать, все враги в заморозке.
# Todo Добавить условия победы
# Todo Добавить телепорты по углам карты
# Todo Элексир суперсилы - на короткое время.
# Todo Загрузить музыку для фона, и эффектов - поймал охранник, собрал предмет, Геймовер и Победа


def add_elixir(timer):
    from random import randint
    mode = randint(1, 3)
    skins = ("", "freeze.png", "yellow.png", "red.png")
    temp_el = Elexir(img=skins[mode], x=randint(10, win_width//5 - 10) * 5,
                     y=randint(10, win_height//5 - 10) * 5, size_x=40, size_y=40, mode=mode, timer=timer)
    while (pg.sprite.spritecollide(temp_el, walls, dokill=False) or
            pg.sprite.collide_rect(temp_el, hero)):
        temp_el.rect.x = randint(10, win_width//5 - 10) * 5
        temp_el.rect.y = randint(10, win_height//5 - 10) * 5
    elixirs.add(temp_el)



hero = Player(img="шар.png", x=45, y=45, size_x=50, size_y=50, speed=10)
guards = pg.sprite.Group()
guards.add(
    Guard(img="шар.png", x=win_width - 100, y=win_height//2, size_x=50, size_y=50, speed=4),
    Guard(img="шар.png", x=win_width//2, y=win_height//2, size_x=50, size_y=50, speed=4)
)
aurum = GameSprite(img="treasure.png", x=win_width - 100, y=win_height - 100,
                   size_x=60, size_y=60, speed=10)
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

control_timer = ControlTimer()
elixirs = pg.sprite.Group()

last_time_el = time()

run = True
finish = False
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # обновляем координаты и накладываем на экранную поверхность фон и всех спрайтов
    # window.blit(background, (0, 0))  # копирование изображения на экранную поверхность
    if not finish:
        window.fill(GREEN)
        hero.update(walls, guards)
        guards.update(hero, walls, control_timer)
        elixirs.update(hero, elixirs)
        control_timer.update(window)

        aurum.reset()
        guards.draw(window)
        walls.draw(window)  # вызываем групповой метод копирования изображения каждой стены на экранную поверхность
        setka.draw(window)
        elixirs.draw(window)
        hero.reset(window)

        if time() - last_time_el > 10:
            add_elixir(control_timer)
            last_time_el = time()

        if hero.life <= 0:
            finish = True
            window.blit(lose, (win_width//2 - 300, win_height//2 - 60))

    pg.display.update()
    clock.tick(FPS)



