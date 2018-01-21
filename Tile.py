import pygame
import hues
import Event
from pygame import gfxdraw

class Tile:
	def __init__(self, x, y, col, row, s, size):
		self.x = x
		self.y = y
		self.col = col
		self.row = row
		self.size = size
		self.middle = (self.x + self.size / 2, self.y + self.size / 2)
		self.s = s
		self.occupied = False
		self.entryPoint = None
		self.isExitPoint = False
		self.mixer = False
		self.mixerColor = hues.GRAY
		self.colorNodeHue = None
		self.exitPointHue = None
		self.connectingColors = []
		self.isColorNode = False

	def renderDebugSquare(self):
		pygame.draw.rect(self.s, hues.BLACK, pygame.Rect(self.x + 10, self.y + 10, self.size - 20, self.size - 20))

	def renderHover(self):
		pygame.draw.rect(self.s, hues.LIGHT_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderClick(self):
		pygame.draw.rect(self.s, hues.CLICK_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderColorNode(self):
		if self.isColorNode:
			pygame.draw.rect(self.s, self.colorNodeHue, pygame.Rect(self.x + 37, self.y + 37, self.size - 72, self.size - 72))

	def renderMixer(self):
		# Re-calculate mixercolor depending on connectingColors
		self.mixerColor = hues.average(self.connectingColors)
		# Draw mixer node, if the tile has one!
		if self.mixer:
			pygame.draw.rect(self.s, self.mixerColor, pygame.Rect(self.x + 37, self.y + 37, self.size - 72, self.size - 72))
			pygame.draw.line(self.s, hues.WHITE, (self.middle[0], self.middle[1] - 9), (self.middle[0], self.middle[1] + 10), 6)
			pygame.draw.line(self.s, hues.WHITE, (self.middle[0] - 9, self.middle[1]), (self.middle[0] + 10, self.middle[1]), 6)

	def renderExitPoint(self):
		pygame.draw.rect(self.s, self.exitPointHue, pygame.Rect(self.x + 37, self.y + 37, self.size - 72, self.size - 72))
