"""Classes for messages to be displayed and a log for recording them."""
# Source: Roguelike Tutorial Revised
# https://github.com/TStand90/roguelike_tutorial_revised/blob/part7/game_messages.py

import textwrap

class Message:
	def __init__(self, text, colour = 'white'):
		self.text = text
		self.colour = colour
		

class MessageLog:
	def __init__(self, x, width, height):
		self.x = x
		self.width = width
		self.height = height
		self.messages = []
		
	def add_msg(self, message):
		lines = textwrap.wrap(message.text, self.width)
		
		for line in lines:
			if len(self.messages) == self.height:
				del(self.messages[0])
			
			self.messages.append(Message(line, message.colour))