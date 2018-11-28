"""Enum for Game States."""
# Source: Roguelike Tutorial Revised
# https://github.com/TStand90/roguelike_tutorial_revised/blob/part7/game_states.py

from enum import Enum

class GameStates(Enum):
	PLAYER = 1
	ENEMY = 2
	DEAD = 3
	DIRECTION = 4