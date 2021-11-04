import pygame, pgeng
from random import uniform, randint
from pygame.locals import *

pygame.init()

display_size = (500, 500)
screen = pgeng.Screen(display_size, vsync=0)
display = screen.get_display()
clock = pygame.time.Clock()
large_font = pgeng.create_font((255, 255, 255))[1]

scroll = pygame.Vector2()
flames = [pgeng.Flame((250, 400), 6, 0.07, (255, 0, 0), 4)]

while True:
    display.fill((0, 0, 0))
    dt = pgeng.delta_time(clock, 60)

    keys = pygame.key.get_pressed()
    if keys[K_w]:
        scroll.y -= 5 * dt
    if keys[K_s]:
        scroll.y += 5 * dt
    if keys[K_a]:
        scroll.x -= 5 * dt
    if keys[K_d]:
        scroll.x += 5 * dt

    rendering = 0
    for flame in flames:
        if any([0 <= p.location.x - scroll.x <= display_size[0] and 0 <= p.location.y - scroll.y <= display_size[1] for p in flame.particles]):
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
        if event.type == MOUSEBUTTONDOWN:
            flames.append(pgeng.Flame(pygame.mouse.get_pos() + scroll, uniform(4, 6), uniform(0.025, 0.1), (randint(200, 255), randint(0, 50), randint(0, 200)), randint(2, 5)))
    large_font.render(display, f'{round(clock.get_fps())}\nflames: {len(flames)}\nrendering: {rendering})', (1, 1))

    pygame.display.update()
    clock.tick(144)