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
		self.s = s

	def renderHover(self):
		pygame.draw.rect(self.s, hues.LIGHT_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderClick(self):
		pygame.draw.rect(self.s, hues.MED_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))
