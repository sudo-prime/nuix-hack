import pygame
import Event
from Level import Level
import hues
import math
import copy


width = 1280
height = 720

pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

colors = []
connected = []
points = []
firstClick = True
firstTile = False
prevTile = None
prevTileRef = None
levelNum = 1

colornodes = {
	1: [
		{"hue": hues.RED, "col": -1, "row": 1},
		{"hue": hues.YELLOW, "col": 3, "row": 1}
	]
}

mixers = {
	1: [
		(1, 1)
	]
}

exitpoints = {
	1: [
		{"hue": pygame.Color(255, 255, 0, 255), "col": 1, "row": -1, "solved": False}
	]
}

colornodesCopy = copy.deepcopy(colornodes)
mixersCopy = copy.deepcopy(mixers)
exitpointsCopy = copy.deepcopy(exitpoints)

def updateDefaults(levelNum):
	colornodesCopy = copy.deepcopy(colornodes)
	mixersCopy = copy.deepcopy(mixers)
	exitpointsCopy = copy.deepcopy(exitpoints)

	levelList = {
		1: Level(surface, 3, 2, 100, width, height, colornodesCopy[1], mixersCopy[1], exitpointsCopy[1])
	}
	return levelList[levelNum]

level = updateDefaults(1)

while running:
	clock.tick(60) # Restricts framerate to 60fps
	surface.fill(hues.WHITE) # Start from white screen

	level.renderLevelLines()

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
			level = updateDefaults(1)

	tileUnderMouse = level.getTileByCoord(pygame.mouse.get_pos())

	# DEBUG
	# Renders debug squares over entry points
	# for x in range(-1, len(level.tiles)-1):
	# 	for y in range(-1, len(level.tiles[x])-1):
	# 		if level.tiles[x][y].entryPoint is not None:
	# 			level.tiles[x][y].renderDebugSquare()

	# For rendering debug square on occupied tiles
	# for x in range(-1, len(level.tiles)-1):
	# 	for y in range(-1, len(level.tiles[x])-1):
	# 		if level.tiles[x][y].occupied:
	# 			level.tiles[x][y].renderDebugSquare()

	# For rendering debug square on solved tiles
	# for x in range(-1, len(level.tiles)-1):
	# 	for y in range(-1, len(level.tiles[x])-1):
	# 		if level.tiles[x][y].solved:
	# 			level.tiles[x][y].renderDebugSquare()

	if tileUnderMouse is not None: #if tile under mouse exists
		tileUnderMouse.renderHover()
		# Tile being clicked color change
		if pygame.mouse.get_pressed()[0]: #if mouse is being held
			tileUnderMouse.renderClick()
			if tileUnderMouse.entryPoint is not None: #if tile under mouse is an entry point
				if firstClick: #if it's the first time clicking the entry point
					firstClick = False
					prevTileRef = tileUnderMouse
					points.append(((level.x + level.tileSize * tileUnderMouse.entryPoint.col) + level.tileSize / 2,
								   (level.y + level.tileSize * tileUnderMouse.entryPoint.row) + level.tileSize / 2))
					color = tileUnderMouse.entryPoint.colorNodeHue

			newTile = tileUnderMouse

			if len(points) <= 1:
				firstTile = True
			else:
				firstTile = False

			if newTile is not prevTile:
				prevTile = newTile
				if points:
					if level.getTileByCoord(points[0]).entryPoint is not None:
						if tileUnderMouse.middle not in points:
							if (prevTileRef.col - 1) in level.tiles:
								leftTile = level.tiles[prevTileRef.col - 1][prevTileRef.row]
							else:
								leftTile = 0

							if (prevTileRef.col + 1) in level.tiles:
								rightTile = level.tiles[prevTileRef.col + 1][prevTileRef.row]
							else:
								rightTile = 0

							if (prevTileRef.row - 1) in level.tiles[prevTileRef.col]:
								upTile = level.tiles[prevTileRef.col][prevTileRef.row - 1]
							else:
								upTile = 0

							if (prevTileRef.row + 1) in level.tiles[prevTileRef.col]:
								downTile = level.tiles[prevTileRef.col][prevTileRef.row + 1]
							else:
								downTile = 0

							if ((newTile is leftTile)
							 or (newTile is rightTile)
							 or (newTile is upTile)
							 or (newTile is downTile)):
							 	if (not newTile.occupied) or newTile.mixer:
									 if not prevTileRef.mixer or firstTile:
										prevTile = newTile
										prevTileRef = newTile
										points.append(((level.x + level.tileSize * tileUnderMouse.col) + level.tileSize / 2,
					   								   (level.y + level.tileSize * tileUnderMouse.row) + level.tileSize / 2))
										firstClick = False

			if len(points) > 1:
				pygame.draw.lines(surface, color, False, points, 6)
				for point in points:
					pygame.draw.rect(surface, color, pygame.Rect(point[0]-2, point[1]-2, 6, 6))

		else:
			if points:
				# If final point in list is valid sticking point,
				# append points to connected to draw them indefinitely
				if (level.getTileByCoord(points[len(points)-1]).mixer
				or (level.getTileByCoord(points[len(points)-1]).isExitPoint
				and level.getTileByCoord(points[len(points)-1]).exitPointHue == level.getTileByCoord(points[0]).colorNodeHue)):
					# only if the middle point of mixer is in points should connection happen
					if len(points) > 1:
						for point in points:
							level.getTileByCoord(point).occupied = True

						if level.getTileByCoord(pygame.mouse.get_pos()).isExitPoint:
							level.getTileByCoord(pygame.mouse.get_pos()).solved = True
							for exitpoint in level.exitpoints:
								if (exitpoint["col"] == level.getTileByCoord(points[len(points)-1]).col
								and exitpoint["row"] == level.getTileByCoord(points[len(points)-1]).row):
									exitpoint["solved"] = True

							if level.levelIsSolved():
								level.renderLevelComplete()

						# TODO: ADD FUNCTIONALITY TO REMOVE CONNECTIONS THAT ARE NOW INVALID
						connected.append(points)
						colors.append(color)
						level.getTileByCoord(points[len(points)-1]).connectingColors.append(color)
						level.refreshEntryPoints()

			points = []
			firstClick = True
			firstTile = False
			prevTile = None
			diagonal = False

	if connected:
		i = 0
		for connection in connected:
			pygame.draw.lines(surface, colors[i], False, connection, 6)
			for point in connection:
				pygame.draw.rect(surface, colors[i], pygame.Rect(point[0]-2, point[1]-2, 6, 6))
			i += 1

	level.renderColorNodes()
	level.renderMixers()
	level.renderExitPoints()
	print points
	#print (firstTile, firstClick)
	pygame.display.flip()
