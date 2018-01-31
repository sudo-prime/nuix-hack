import pygame

class Hue(pygame.Color):
	def __init__(self, r, g, b, mixes):
		super(pygame.Color, self).__init__(r, g, b)
		self.set_length(3)
		self.mixes = mixes
