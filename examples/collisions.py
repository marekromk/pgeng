import pygame, pgeng
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
Screen = pgeng.Screen((320, 240), vsync=0)
display = Screen.get_display()
small_font = pgeng.create_font((255, 255, 255))[0]

original_points = [(150, 180), (170, 180), (160, 200)]
original_center = [160, 180]

poly = pgeng.Polygon([(150, 180), (170, 180), (160, 200)], (255, 0, 0))
poly2 = pgeng.Polygon([(40, 40), (120, 40), (80, 100), (80, 50)], (0, 0, 255))
circle = pgeng.Circle(original_center, 10, (255, 0, 0))
circle2 = pgeng.Circle([160, 80], 10, (0, 0, 255))
rect = Rect(220, 70, 20, 20)
rect_colour = (0, 0, 255)

rotate_timer = 100
poly_mode = True
show_mask = False
while True:
    display.fill((50, 50, 50))
    dt = pgeng.delta_time(clock, 144)

    keys = pygame.key.get_pressed()
    if keys[K_a]:
        poly.move([-1.5, 0], dt) if poly_mode else None
        circle.center[0] -= 1.5 * dt if not poly_mode else 0
    if keys[K_d]:
        poly.move([1.5, 0], dt) if poly_mode else None
        circle.center[0] += 1.5 * dt if not poly_mode else 0
    if keys[K_s]:
        poly.move([0, 1.5], dt) if poly_mode else None
        circle.center[1] += 1.5 * dt if not poly_mode else 0
    if keys[K_w]:
        poly.move([0, -1.5], dt) if poly_mode else None
        circle.center[1] -= 1.5 * dt if not poly_mode else 0

    colliding = False
    if poly_mode:
        if poly.collide(poly2):
            colliding = True
            poly2.colour = (255, 0, 0)
        elif poly.colliderect(rect):
            colliding = True
            rect_colour = (255, 0, 0)
        elif poly.collidecircle(circle2):
            colliding = True
            circle2.colour = (255, 0, 0)
        else: #so if it is not colliding with anything
            poly2.colour = (0, 0, 255)
            rect_colour = (0, 0, 255)
            circle2.colour = (0, 0, 255)
    else:
        if circle.collide(circle2):
            colliding = True
            circle2.colour = (255, 0, 0)
        elif circle.colliderect(rect):
            colliding = True
            rect_colour = (255, 0, 0)
        elif circle.collidepolygon(poly2):
            colliding = True
            poly2.colour = (255, 0, 0)
        else: #so if it is not colliding with anything
            circle2.colour = (0, 0, 255)
            rect_colour = (0, 0, 255)
            poly2.colour = (0, 0, 255)
    rect_colour = (255, 255, 255) if show_mask else rect_colour

    rotate_timer += 0.5 * dt
    if round(rotate_timer) <= 90:
        poly.rotate(0.5 * dt)
    elif poly.rotation % 90:
        poly.rotate(pgeng.nearest(poly.rotation, 90) - poly.rotation)

    poly2.render(display)
    circle2.render(display)
    pygame.draw.rect(display, rect_colour, rect)
    poly.render(display) if poly_mode else circle.render(display)
    if show_mask:
        display.blit(poly2.mask.to_surface(), poly2.location)
        display.blit(circle2.mask.to_surface(), circle2.location)
        display.blit(poly.mask.to_surface(), poly.location) if poly_mode else display.blit(circle.mask.to_surface(), circle.location)

    for event in pygame.event.get():
        if event.type == QUIT:
            pgeng.quit_game()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pgeng.quit_game()
            if event.key == K_SPACE:
                poly_mode = not poly_mode
                poly.set_points(original_points)
                circle.center = pygame.Vector2(original_center)
            if event.key == K_RETURN:
                show_mask = not show_mask
            if event.key == K_r:
                rotate_timer = 0 if poly_mode else 91

    small_font.render(display, f'{round(clock.get_fps())}', (1, 1))
    pygame.display.update()
    clock.tick(144)