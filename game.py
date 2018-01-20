import pygame
import Event
from Level import Level
import hues
from ColorNode import ColorNode

width = 1280
height = 720

pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

testNode = ColorNode(hues.RED, "RIGHT", 1, -1)
testNode2 = ColorNode(hues.YELLOW, "LEFT", 1, 3)
level1 = Level(surface, 3, 2, 100, width, height, [testNode, testNode2], [(1, 1)])

colors = []
connected = []
points = []
prevTile = None
firstClick = True
diagonal = False

while running:
	clock.tick(60) # Restricts framerate to 60fps
	surface.fill(hues.WHITE) # Start from white screen

	for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	                running = False

	level1.render()
	tileUnderMouse = level1.getTileByCoord(pygame.mouse.get_pos())

	# DEBUG - SHOWS ENTRY POINTS IN ORANGE
	# for y in range(0, len(level1.tiles)):
	# 	for x in range(0, len(level1.tiles[y])):
	# 		if level1.tiles[x][y].entryPoint is not None:
	# 			surface.fill(hues.ORANGE, level1.tileSpan[x][y])

	# Tile hover color ch

	if tileUnderMouse is not None: #if tile under mouse exists
		tileUnderMouse.renderHover()
		# Tile being clicked color change
		if pygame.mouse.get_pressed()[0]: #if mouse is being held
			tileUnderMouse.renderClick()
			if tileUnderMouse.entryPoint is not None: #if tile under mouse is an entry point

				if firstClick: #if it's the first time clicking the entry point
					firstClick = False
					points.append(((level1.x + level1.tileSize * tileUnderMouse.entryPoint.col) + level1.tileSize / 2,
								   (level1.y + level1.tileSize * tileUnderMouse.entryPoint.row) + level1.tileSize / 2))
					color = tileUnderMouse.entryPoint.hue

			newTile = tileUnderMouse
			#print(str(newTile) + ", " +str(prevTile))

			if (newTile is not prevTile) and (newTile is not None):
				if prevTile is not None:
					if (newTile.col is not prevTile.col) and (newTile.row is not prevTile.row):
						# Diagonal movement!
						diagonal = True

				if len(points) > 1 or tileUnderMouse.entryPoint is not None:
					if  ((level1.x + level1.tileSize * tileUnderMouse.col) + level1.tileSize / 2, (level1.y + level1.tileSize * tileUnderMouse.row) + level1.tileSize / 2) not in points and not (((level1.x + level1.tileSize * tileUnderMouse.col) + level1.tileSize / 2) - points[len(points)-1][0]) > level1.tileSize and not (((level1.y + level1.tileSize * tileUnderMouse.row) + level1.tileSize / 2) - points[len(points)-1][1]) > level1.tileSize:
						if (not diagonal and not tileUnderMouse.occupied) or (tileUnderMouse.mixer and not diagonal):
							print tileUnderMouse.occupied
							prevTile = newTile
							points.append(((level1.x + level1.tileSize * tileUnderMouse.col) + level1.tileSize / 2,
										   (level1.y + level1.tileSize * tileUnderMouse.row) + level1.tileSize / 2))
							firstClick = False

				diagonal = False

			if len(points) > 1:
				pygame.draw.lines(surface, color, False, points, 6)

		else:
			if points:
				# If final point in list is valid sticking point,
				# append points to connected to draw them indefinitely
				if level1.getTileByCoord(pygame.mouse.get_pos()).mixer or level1.getTileByCoord(pygame.mouse.get_pos()).exitPoint:
					# only if the middle point of mixer is in points should connection happen
					if tileUnderMouse.middle in points:
						for point in points[1:]:
							level1.getTileByCoord(point).occupied = True
						connected.append(points)
						colors.append(color[0])
						level1.getTileByCoord(pygame.mouse.get_pos()).connectingColors.append(color[0])

			points = []
			firstClick = True
			prevTile = None
			diagonal = False

	# For rendering debug square on occupied tiles
	# for x in range(0, len(level1.tiles)):
	# 	for y in range(0, len(level1.tiles[x])):
	# 		if level1.tiles[x][y].occupied:
	# 			level1.tiles[x][y].renderDebugSquare()

	if connected:
		i = 0
		for connection in connected:
			pygame.draw.lines(surface, colors[i], False, connection, 6)
			i += 1

	level1.renderMixers()

	pygame.display.flip()
