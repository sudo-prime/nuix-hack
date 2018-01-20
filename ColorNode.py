import hues
import Tile

class ColorNode():
	def __init__(self, hue, direction, row, col):
		self.hue = hue
		self.direction = direction
		self.row = row
		self.col = col
