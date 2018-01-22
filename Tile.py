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
		self.solved = None

	def printTileInfo(self):
		print self.mixer
		print self.isColorNode
		print self.entryPoint
		print self.colorNodeHue
		print self.solved
		print self.exitPointHue
		print self.connectingColors
		print self.mixerColor

	def renderObstacle(self):
		pygame.draw.rect(self.s, hues.MED_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderDebugSquare(self):
		pygame.draw.rect(self.s, hues.BLACK, pygame.Rect(self.x + 10, self.y + 10, self.size - 20, self.size - 20))

	def renderHover(self):
		pygame.draw.rect(self.s, hues.LIGHT_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderClick(self):
		pygame.draw.rect(self.s, hues.CLICK_GRAY, pygame.Rect(self.x + 1, self.y + 1, self.size - 1, self.size - 1))

	def renderColorNode(self):
		if self.isColorNode:
			pygame.draw.rect(self.s, self.colorNodeHue, pygame.Rect(self.x + 37, self.y + 37, self.size - 72, self.size - 72))

	def convertToColorNode(self):
		self.mixer = False
		self.isColorNode = True
		self.colorNodeHue = hues.average(self.connectingColors)
		self.mixerColor = hues.GRAY

	def convertToMixer(self):
		self.mixer = True
		self.isColorNode = False
		self.mixerColor = hues.average(self.connectingColors)

	def renderMixer(self):
		# Re-calculate mixercolor depending on connectingColors
		self.mixerColor = hues.average(self.connectingColors)
		# Draw mixer node, if the tile has one!
		if self.mixer:
			pygame.draw.rect(self.s, self.mixerColor, pygame.Rect(self.x + 37, self.y + 37, self.size - 72, self.size - 72))
			pygame.draw.line(self.s, hues.WHITE, (self.middle[0], self.middle[1] - 9), (self.middle[0], self.middle[1] + 10), 6)
			pygame.draw.line(self.s, hues.WHITE, (self.middle[0] - 9, self.middle[1]), (self.middle[0] + 10, self.middle[1]), 6)

	def renderExitPoint(self):
		pygame.draw.rect(self.s, self.exitPointHue, pygame.Rect(self.x + 37, self.y + 37, self.size - 73, self.size - 73), 6)
		pygame.draw.rect(self.s, self.exitPointHue, pygame.Rect(self.x + 35, self.y + 35, 6, 6))
		pygame.draw.rect(self.s, self.exitPointHue, pygame.Rect(self.x + 35, (self.y + 35) + (self.size - 73) - 1, 6, 6))
		pygame.draw.rect(self.s, self.exitPointHue, pygame.Rect((self.x + 35) + (self.size - 73) - 1, self.y + 35, 6, 6))
		pygame.draw.rect(self.s, self.exitPointHue, pygame.Rect((self.x + 35) + (self.size - 73) - 1, (self.y + 35) + (self.size - 73) - 1, 6, 6))
		pygame.draw.rect(self.s, hues.WHITE, pygame.Rect(self.x + 41, self.y + 41, self.size - 80, self.size - 80))
