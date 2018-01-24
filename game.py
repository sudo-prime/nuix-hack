import pygame # Module used for all graphics.
from Level import Level # Custom level class, used for tracking tiles and drawing level elements to screen.
from Button import Button # Custom button class. For clicking!
from ButtonController import ButtonController # Button Controller class handles drawing and keeping track of all buttons.
import hues # Module that contains some pre-defined color assignments and color-handling methods
import copy # Module used to copy level details / defaults, gets around python pass-by-name for mutable objects


width = 1600 # The width (px) of the screen.
height = 900 # The height (px) of the screen.

pygame.init() # Initialize the pygame module.

# Create variables to control how the game runs.
# clock is used for framerate, surface is drawn to, running is the game loop condition.
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

# frameObjs array holds loaded pyagme.image objects, so that they can be displayed sequentially -
# and frame holds the index of the current frame.
frame = 0
frameObjs = []

# Appending all pygame.image ojects to the frameObjs array.
for i in range(0, 240):
	frameObjs.append(pygame.image.load(str('00000'[:4 - len(str(i))+1] + str(i) + '.png')))

# Create various flags to keep track of what's going on in the game.
colors = []		   # Array for storing colors of established connections.
connected = []		# Array of established connections.
points = []		   # The center points of all (valid) tiles the user has dragged through.
firstClick = True	 # Whether it's the frame on which the user has clicked for the first time
firstTile = False	  # Whether the tile being clicked (and that is under the mouse) is the first tile
prevTile = None	   # Holds reference to the last tile the user was on, checked every frame - unless
					  # the user dragged to another, this will be none. Otherwise, it'll be a tile object.
prevTileRef = None	# Same thing as prevTile, but this object remains unchanged until later in the
					  # code, so that it can still be referenced.
levelNum = -2		  # The ID of the level the user is currently on. (-2 is title screen.)
clicking = False	  # Used to detect rising edge of mouse click, helps avoid unintended button presses.
prevClicking = False  # See above.
solved = False		  # Whether or not the current puzzle has been solved.
wasMixer = False	  # Whether the first node that was dragged from was a mixer to begin with.

# Dict that holds an array of button objects, associated with the level ID on which they are displayed.
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

# Button contoller to contain all of the level's buttons and make them accessible.
buttonController = ButtonController(surface, buttons[levelNum])

# Color node dict, like the buttons dict, holds dictionaries containing info for each color node.
# Grouped by level ID on which they are displayed.
colornodes = {
	1: [
		{"hue": hues.GREEN, "col": -1, "row": 0}
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
		{"hue": hues.GREEN, "col": 2, "row": 1},
		{"hue": hues.INDIGO, "col": 3, "row": 2}
	]
}

# Dict of mixer coordinates (tile col, tile row), grouped by level ID on which they are displayed.
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

# Dict of obstacle coordinates (tile col, tile row), grouped by level ID on which they are displayed.
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

# Exit point dict, like the buttons dict, holds dictionaries containing info for each exit node.
# Grouped by level ID on which they are displayed.
exitpoints = {
	1: [
		{"hue": hues.GREEN, "col": 1, "row": 0, "solved": False}
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

# Make copy of the level defaults that can be changed as the game is running -
# so that they arent permanently changed. Gets around python pass-by-name style.
colornodesCopy = copy.deepcopy(colornodes)
mixersCopy = copy.deepcopy(mixers)
exitpointsCopy = copy.deepcopy(exitpoints)


"""
	@param int levelNum
		The integer ID associated with the current level \ screen.
	@return Level
		Level object which is used to display necessary graphics
		and handle tile logic while the user is doing a puzzle.
"""
def updateDefaults(levelNum):
	# Like above, refresh the copies by overwriting them:
	colornodesCopy = copy.deepcopy(colornodes)
	mixersCopy = copy.deepcopy(mixers)
	exitpointsCopy = copy.deepcopy(exitpoints)

	# Dictionary of levels, constructed using the level defaults.
	levelList = {
		1: Level(surface, 1, 1, 100, width, height, colornodesCopy[1], mixersCopy[1], exitpointsCopy[1], obstacles[1]),
		2: Level(surface, 1, 1, 100, width, height, colornodesCopy[2], mixersCopy[2], exitpointsCopy[2], obstacles[2]),
		3: Level(surface, 3, 3, 100, width, height, colornodesCopy[3], mixersCopy[3], exitpointsCopy[3], obstacles[3]),
		4: Level(surface, 1, 1, 100, width, height, colornodesCopy[4], mixersCopy[4], exitpointsCopy[4], obstacles[4]),
		5: Level(surface, 2, 1, 100, width, height, colornodesCopy[5], mixersCopy[5], exitpointsCopy[5], obstacles[5]),
		6: Level(surface, 4, 3, 100, width, height, colornodesCopy[6], mixersCopy[6], exitpointsCopy[6], obstacles[6]),
		7: Level(surface, 6, 3, 100, width, height, colornodesCopy[7], mixersCopy[7], exitpointsCopy[7], obstacles[7]),
	}

	# Lastly, return the level that has been reconstructed.
	return levelList[levelNum]

# Initialize the first level.
level = updateDefaults(1)

# pygame.image objects, for all of the buttons in the game.
exitIcon = pygame.image.load("exitIcon.png")
levelsIcon = pygame.image.load("levelsIcon.png")
nextIcon = pygame.image.load("nextIcon.png")
backIcon = pygame.image.load("backIcon.png")
solvedIcon = pygame.image.load("solvedIcon.png")

# Number icons for the buttons on the level select screen.
numIcons = {
	1: pygame.image.load("numIcon_1.png"),
	2: pygame.image.load("numIcon_2.png"),
	3: pygame.image.load("numIcon_3.png"),
	4: pygame.image.load("numIcon_4.png"),
	5: pygame.image.load("numIcon_5.png"),
	6: pygame.image.load("numIcon_6.png"),
	7: pygame.image.load("numIcon_7.png"),
}

# Game loop:
while running:
	# All loops within the game loop correspond to a certain screen / level ID.
	while levelNum == -2:
		# User is at title screen.
		clock.tick(60) # Restrict framerate to 60fps.
		surface.fill(hues.WHITE) # Start from white screen.

		# Initialize the ButtonController for the title screen.
		buttonController = ButtonController(surface, buttons[levelNum])

		# If the "x" window icon is pressed, close the game.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				levelNum = "QUIT"
				running = False

		# titleFrame is the specific pygame.image object for the current frame of the title screen.
		titleFrame = frameObjs[frame]
		# Render that image.
		surface.blit(titleFrame, (100, 75))
		# Lastly, increment the frame - if the frame is >= 240 (the total number of frames), start over.
		frame += 1
		if frame >= 240:
			frame = 0

		# Get the button object currently under the mouse by the mouse coordinates.
		buttonUnderMouse = buttonController.getButtonByCoord(pygame.mouse.get_pos())

		# Render the buttons to the screen.
		buttonController.renderButtons()

		if buttonUnderMouse is not None:
			# If there's a button currently under the mouse,
			# Render the hover graphics on that button.
			buttonUnderMouse.renderHover()
			if pygame.mouse.get_pressed()[0]:
				# If the left mouse button is currently held,
				# The user is clicking.
				clicking = True
				if prevClicking != clicking:
					# If the user wasn't previously clicking before,
					# Now they are - update prevClicking.
					prevClicking = clicking

					# Set the level ID to that of the button.
					levelNum = buttonUnderMouse.levelDirect()

					if levelNum in [1, 2, 3, 4, 5, 6, 7]:
						# If the level the user is going to is a puzzle level,
						# Re-construct that level with its default values.
						level = updateDefaults(levelNum)
			else:
				# Otherwise, the user isn't currently clicking the mouse.
				prevClicking = False
				clicking = False

		# Draw the "level." and "exit." buttons to the screen.
		surface.blit(levelsIcon, (134, 365))
		surface.blit(exitIcon, (134, 525))

		# Update the display.
		pygame.display.flip()

	while levelNum == -1:
		# User is at the level select screen.
		clock.tick(60) # Restricts framerate to 60fps
		surface.fill(hues.WHITE) # Start from white screen

		# Initialize the ButtonController for the level select screen.
		buttonController = ButtonController(surface, buttons[levelNum])

		# If the "x" window icon is pressed, close the game.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				levelNum = "QUIT"
				running = False

		# Get the button object currently under the mouse by the mouse coordinates.
		buttonUnderMouse = buttonController.getButtonByCoord(pygame.mouse.get_pos())

		# Render the buttons to the screen.
		buttonController.renderButtons()

		if buttonUnderMouse is not None:
			# If there's a button currently under the mouse,
			# Render the hover graphics on that button.
			buttonUnderMouse.renderHover()
			if pygame.mouse.get_pressed()[0]:
				# If the left mouse button is currently held,
				# The user is clicking.
				clicking = True
				if prevClicking != clicking:
					# If the user wasn't previously clicking before,
					# Now they are - update prevClicking.
					prevClicking = clicking

					# Set the level ID to that of the button.
					levelNum = buttonUnderMouse.levelDirect()

					if levelNum in [1, 2, 3, 4, 5, 6, 7]:
						# If the level the user is going to is a puzzle level,
						# Re-construct that level with its default values.
						level = updateDefaults(levelNum)
			else:
				# Otherwise, the user isn't currently clicking the mouse.
				prevClicking = False
				clicking = False

		# Draw the "back" icon to the screen.
		surface.blit(backIcon, (width/2 - 500, 95))

		# Draw the level number icons to the screen.
		for i in range(1, len(numIcons) + 1):
			surface.blit(numIcons[i], (buttonController.buttons[i-1].x, buttonController.buttons[i-1].y))

		# Update the display.
		pygame.display.flip()

	while levelNum in [1, 2, 3, 4, 5, 6, 7]:
		# User is playing a level!
		clock.tick(60) # Restricts framerate to 60fps.
		surface.fill(hues.WHITE) # Start from white screen.
		level.renderLevelLines() # Render the lines of the level.

		tileUnderMouse = level.getTileByCoord(pygame.mouse.get_pos())

		# DEBUG: Renders debug squares over entry points
		# for x in range(-1, len(level.tiles)-1):
		#	 for y in range(-1, len(level.tiles[x])-1):
		#		 if level.tiles[x][y].entryPoint is not None:
		#			 level.tiles[x][y].renderDebugSquare()

		# DEBUG: Renders debug square on occupied tiles
		# for x in range(-1, len(level.tiles)-1):
		#	 for y in range(-1, len(level.tiles[x])-1):
		#		 if level.tiles[x][y].occupied:
		#			 level.tiles[x][y].renderDebugSquare()

		# DEBUG: Renders debug square on solved tiles
		# for x in range(-1, len(level.tiles)-1):
		#	 for y in range(-1, len(level.tiles[x])-1):
		#		 if level.tiles[x][y].solved:
		#			 level.tiles[x][y].renderDebugSquare()

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
							print(color)

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
											 if (not prevTileRef.mixer or firstTile) and (not prevTileRef.isExitPoint):
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

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# If the user presses the "x" window button, quit the game.
				levelNum = "QUIT"
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				# If the user presses "r", refresh the level.
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
				# If the user presses escape, refresh the level and return to the level select screen.
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

		pygame.display.flip()

	if levelNum == "QUIT":
		running = False
