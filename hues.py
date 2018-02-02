import pygame
from Hue import Hue
import math

RED =        Hue(255, 0, 0, 1)
ORANGE =     Hue(255, 127, 0, 2)
YELLOW =     Hue(255, 255, 0, 1)
LIME =       Hue(128, 220, 0, 2)
GREEN =      Hue(0, 255, 0, 2)
CYAN =       Hue(0, 255, 255, 2)
BLUE =       Hue(0, 0, 255, 1)
PURPLE =     Hue(128, 0, 255, 2)
MAGENTA =    Hue(255, 0, 255, 2)
WHITE =      Hue(255, 255, 255, 0)
GRAY =       Hue(175, 175, 175, 0)
LIGHT_GRAY = Hue(245, 245, 245, 0)
MED_GRAY =   Hue(205, 205, 205, 0)
CLICK_GRAY = Hue(240, 240, 240, 0)
BLACK =      Hue(0, 0, 0, 4)

def average(colors):
	if BLACK in colors:
		return BLACK

	combinations = []

	if colors:
		rsum = 0
		ysum = 0
		bsum = 0

		for color in colors:
			combinations.append(color.mixes)
			ryb = toRYB(color.r, color.g, color.b)
			rsum += ryb[0]
			ysum += ryb[1]
			bsum += ryb[2]

		rgb = toRGB(rsum, ysum, bsum)
		rgb = maxSat(rgb[0], rgb[1], rgb[2])
		newColor = Hue(rgb[0], rgb[1], rgb[2], sum(combinations))

		if sum(combinations) > 3:
			return BLACK
		else:
			return newColor
	else:
		return GRAY

def subtract(colors):
	if len(colors) >= 2:
		# color[1] - color[0]
		color0 = toRYB(colors[0].r, colors[0].g, colors[0].b)
		color0 = maxSat(color0[0], color0[1], color0[2])
		color1 = toRYB(colors[1].r, colors[1].g, colors[1].b)
		color1 = maxSat(color1[0], color1[1], color1[2])
		howMixed = colors[1].mixes - colors[0].mixes
		r = max(color1[0] - color0[0], 0)
		y = max(color1[1] - color0[1], 0)
		b = max(color1[2] - color0[2], 0)
		rgb = toRGB(r, y, b)
		rgb = maxSat(rgb[0], rgb[1], rgb[2])
		if rgb == (0, 0, 0):
			return BLACK
		return Hue(rgb[0], rgb[1], rgb[2], howMixed)
	return GRAY

def toRYB(r, g, b):
	iRed = r
	iGreen = g
	iBlue = b

	iWhite = min(iRed, iGreen, iBlue)

	iRed   -= iWhite
	iGreen -= iWhite
	iBlue  -= iWhite

	iMaxGreen = max(iRed, iGreen, iBlue)

	iYellow = min(iRed, iGreen)

	iRed   -= iYellow
	iGreen -= iYellow

	if iBlue > 0 and iGreen > 0:
		iBlue  /= 2
		iGreen /= 2

	iYellow += iGreen
	iBlue   += iGreen

	iMaxYellow = max(iRed, iYellow, iBlue)

	if iMaxYellow > 0:
		iN = iMaxGreen / iMaxYellow

		iRed    *= iN
		iYellow *= iN
		iBlue   *= iN

	iRed    += iWhite
	iYellow += iWhite
	iBlue   += iWhite

	return (int(math.floor(iRed)), int(math.floor(iYellow)), int(math.floor(iBlue)))

def toRGB(r, y, b):
	iRed = r
	iYellow = y
	iBlue = b

	iWhite = min(iRed, iYellow, iBlue)

	iRed    -= iWhite;
	iYellow -= iWhite;
	iBlue   -= iWhite;

	iMaxYellow = max(iRed, iYellow, iBlue)

	iGreen = min(iYellow, iBlue)

	iYellow -= iGreen
	iBlue   -= iGreen

	if iBlue > 0 and iGreen > 0:
		iBlue  *= 2.0
		iGreen *= 2.0

	iRed   += iYellow
	iGreen += iYellow

	iMaxGreen = max(iRed, iGreen, iBlue)

	if iMaxGreen > 0:
	 	iN = iMaxYellow / float(iMaxGreen)

	 	iRed   *= iN
	 	iGreen *= iN
	 	iBlue  *= iN

	iRed   += iWhite
	iGreen += iWhite
	iBlue  += iWhite

	return (int(math.floor(iRed)), int(math.floor(iGreen)), int(math.floor(iBlue)))

def maxSat(r, g, b):
	maxPrim = max(r, g, b)
	if maxPrim == 0:
		return (0,0,0)
	factor = 255 / float(maxPrim)
	r *= factor
	g *= factor
	b *= factor
	return (int(math.ceil(r)), int(math.ceil(g)), int(math.ceil(b)))
