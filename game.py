import pygame
import Event
from Level import Level
from Button import Button
from ButtonController import ButtonController
import hues
import math
import copy


width = 1600
height = 900

pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
frame = 0
frameObjs = []

for i in range(0, 240):
	frameObjs.append(pygame.image.load(str('00000'[:4 - len(str(i))+1] + str(i) + '.png')))

colors = []
connected = []
points = []
firstClick = True
firstTile = False
prevTile = None
prevTileRef = None
levelNum = -2
clicking = False
prevClicking = False
solved = False
wasMixer = False

buttons = {
	-1: [
		Button(surface, width/2 - 500, height/2 - 50, 100, 100, 1),
		Button(surface, width/2 - 350, height/2 - 50, 100, 100, 2),
		Button(surface, width/2 - 200, height/2 - 50, 100, 100, 3),
		Button(surface, width/2 - 50,  height/2 - 50, 100, 100, 4),
		Button(surface, width/2 + 100, height/2 - 50, 100, 100, 5),
		Button(surface, width/2 + 250, height/2 - 50, 100, 100, 6),
		Button(surface, width/2 + 400, height/2 - 50, 100, 100, 7),
		Button(surface, width/2 - 500, 95, 175, 77, -2),
	],
	-2: [
		Button(surface, 134, 365, 300, 100, -1),
		Button(surface, 134, 525, 300, 100, "QUIT")
	]
}

buttonController = ButtonController(surface, buttons[levelNum])

colornodes = {
	1: [
		{"hue": hues.RED, "col": -1, "row": 0}
	],
	2: [
		{"hue": hues.RED, "col": -1, "row": 0}
	],
	3: [
		{"hue": hues.RED, "col": -1, "row": 1}
	],
	4: [
		{"hue": hues.RED, "col": -1, "row": 0},
		{"hue": hues.YELLOW, "col": 1, "row": 0}
	],
	5: [
		{"hue": hues.BLUE, "col": 2, "row": 0},
		{"hue": hues.YELLOW, "col": -1, "row": 0}
	],
	6: [
		{"hue": hues.INDIGO, "col": -1, "row": 1},
		{"hue": hues.RED, "col": 4, "row": 1}
	],
	7: [
		{"hue": hues.RED, "col": 3, "row": 0},
		{"hue": hues.YELLOW, "col": 2, "row": 1},
		{"hue": hues.BLUE, "col": 3, "row": 2}
	]
}

mixers = {
	1: [ ],
	2: [
		(0, 0)
	],
	3: [

	],
	4: [
		(0, 0)
	],
	5: [
		(0, 0),
		(1, 0)
	],
	6: [
		(0, 1),
		(1, 2),
		(3, 1)
	],
	7: [
		(1, 2),
		(4, 2)
	]
}

obstacles = {
	1: [ ],
	2: [ ],
	3: [
		(1, 1),
		(0, 0)
	],
	4: [ ],
	5: [ ],
	6: [ ],
	7: [ ]
}

exitpoints = {
	1: [
		{"hue": pygame.Color(255, 0, 0, 255), "col": 1, "row": 0, "solved": False}
	],
	2: [
		{"hue": pygame.Color(255, 0, 0, 255), "col": 0, "row": -1, "solved": False},
		{"hue": pygame.Color(255, 0, 0, 255), "col": 0, "row": 1, "solved": False}
	],
	3: [
		{"hue": pygame.Color(255, 0, 0, 255), "col": 1, "row": -1, "solved": False}
	],
	4: [
		{"hue": pygame.Color(255, 127, 0, 255), "col": 0, "row": -1, "solved": False}
	],
	5: [
		{"hue": hues.YELLOW, "col": 0, "row": -1, "solved": False},
		{"hue": pygame.Color(127, 191, 127, 255), "col": 1, "row": -1, "solved": False},
		{"hue": pygame.Color(127, 191, 127, 255), "col": 1, "row": 1, "solved": False}
	],
	6: [
		{"hue": pygame.Color(63, 0, 191, 255), "col": 2, "row": 1, "solved": False},
	],
	7: [
		{"hue": pygame.Color(127, 191, 127, 255), "col": 2, "row": 0, "solved": False},
		{"hue": pygame.Color(127, 64, 127, 255), "col": 3, "row": 1, "solved": False}
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
		1: Level(surface, 1, 1, 100, width, height, colornodesCopy[1], mixersCopy[1], exitpointsCopy[1], obstacles[1]),
		2: Level(surface, 1, 1, 100, width, height, colornodesCopy[2], mixersCopy[2], exitpointsCopy[2], obstacles[2]),
		3: Level(surface, 3, 3, 100, width, height, colornodesCopy[3], mixersCopy[3], exitpointsCopy[3], obstacles[3]),
		4: Level(surface, 1, 1, 100, width, height, colornodesCopy[4], mixersCopy[4], exitpointsCopy[4], obstacles[4]),
		5: Level(surface, 2, 1, 100, width, height, colornodesCopy[5], mixersCopy[5], exitpointsCopy[5], obstacles[5]),
		6: Level(surface, 4, 3, 100, width, height, colornodesCopy[6], mixersCopy[6], exitpointsCopy[6], obstacles[6]),
		7: Level(surface, 6, 3, 100, width, height, colornodesCopy[7], mixersCopy[7], exitpointsCopy[7], obstacles[7]),
	}
	return levelList[levelNum]

level = updateDefaults(1)

exitIcon = pygame.image.load("exitIcon.png")
levelsIcon = pygame.image.load("levelsIcon.png")
nextIcon = pygame.image.load("nextIcon.png")
backIcon = pygame.image.load("backIcon.png")
solvedIcon = pygame.image.load("solvedIcon.png")
numIcons = {
	1: pygame.image.load("numIcon_1.png"),
	2: pygame.image.load("numIcon_2.png"),
	3: pygame.image.load("numIcon_3.png"),
	4: pygame.image.load("numIcon_4.png"),
	5: pygame.image.load("numIcon_5.png"),
	6: pygame.image.load("numIcon_6.png"),
	7: pygame.image.load("numIcon_7.png"),
}

while running:
	while levelNum == -2:
		# User is at title screen
		clock.tick(60) # Restricts framerate to 60fps
		surface.fill(hues.WHITE) # Start from white screen

		buttonController = ButtonController(surface, buttons[levelNum])

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				levelNum = "QUIT"
				running = False

		titleFrame = frameObjs[frame]
		surface.blit(titleFrame, (100, 75))
		frame += 1
		if frame >= 240:
			frame = 0

		buttonUnderMouse = buttonController.getButtonByCoord(pygame.mouse.get_pos())
		buttonController.renderButtons()

		if buttonUnderMouse is not None:
			buttonUnderMouse.renderHover()
			if pygame.mouse.get_pressed()[0]:
				clicking = True
				if prevClicking != clicking:
					prevClicking = clicking
					levelNum = buttonUnderMouse.levelDirect()
					if levelNum in [1, 2, 3, 4, 5, 6, 7]:
						level = updateDefaults(levelNum)
			else:
				prevClicking = False
				clicking = False

		surface.blit(levelsIcon, (134, 365))
		surface.blit(exitIcon, (134, 525))

		pygame.display.flip()

	while levelNum == -1:
		# User is at the level select screen

		clock.tick(60) # Restricts framerate to 60fps
		surface.fill(hues.WHITE) # Start from white screen

		buttonController = ButtonController(surface, buttons[levelNum])

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				levelNum = "QUIT"
				running = False

		buttonUnderMouse = buttonController.getButtonByCoord(pygame.mouse.get_pos())
		buttonController.renderButtons()

		if buttonUnderMouse is not None:
			buttonUnderMouse.renderHover()
			if pygame.mouse.get_pressed()[0]:
				clicking = True
				if prevClicking != clicking:
					prevClicking = clicking
					levelNum = buttonUnderMouse.levelDirect()
					if levelNum in [1, 2, 3, 4, 5, 6, 7]:
						level = updateDefaults(levelNum)
			else:
				prevClicking = False
				clicking = False

		surface.blit(backIcon, (width/2 - 500, 95))

		for i in range(1, len(numIcons) + 1):
			surface.blit(numIcons[i], (buttonController.buttons[i-1].x, buttonController.buttons[i-1].y))

		pygame.display.flip()

	while levelNum in [1, 2, 3, 4, 5, 6, 7]:
		# User is playing a level!
		clock.tick(60) # Restricts framerate to 60fps
		surface.fill(hues.WHITE) # Start from white screen

		level.renderLevelLines()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				levelNum = "QUIT"
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				connected = []
				colors = []
				color = None
				solved = False
				wasMixer = False
				points = []
				prevTile = None
				prevTileRef = None
				firstClick = True
				level = updateDefaults(levelNum)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				connected = []
				colors = []
				color = None
				solved = False
				wasMixer = False
				points = []
				prevTile = None
				prevTileRef = None
				firstClick = True
				level = updateDefaults(levelNum)
				levelNum = -1


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
			if not solved:
				if pygame.mouse.get_pressed()[0]: #if mouse is being held
					tileUnderMouse.renderClick()
					if tileUnderMouse.entryPoint is not None: #if tile under mouse is an entry point
						if firstClick: #if it's the first time clicking the entry point
							firstClick = False
							prevTileRef = tileUnderMouse
							points.append(((level.x + level.tileSize * tileUnderMouse.entryPoint.col) + level.tileSize / 2,
										   (level.y + level.tileSize * tileUnderMouse.entryPoint.row) + level.tileSize / 2))
							color = level.getTileByCoord(points[0]).colorNodeHue
							print color

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
												if level.getTileByCoord(points[0]).mixer:
						 						    #Tile is a mixer, and now color is being selected from it so it needs to be converted to a color node
						 							level.convertTileToColorNode(level.getTileByCoord(points[0]))
													wasMixer = True
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
					if len(points) > 1:
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
										solved = True

								connected.append(points)
								colors.append(color)
								level.getTileByCoord(points[len(points)-1]).connectingColors.append(color)
								level.refreshEntryPoints()
						else:
							if wasMixer:
								level.convertTileToMixer(level.getTileByCoord(points[0]))
								wasMixer = False

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

		if solved:
			surface.blit(solvedIcon, (width / 2 - 105, 770))

		level.renderObstacles()

		pygame.display.flip()

	if levelNum == "QUIT":
		running = False
