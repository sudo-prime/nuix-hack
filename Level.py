import pygame
import hues
from Tile import Tile

class Level:
	def __init__(self, s, cols, rows, tileSize, screenWidth, screenHeight):
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

		self.tiles = [[0 for y in range(rows)] for x in range(cols)]
		self.tileSpan = [[0 for y in range(rows)] for x in range(cols)]

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
		for col in range(0, self.cols + 1):
			pygame.draw.line(self.s,
							 hues.GRAY,
			 				(self.x + self.tileSize * col, self.y - self.lineOff),
			 				(self.x + self.tileSize * col, self.y + self.height + self.lineOff),
							self.lineWidth)

		for row in range(0, self.rows + 1):
			pygame.draw.line(self.s,
			 				 hues.GRAY,
							(self.x - self.lineOff, self.y + self.tileSize * row),
							(self.x + self.width + self.lineOff, self.y + self.tileSize * row),
							 self.lineWidth)

	def getTileByCoord(self, mousePos):
		# Pass in x and y of mos pos, get tile obj under it
		for y in range(0, self.rows):
			for x in range(0, self.cols):
				if self.tileSpan[x][y].collidepoint(mousePos):
					return self.tiles[x][y]

		return None
