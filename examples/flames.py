import pygame, pgeng
from random import uniform, randint
from pygame.locals import *

pygame.init()

display_size = (500, 500)
screen = pgeng.Screen(display_size, vsync=0)
display = screen.get_display()
clock = pygame.time.Clock()
large_font = pgeng.create_font((255, 255, 255))[1]

scroll = [0, 0]
directions = {direction: False for direction in ['up', 'down', 'left', 'right']}

flames = [pgeng.Flame((250, 400), 6, 0.07, (255, 0, 0), 4)]

while True:
    display.fill((0, 0, 0))
    dt = pgeng.delta_time(clock, 60)
    if directions['up']:
        scroll[1] -= 5 * dt
    if directions['down']:
        scroll[1] += 5 * dt
    if directions['left']:
        scroll[0] -= 5 * dt
    if directions['right']:
        scroll[0] += 5 * dt

    rendering = 0
    for flame in flames:
        if any([0 <= p.location[0] - scroll[0] <= display_size[0] and 0 <= p.location[1] - scroll[1] <= display_size[1] for p in flame.particles]):
            flame.render(display, -4, scroll, dt)
            rendering += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            pgeng.quit_game()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pgeng.quit_game()
            if event.key == K_F11:
                screen.toggle_fullscreen()
            if event.key == K_w:
                directions['up'] = True
            if event.key == K_s:
                directions['down'] = True
            if event.key == K_a:
                directions['left'] = True
            if event.key == K_d:
                directions['right'] = True
        if event.type == KEYUP:
            if event.key == K_w:
                directions['up'] = False
            if event.key == K_s:
                directions['down'] = False
            if event.key == K_a:
                directions['left'] = False
            if event.key == K_d:
                directions['right'] = False
        if event.type == MOUSEBUTTONDOWN:
            flames.append(pgeng.Flame([pygame.mouse.get_pos()[i] + scroll[i] for i in range(2)], uniform(4, 6), uniform(0.025, 0.1), (randint(200, 255), randint(0, 50), randint(0, 200)), randint(2, 5)))
    large_font.render(display, f'{round(clock.get_fps())}\nflames: {len(flames)}\nrendering: {rendering})', (1, 1))

    pygame.display.update()
    clock.tick(144)