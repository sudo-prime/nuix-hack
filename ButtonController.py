import pygame

class ButtonController:
	def __init__(self, s, buttons):
		self.s = s
		self.buttons = buttons
		self.buttonSpan = []

		for i in range(0, len(buttons)):
			self.buttonSpan.append(pygame.Rect(self.buttons[i].x, self.buttons[i].y, self.buttons[i].width, self.buttons[i].height))

	def renderButtons(self):
		for i in range(0, len(self.buttons)):
			self.buttons[i].render()

	def getButtonByCoord(self, coord):
		for i in range(0, len(self.buttons)):
			if self.buttonSpan[i].collidepoint(coord):
				return self.buttons[i]

		return None
