import pygame, pgeng
from pygame.locals import *

pygame.init()
pgeng.tile_size = 20

screen = pgeng.Screen((320, 240), vsync=0)
display = screen.get_display()
clock = pygame.time.Clock()

spawn = pygame.Vector2(150, 165)
entity = pgeng.Entity(spawn, (20, 25))

scroll_change = [(screen.size[i] + entity.rect.size[i]) * 0.5 for i in range(2)] #this makes it so the camera sets the player to the center of the screen, not the top left corner
scroll = entity.center - scroll_change

jumping = False
y_momentum = 0
air_timer = 0

tiles = []
for i in range(60, 260, 20):
	tiles.append(pgeng.Tile((i, 190), pgeng.tile_size))

for i in range(-40, 41, 20):
	tiles.append(pgeng.Tile((i, 130), pgeng.tile_size))
	tiles.append(pgeng.Tile((i + 300, 130), pgeng.tile_size))

while True:
	display.fill((25, 25, 25))
	dt = pgeng.delta_time(clock, 144)

	scroll.x += (entity.center.x - scroll.x - scroll_change[0]) / 20 * dt
	scroll.y += (entity.center.y - scroll.y - scroll_change[1]) / 20 * dt

	keys = pygame.key.get_pressed()
	x_momentum = 0
	if keys[K_d]:
		x_momentum += 1.25 * dt
	if keys[K_a]:
		x_momentum -= 1.25 * dt

	for tile in tiles:
		pygame.draw.rect(display, (255, 255, 255), Rect(tile.location - scroll, tile.size), 2, 3)

	y_momentum += 0.1 * dt
	if entity.center.y > 300:
		entity.location = spawn
	collisions = entity.movement(pygame.Vector2(x_momentum, y_momentum * dt), tiles)
	if collisions['bottom']:
		y_momentum = 0
		air_timer = 0
		jumping = False
	else:
		air_timer += dt
	if collisions['top']:
		y_momentum = 0

	pygame.draw.rect(display, (255, 0, 0), Rect(entity.rect.topleft - scroll, entity.rect.size))

	for event in pygame.event.get():
		if event.type == QUIT:
			pgeng.quit_game()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pgeng.quit_game()
			if event.key == K_w and air_timer < 15 and not jumping:
				y_momentum = -4
				jumping = True

	pygame.display.update()
	clock.tick(144)