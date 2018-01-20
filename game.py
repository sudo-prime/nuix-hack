import pygame
import Event
from Level import Level
import hues

width = 1280
height = 720

pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

level1 = Level(surface, 4, 4, 100, width, height)

while running:
	clock.tick(60)
	surface.fill(hues.WHITE)

	for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	                running = False

	level1.render()
	tileUnderMouse = level1.getTileByCoord(pygame.mouse.get_pos())

	# Tile hover color change
	if tileUnderMouse is not None:
		level1.getTileByCoord(pygame.mouse.get_pos()).renderHover()
		# Tile being clicked color change
		if pygame.mouse.get_pressed()[0]:
			level1.getTileByCoord(pygame.mouse.get_pos()).renderClick()

	pygame.display.flip()
