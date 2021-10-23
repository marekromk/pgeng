import pygame, pgeng
from random import uniform, randint
from pygame.locals import *

pygame.init()

screen = pgeng.Screen((640, 480), SCALED | RESIZABLE, vsync=0)
display = screen.get_display()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

sparks = []
shockwaves = []
turn = False
lighting = False
turnnumber = 0.08
haveangle = False
gravity = False

large_font = pgeng.create_font((255, 255, 255))[1]

while True:
    display.fill((100, 100, 100))
    dt = pgeng.delta_time(clock, 60)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if turn and haveangle:
        turnnumber = -0.08
    elif haveangle:
        turnnumber = 0.08
    else:
        turnnumber = 0

    for i in range(7 - lighting * 4):
        sparks.append(pgeng.Spark([mouse_x, mouse_y], randint(0, 360), uniform(3.5, 5), uniform(2, 3.5), (randint(100, 255), 0, randint(0, 100)))) #BLUE COLORS: (randint(0, 255), 255, 255)

    for i, spark in sorted(enumerate(sparks), reverse=True):
        if gravity:
            spark.gravity_movement(0.035, 0.15, 9.1, dt)
        else:
            spark.normal_movement(0.035, dt, turnnumber)
        if lighting:
            spark.render(display, lighting_colour=(255, 0, 0), lighting_flag=BLEND_RGBA_ADD)
        else:
             spark.render(display)
        if not spark.alive:
            sparks.pop(i)

    for i, wave in sorted(enumerate(shockwaves), reverse=True):
        wave.update(display, 1.5, 0.75, delta_time=dt)
        if not wave.alive:
            shockwaves.pop(i)

    for event in pygame.event.get():
        if event.type == QUIT:
            pgeng.quit_game()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pgeng.quit_game()
            if event.key == K_SPACE:
                shockwaves.append(pgeng.ShockWave([mouse_x, mouse_y], 20, 30, (255, 0, randint(171, 255))))
                lighting = not lighting
                if lighting:
                    sparks = []
            if event.key == K_RETURN:
                shockwaves.append(pgeng.ShockWave([mouse_x, mouse_y], 20, 30, (255, 0, randint(86, 170))))
                gravity = not gravity
            if event.key == K_f:
                screen.toggle_fullscreen()
        if event.type == MOUSEBUTTONDOWN:
            shockwaves.append(pgeng.ShockWave([mouse_x, mouse_y], 20, 30, (255, 0, randint(0, 85))))
            if event.button == 3:
                haveangle = not haveangle
            else:
                turn = True
        if event.type == MOUSEBUTTONUP:
            turn = False
    large_font.render(display, f'{round(clock.get_fps())}', (1, 1))
    pygame.display.update()
    clock.tick(144)
