from typing import Protocol
from enum import Enum
from abc import ABC, abstractmethod

class Color(Enum):
	Black = 0
	DarkBlue = 1
	DarkPurple = 2
	DarkGreen = 3
	Brown = 4
	DarkGray = 5
	LightGray = 6
	White = 7
	Red = 8
	Orange = 9
	Yellow = 10
	Green = 11
	Blue = 12
	Indigo = 13
	Pink = 14
	Peach = 15

class Enemy(ABC):
	"""
	Base enemy
	Position is tracked in grid space (col, row)
	Coordinates are floats so movement will be smooth
	Radius in pixels, usually used for collision detected
	`progress` check move_enemy() in model.py for explanation
	`next_idx` tracks which path indx to go next
	"""
	def __init__(self, start_col, start_row, radius):
		self._walk_speed = 0.1
		self._color = Color.Orange
		self._base_health = 1
		self._current_health = 1
		self._col = float(start_col)
		self._row = float(start_row)
		self._radius = radius # pixel radius, for collision detection
		self._next_idx = 1 # what ith path coord to go next
		self._progress = 0 # basically like ith current/previous passed path coord, then yung decimals indicates the progress towards the next path coord

	@property
	def walk_speed(self):
		return self._walk_speed
	
	@property
	def color(self):
		return self._color
	
	@property
	def base_health(self):
		return self._base_health
	
	@property
	def current_health(self):
		return self._current_health

	@property
	def col(self):
		return self._col

	@property
	def row(self):
		return self._row

	@property
	def next_idx(self):
		return self._next_idx
	
	@property
	def progress(self):
		return self._progress

	@property
	def radius(self):
		return self._radius

	@col.setter
	def col(self, value):
		self._col = value

	@row.setter
	def row(self, value):
		self._row = value

	@radius.setter
	def radius(self, value):
		self._radius = value

	@progress.setter
	def progress(self, value):
		self._progress = value

	@current_health.setter
	def current_health(self, value):
		self._current_health = value

class OrangeEnemy(Enemy):
	def __init__(self, start_col = 0, start_row = 0, radius = 15):
		super().__init__(start_col, start_row, radius)
		self._walk_speed = 0.1
		self._color = Color.Orange
		self._base_health = 1
		self._current_health = 1

class RedEnemy(Enemy):
	def __init__(self, start_col = 0, start_row = 0, radius = 15):
		super().__init__(start_col, start_row, radius)
		self._walk_speed = 0.1
		self._color = Color.Red
		self._base_health = 1
		self._current_health = 1

class BlueEnemy(Enemy):
	def __init__(self, start_col = 0, start_row = 0, radius = 15):
		super().__init__(start_col, start_row, radius)
		self._walk_speed = 0.1
		self._color = Color.Blue
		self._base_health = 1
		self._current_health = 1