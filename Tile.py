import pygame
import hues
import Event
from Hue import Hue
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
		self.exitpoint = False
		self.subtractor = False
		self.mixer = False
		self.color = hues.GRAY
		self.outerColor = hues.LIGHT_GRAY
		self.connectingColors = []
		self.colornode = False
		self.solved = None

	def printTileInfo(self):
		print (self.mixer)
		print (self.colornode)
		#print (self.entryPoint)
		print (self.subtractor)
		print (self.color)
		#print (self.solved)
		print (self.connectingColors)

	def renderObstacle(self):
		pygame.draw.rect(self.s, hues.MED_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderDebugSquare(self):
		pygame.draw.rect(self.s, hues.BLACK, pygame.Rect(self.x + 10, self.y + 10, self.size - 20, self.size - 20))

	def renderHover(self):
		pygame.draw.rect(self.s, hues.LIGHT_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderClick(self):
		pygame.draw.rect(self.s, hues.CLICK_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderColorNode(self):
		if self.colornode:
			if self.outerColor is not hues.LIGHT_GRAY:
				pygame.draw.rect(self.s, self.outerColor, pygame.Rect(self.x + 35, self.y + 35, self.size - 68, self.size - 68))
				pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 41, self.y + 41, self.size - 80, self.size - 80))
			if self.outerColor is hues.LIGHT_GRAY:
				pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 37, self.y + 37, self.size - 72, self.size - 72))

	def convertToColorNode(self):
		if self.mixer:
			self.color = hues.average(self.connectingColors)
		elif self.subtractor:
			self.color = hues.subtract(self.connectingColors)
		self.subtractor = False
		self.mixer = False
		self.colornode = True
		self.occupied = True

	def convertToMixer(self):
		self.mixer = True
		self.colornode = False
		self.subtractor = False
		self.occupied = False
		self.color = hues.average(self.connectingColors)

	def renderMixer(self):
		# Re-calculate mixer color depending on connectingColors
		self.color = hues.average(self.connectingColors)
		# Draw mixer node, if the tile has one!
		if self.mixer:
			pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 37, self.y + 37, self.size - 72, self.size - 72))
			pygame.draw.line(self.s, hues.WHITE, (self.middle[0], self.middle[1] - 9), (self.middle[0], self.middle[1] + 10), 6)
			pygame.draw.line(self.s, hues.WHITE, (self.middle[0] - 9, self.middle[1]), (self.middle[0] + 10, self.middle[1]), 6)

	def renderSubtractor(self):
			# Re-calculate subtractor color depending on connectingColors
			self.color = hues.subtract(self.connectingColors)
			# Draw subtractor node, if the tile has one!
			if self.subtractor:
				if self.outerColor is hues.LIGHT_GRAY:
					pygame.draw.rect(self.s, hues.GRAY, pygame.Rect(self.x + 35, self.y + 35, self.size - 68, self.size - 68))
					if self.color is hues.GRAY:
						pygame.draw.rect(self.s, hues.MED_GRAY, pygame.Rect(self.x + 41, self.y + 41, self.size - 80, self.size - 80))
					else:
						pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 41, self.y + 41, self.size - 80, self.size - 80))
				else:
					pygame.draw.rect(self.s, self.outerColor, pygame.Rect(self.x + 35, self.y + 35, self.size - 68, self.size - 68))
					if self.color is hues.GRAY:
						pygame.draw.rect(self.s, hues.MED_GRAY, pygame.Rect(self.x + 41, self.y + 41, self.size - 80, self.size - 80))
					else:
						pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 41, self.y + 41, self.size - 80, self.size - 80))
				pygame.draw.line(self.s, hues.WHITE, (self.middle[0] - 9, self.middle[1]), (self.middle[0] + 10, self.middle[1]), 6)

	def renderExitPoint(self):
		pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 37, self.y + 37, self.size - 73, self.size - 73), 6)
		pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 35, self.y + 35, 6, 6))
		pygame.draw.rect(self.s, self.color, pygame.Rect(self.x + 35, (self.y + 35) + (self.size - 73) - 1, 6, 6))
		pygame.draw.rect(self.s, self.color, pygame.Rect((self.x + 35) + (self.size - 73) - 1, self.y + 35, 6, 6))
		pygame.draw.rect(self.s, self.color, pygame.Rect((self.x + 35) + (self.size - 73) - 1, (self.y + 35) + (self.size - 73) - 1, 6, 6))
		pygame.draw.rect(self.s, hues.WHITE, pygame.Rect(self.x + 41, self.y + 41, self.size - 80, self.size - 80))
