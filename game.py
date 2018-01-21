import pygame
import Event
from Level import Level
import hues
import math

width = 1280
height = 720

pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

colornodes = [
	{"hue": hues.RED, "col": -1, "row": 1},
	{"hue": hues.YELLOW, "col": 3, "row": 1}
]

exitpoints = [
	{"hue": pygame.Color(255, 127, 0, 255), "col": 1, "row": -1}
]

level1 = Level(surface, 3, 2, 100, width, height, colornodes, [(1, 1)], exitpoints)

colors = []
connected = []
points = []
firstClick = True
prevTile = None
prevTileRef = None


while running:
	clock.tick(60) # Restricts framerate to 60fps
	surface.fill(hues.WHITE) # Start from white screen

	level1.renderLevelLines()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
			connected = []
			colors = []
			color = None
			points = []
			prevTile = None
			prevTileRef = None
			firstClick = True
			colornodes = [
				{"hue": hues.RED, "col": -1, "row": 1},
				{"hue": hues.YELLOW, "col": 3, "row": 1}
			]
			exitpoints = [
				{"hue": pygame.Color(255, 127, 0, 255), "col": 1, "row": -1}
			]
			level1 = Level(surface, 3, 2, 100, width, height, colornodes, [(1, 1)], exitpoints)

	tileUnderMouse = level1.getTileByCoord(pygame.mouse.get_pos())

	# DEBUG
	# for x in range(-1, len(level1.tiles)-1):
	# 	for y in range(-1, len(level1.tiles[x])-1):
	# 		if level1.tiles[x][y].entryPoint is not None:
	# 			level1.tiles[x][y].renderDebugSquare()

	# For rendering debug square on occupied tiles
	# for x in range(-1, len(level1.tiles)-1):
	# 	for y in range(-1, len(level1.tiles[x])-1):
	# 		if level1.tiles[x][y].occupied:
	# 			level1.tiles[x][y].renderDebugSquare()

	# Tile hover color ch

	if tileUnderMouse is not None: #if tile under mouse exists
		tileUnderMouse.renderHover()
		# Tile being clicked color change
		if pygame.mouse.get_pressed()[0]: #if mouse is being held
			tileUnderMouse.renderClick()

			if tileUnderMouse.entryPoint is not None: #if tile under mouse is an entry point

				if firstClick: #if it's the first time clicking the entry point
					firstClick = False
					prevTileRef = tileUnderMouse
					points.append(((level1.x + level1.tileSize * tileUnderMouse.entryPoint.col) + level1.tileSize / 2,
								   (level1.y + level1.tileSize * tileUnderMouse.entryPoint.row) + level1.tileSize / 2))
					color = tileUnderMouse.entryPoint.colorNodeHue
					print color

			newTile = tileUnderMouse

			if newTile is not prevTile:
				prevTile = newTile
				if points:
					if level1.getTileByCoord(points[0]).entryPoint is not None:
						if tileUnderMouse.middle not in points:
							if (prevTileRef.col - 1) in level1.tiles:
								leftTile = level1.tiles[prevTileRef.col - 1][prevTileRef.row]
							else:
								leftTile = 0

							if (prevTileRef.col + 1) in level1.tiles:
								rightTile = level1.tiles[prevTileRef.col + 1][prevTileRef.row]
							else:
								rightTile = 0

							if (prevTileRef.row - 1) in level1.tiles[prevTileRef.col]:
								upTile = level1.tiles[prevTileRef.col][prevTileRef.row - 1]
							else:
								upTile = 0

							if (prevTileRef.row + 1) in level1.tiles[prevTileRef.col]:
								downTile = level1.tiles[prevTileRef.col][prevTileRef.row + 1]
							else:
								downTile = 0

							if ((newTile is leftTile)
							 or (newTile is rightTile)
							 or (newTile is upTile)
							 or (newTile is downTile)):
							 	if (not newTile.occupied) or (newTile.mixer):
									prevTile = newTile
									prevTileRef = newTile
									points.append(((level1.x + level1.tileSize * tileUnderMouse.col) + level1.tileSize / 2,
				   								   (level1.y + level1.tileSize * tileUnderMouse.row) + level1.tileSize / 2))
									firstClick = False

			if len(points) > 1:
				pygame.draw.lines(surface, color, False, points, 6)
				for point in points:
					pygame.draw.rect(surface, color, pygame.Rect(point[0]-2, point[1]-2, 6, 6))

		else:
			if points:
				# If final point in list is valid sticking point,
				# append points to connected to draw them indefinitely
				if (level1.getTileByCoord(pygame.mouse.get_pos()).mixer
				or (level1.getTileByCoord(pygame.mouse.get_pos()).isExitPoint
				and level1.getTileByCoord(pygame.mouse.get_pos()).exitPointHue == level1.getTileByCoord(points[0]).colorNodeHue)):
					if level1.getTileByCoord(pygame.mouse.get_pos()) is level1.getTileByCoord(points[-1]):
						# only if the middle point of mixer is in points should connection happen
						if tileUnderMouse.middle in points:
							if len(points) > 1:
								for point in points:
									level1.getTileByCoord(point).occupied = True
								connected.append(points)
								colors.append(color)
								level1.getTileByCoord(pygame.mouse.get_pos()).connectingColors.append(color)
								level1.refreshEntryPoints()

			points = []
			firstClick = True
			prevTile = None
			diagonal = False

	if connected:
		i = 0
		for connection in connected:
			pygame.draw.lines(surface, colors[i], False, connection, 6)
			for point in connection:
				pygame.draw.rect(surface, colors[i], pygame.Rect(point[0]-2, point[1]-2, 6, 6))
			i += 1

	level1.renderColorNodes()
	level1.renderMixers()
	level1.renderExitPoints()

	pygame.display.flip()
