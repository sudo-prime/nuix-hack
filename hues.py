import pygame

RED =        pygame.Color(255, 0, 0)
ORANGE =     pygame.Color(255, 128, 0)
YELLOW =     pygame.Color(255, 255, 0)
LIME =       pygame.Color(128, 220, 0)
GREEN =      pygame.Color(0, 220, 0)
CYAN =       pygame.Color(0, 128+64, 255)
BLUE =       pygame.Color(0, 128, 255)
INDIGO =     pygame.Color(0, 0, 255)
PURPLE =     pygame.Color(128, 0, 255)
MAGENTA =    pygame.Color(255, 0, 255)
WHITE =      pygame.Color(255, 255, 255)
GRAY =       pygame.Color(175, 175, 175)
LIGHT_GRAY = pygame.Color(245, 245, 245)
MED_GRAY =   pygame.Color(205, 205, 205)
CLICK_GRAY = pygame.Color(240, 240, 240)
BLACK =      pygame.Color(0, 0, 0)

def average(colors):
	rsum = 0
	gsum = 0
	bsum = 0

	for color in colors:
		rsum += color.r
		gsum += color.g
		bsum += color.b

	if len(colors) is not 0:
		return pygame.Color(rsum/len(colors), gsum/len(colors), bsum/len(colors))
	else:
		return GRAY
