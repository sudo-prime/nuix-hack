import pygame
import math
import chroma

RED =        pygame.Color(255, 0, 0)
ORANGE =     pygame.Color(255, 128, 0)
YELLOW =     pygame.Color(255, 255, 0)
LIME =       pygame.Color(128, 220, 0)
GREEN =      pygame.Color(0, 255, 0)
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

R_WEIGHT = 0.875
G_WEIGHT = 1
b_WEIGHT = 0.80

def average(colors):
	rsum = 0
	gsum = 0
	bsum = 0

	for color in colors:
		rsum += color.r
		gsum += color.g
		bsum += color.b

		if len(colors) > 1:
			rsum = min(255, math.floor(rsum * R_WEIGHT))
			gsum = min(255, math.floor(gsum * G_WEIGHT))
			bsum = min(255, math.floor(bsum * b_WEIGHT))

	if colors:
		return pygame.Color(rsum//len(colors), gsum//len(colors), bsum//len(colors), 255)
	else:
		return GRAY
