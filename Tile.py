import pygame
import hues
import Event

class Tile:
	def __init__(self, x, y, col, row, s, size):
		self.x = x
		self.y = y
		self.col = col
		self.row = row
		self.size = size

		pygame.draw.rect(s, hues.GRAY, pygame.Rect(x + 10, y + 10, size - 20, size - 20))
