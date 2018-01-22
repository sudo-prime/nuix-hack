import pygame
import hues

class Button:
	def __init__(self, s, x, y, width, height, levelNum):
		self.s = s
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.levelNum = levelNum

	def levelDirect(self):
		return self.levelNum

	def render(self):
		pygame.draw.rect(self.s, hues.LIGHT_GRAY, pygame.Rect(self.x, self.y, self.width, self.height))

	def renderClick(self):
		pygame.draw.rect(self.s, hues.GRAY, pygame.Rect(self.x, self.y, self.width, self.height))

	def renderHover(self):
		pygame.draw.rect(self.s, hues.CLICK_GRAY, pygame.Rect(self.x, self.y, self.width, self.height))
