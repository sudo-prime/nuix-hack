import pygame
import Event
import Level
import hues

width = 1280
height = 720

pygame.init()
surface = pygame.display.set_mode((width, height))
running = True

pygame.Surface.fill(surface, hues.WHITE)
level1 = Level.Level(surface, 3, 3, 100, width, height)
level1.begin()

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        pygame.display.flip()
