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
		self.middle = (self.x + self.size / 2, self.y + self.size / 2)
		self.s = s
		self.occupied = False
		self.entryPoint = None
		self.exitPoint = None
		self.mixer = False
		self.mixerColor = hues.GRAY
		self.connectingColors = []

	def renderDebugSquare(self):
		pygame.draw.rect(self.s, hues.BLACK, pygame.Rect(self.x + 10, self.y + 10, self.size - 20, self.size - 20))

	def renderHover(self):
		pygame.draw.rect(self.s, hues.LIGHT_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderClick(self):
		pygame.draw.rect(self.s, hues.MED_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderMixer(self):
		# Re-calculate mixercolor demending on connectingColors
		self.mixerColor = hues.average(self.connectingColors)
		# Draw mixer node, if the tile has one!
		if self.mixer:
			pygame.gfxdraw.filled_circle(self.s,
										 self.x + self.size / 2,
										 self.y + self.size / 2, 13, self.mixerColor)
