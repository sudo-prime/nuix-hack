import pygame
import hues
from Tile import Tile
from ColorNode import ColorNode
import copy

class Level:
	def __init__(self, s, cols, rows, tileSize, screenWidth, screenHeight, colornodes, mixers, exitpoints):
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

		self.tiles =    self.dict2D(self.cols, self.rows)
		self.tileSpan = self.dict2D(self.cols, self.rows)

		self.colornodes = colornodes
		self.mixers = mixers
		self.exitpoints = exitpoints

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

		for info in self.colornodes:
			self.tiles[info["col"]][info["row"]].colorNodeHue = info["hue"]
			self.tiles[info["col"]][info["row"]].isColorNode = True
			self.tiles[info["col"]][info["row"]].entryPoint = self.tiles[info["col"]][info["row"]]

		for mixer in self.mixers:
			self.tiles[mixer[0]][mixer[1]].mixer = True

		for info in self.exitpoints:
			self.tiles[info["col"]][info["row"]].exitPointHue = info["hue"]
			self.tiles[info["col"]][info["row"]].isExitPoint = True
			self.tiles[info["col"]][info["row"]].occupied = False
			self.tiles[info["col"]][info["row"]].solved = False

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


	def getTileByCoord(self, mousePos):
		# Pass in x and y of mos pos, get tile obj under it
		for y in range(-1, self.rows + 1):
			for x in range(-1, self.cols + 1):
				if self.tileSpan[x][y].collidepoint(mousePos):
					return self.tiles[x][y]

		return None

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

	def renderLevelComplete(self):
		# TODO: make something other than console message
		print("Level Solved!")

	def refreshEntryPoints(self):
		for x in range(-1, len(self.tiles)-1):
			for y in range(-1, len(self.tiles[x])-1):
				if self.tiles[x][y].mixer and len(self.tiles[x][y].connectingColors) > 0:
					newColor = hues.average(self.tiles[x][y].connectingColors)

					if self.tiles[x][y-1].entryPoint is None:
						self.tiles[x][y].colorNodeHue = newColor
						self.tiles[x][y].isColorNode = True
						self.tiles[x][y].entryPoint = self.tiles[x][y]
						self.colornodes.append({"hue": newColor, "col": x, "row": y})
					# if y + 1 > self.rows:
					# 	print 2
					# 	if not self.tiles[x][y+1].occupied and self.tiles[x][y+1].entryPoint is None:
					# 		self.tiles[x][y].colorNodeHue = newColor
					# 		self.tiles[x][y].isColorNode = True
					# 		self.tiles[x][y].entryPoint = self.tiles[x][y]
					# 		self.colornodes.append({"hue": newColor, "col": x, "row": y})
					# if x - 1 <= 0:
					# 	print 3
					# 	if not self.tiles[x-1][y].occupied and self.tiles[x-1][y].entryPoint is None:
					# 		self.tiles[x][y].colorNodeHue = newColor
					# 		self.tiles[x][y].isColorNode = True
					# 		self.tiles[x][y].entryPoint = self.tiles[x][y]
					# 		self.colornodes.append({"hue": newColor, "col": x, "row": y})
					# if x + 1 > self.cols:
					# 	print 4
					# 	if not self.tiles[x+1][y].occupied and self.tiles[x+1][y].entryPoint is None:
					# 		self.tiles[x][y].colorNodeHue = newColor
					# 		self.tiles[x][y].isColorNode = True
					# 		self.tiles[x][y].entryPoint = self.tiles[x][y]
					# 		self.colornodes.append({"hue": newColor, "col": x, "row": y})


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
