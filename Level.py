import pygame
import hues
from Tile import Tile
from ColorNode import ColorNode
import copy

class Level:
	def __init__(self, s, cols, rows, tileSize, screenWidth, screenHeight, colornodes, mixers, exitpoints, obstacles, subtractors):
		# Here's where I will get level dimensions and starting points / hues
		self.cols = cols
		self.rows = rows

		self.width  = cols * tileSize
		self.height = rows * tileSize

		self.tileSize = tileSize

		self.x = screenWidth/2  - self.width/2
		self.y = (screenHeight/2 - self.height/2) - 50

		self.s = s

		self.lineOff = 30
		self.lineWidth = 1

		self.tiles =    self.dict2D(self.cols, self.rows)
		self.tileSpan = self.dict2D(self.cols, self.rows)

		self.colornodes = colornodes
		self.mixers = mixers
		self.exitpoints = exitpoints
		self.obstacles = obstacles
		self.subtractors = subtractors

		self.complete = False

		for y in range(-1, self.rows + 1):
			for x in range(-1, self.cols + 1):
				self.tiles[x][y] = Tile(self.x + self.tileSize * x,
				 						self.y + self.tileSize * y,
										x, y, s, self.tileSize)

				self.tileSpan[x][y] = pygame.Rect(self.tiles[x][y].x,
												  self.tiles[x][y].y,
												  self.tileSize,
								  				  self.tileSize)

				if (x == -1) or (y == -1) or (x == self.cols) or (y == self.rows):
					# Initialize tile as an outside tile
					self.tiles[x][y].occupied = True

		if self.colornodes:
			for info in self.colornodes:
				self.tiles[info["col"]][info["row"]].color = info["hue"]
				self.tiles[info["col"]][info["row"]].colornode = True
				self.tiles[info["col"]][info["row"]].entryPoint = self.tiles[info["col"]][info["row"]]

		if self.mixers:
			for mixer in self.mixers:
				self.tiles[mixer[0]][mixer[1]].mixer = True

		if self.exitpoints:
			for info in self.exitpoints:
				self.tiles[info["col"]][info["row"]].color = info["hue"]
				self.tiles[info["col"]][info["row"]].exitpoint = True
				self.tiles[info["col"]][info["row"]].occupied = False
				self.tiles[info["col"]][info["row"]].solved = False

		if self.obstacles:
			for obstacle in self.obstacles:
				self.tiles[obstacle[0]][obstacle[1]].occupied = True

		if self.subtractors:
			for sub in self.subtractors:
				self.tiles[sub[0]][sub[1]].subtractor = True

	def renderColorNodes(self):
		for info in self.colornodes:
			# Render colornode circles
			self.tiles[info["col"]][info["row"]].renderColorNode()

	def renderMixers(self):
		# And render mixer nodes
		for mixer in self.mixers:
			self.tiles[mixer[0]][mixer[1]].renderMixer()

	def renderExitPoints(self):
		for info in self.exitpoints:
			self.tiles[info["col"]][info["row"]].renderExitPoint()

	def renderObstacles(self):
		for obstacle in self.obstacles:
			self.tiles[obstacle[0]][obstacle[1]].renderObstacle()

	def renderSubtractors(self):
		for sub in self.subtractors:
			self.tiles[sub[0]][sub[1]].renderSubtractor()

	def getTileByCoord(self, mousePos):
		# Pass in x and y of mos pos, get tile obj under it
		for y in range(-1, self.rows + 1):
			for x in range(-1, self.cols + 1):
				if self.tileSpan[x][y].collidepoint(mousePos):
					return self.tiles[x][y]
		return None

	def convertTileToColorNode(self, tile):
		tile.convertToColorNode()

	def convertTileToMixer(self, tile):
		tile.convertToMixer()

	def renderLevelLines(self):
		for col in range(0, self.cols + 1):
			pygame.draw.line(self.s,
							 hues.MED_GRAY,
			 				(self.x + self.tileSize * col, self.y - self.lineOff),
			 				(self.x + self.tileSize * col, self.y + self.height + self.lineOff),
							self.lineWidth)

		# Store the area they cover, as well - for use in determining hover
		for row in range(0, self.rows + 1):
			pygame.draw.line(self.s,
			 				 hues.MED_GRAY,
							(self.x - self.lineOff, self.y + self.tileSize * row),
							(self.x + self.width + self.lineOff, self.y + self.tileSize * row),
							 self.lineWidth)

	def refreshEntryPoints(self):
		for mixer in self.mixers:
			if len(self.tiles[mixer[0]][mixer[1]].connectingColors) == 1:
				if self.tiles[mixer[0]][mixer[1]].entryPoint is None:
					initialColor = hues.average(self.tiles[mixer[0]][mixer[1]].connectingColors)
					self.tiles[mixer[0]][mixer[1]].entryPoint = self.tiles[mixer[0]][mixer[1]]
					self.colornodes.append({"hue": initialColor, "col": mixer[0], "row": mixer[1]})

		for sub in self.subtractors:
			if len(self.tiles[sub[0]][sub[1]].connectingColors) == 2:
				if self.tiles[sub[0]][sub[1]].entryPoint is None:
					initialColor = hues.subtract(self.tiles[sub[0]][sub[1]].connectingColors)
					self.tiles[sub[0]][sub[1]].entryPoint = self.tiles[sub[0]][sub[1]]
					self.colornodes.append({"hue": initialColor, "col": sub[0], "row": sub[1]})

	def dict2D(self, cols, rows):
		d = dict()
		for x in range(-1, cols + 1):
			d[x] = dict()
			for y in range(-1, rows + 1):
				d[x][y] = 0
		return d

	def levelIsSolved(self):
		for exitpoint in self.exitpoints:
			if exitpoint["solved"] == False:
				return False

		return True
