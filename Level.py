import pygame
from pygame import gfxdraw
import hues
from Tile import Tile

class Level:
	def __init__(self, s, cols, rows, tileSize, screenWidth, screenHeight, colornodes, mixers):
		# Here's where I will get level dimensions and starting points / hues
		self.cols = cols
		self.rows = rows

		self.width  = cols * tileSize
		self.height = rows * tileSize

		self.tileSize = tileSize

		self.x = screenWidth/2  - self.width/2
		self.y = screenHeight/2 - self.height/2

		self.s = s

		self.lineOff = 30
		self.lineWidth = 1

		self.tiles =    [[0 for y in range(rows)] for x in range(cols)]
		self.tileSpan = [[0 for y in range(rows)] for x in range(cols)]

		self.colornodes = colornodes
		self.mixers = mixers

		print(str(len(self.tiles[0])) + "," + str(len(self.tiles)))


		for y in range(0, self.rows):
			for x in range(0, self.cols):
				self.tiles[x][y] = Tile(self.x + self.tileSize * x,
				 						self.y + self.tileSize * y,
										x, y, s, self.tileSize)

				self.tileSpan[x][y] = pygame.Rect(self.tiles[x][y].x,
												  self.tiles[x][y].y,
												  self.tileSize,
								  				  self.tileSize)


	def render(self):
		# Here's where pygame graphics will be drawn, and level will start

		# First, populate a matrix of Tile objects
		for col in range(0, self.cols + 1):
			pygame.draw.line(self.s,
							 hues.GRAY,
			 				(self.x + self.tileSize * col, self.y - self.lineOff),
			 				(self.x + self.tileSize * col, self.y + self.height + self.lineOff),
							self.lineWidth)

		# Store the area they cover, as well - for use in determining hover
		for row in range(0, self.rows + 1):
			pygame.draw.line(self.s,
			 				 hues.GRAY,
							(self.x - self.lineOff, self.y + self.tileSize * row),
							(self.x + self.width + self.lineOff, self.y + self.tileSize * row),
							 self.lineWidth)

		# Then, render colornodes
		for node in self.colornodes:
			pygame.gfxdraw.filled_circle(self.s,
								   		(self.x + self.tileSize * node.col) + self.tileSize / 2,
										(self.y + self.tileSize * node.row) + self.tileSize / 2,
								   		13, node.hue)

			pygame.gfxdraw.aacircle(self.s,
								   (self.x + self.tileSize * node.col) + self.tileSize / 2,
								   (self.y + self.tileSize * node.row) + self.tileSize / 2,
								   13, node.hue)

			# DONT FORGET TO ADD LINE HERE CONNECTING TO GRID

			# Next, set tiles next to colornodes as entryPoints
			if node.direction == "UP":
				self.tiles[node.col][node.row - 1].entryPoint = node
			elif node.direction == "DOWN":
				self.tiles[node.col][node.row + 1].entryPoint = node
			elif node.direction == "LEFT":
				self.tiles[node.col - 1][node.row].entryPoint = node
			elif node.direction == "RIGHT":
				self.tiles[node.col + 1][node.row].entryPoint = node

			# And render mixer nodes
			for mixer in self.mixers:
				self.tiles[mixer[0]][mixer[1]].mixer = True


	def getTileByCoord(self, mousePos):
		# Pass in x and y of mos pos, get tile obj under it
		for y in range(0, self.rows):
			for x in range(0, self.cols):
				if self.tileSpan[x][y].collidepoint(mousePos):
					return self.tiles[x][y]

		return None

	def renderMixers(self):
		# Use list of mixer tiles to draw their graphics
		for mixer in self.mixers:
			self.tiles[mixer[0]][mixer[1]].renderMixer()
