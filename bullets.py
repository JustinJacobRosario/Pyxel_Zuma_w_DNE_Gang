from enemies import Color
from typing import Protocol
from enum import Enum
from abc import ABC, abstractmethod
from player import Dir

class Bullet(ABC):
	def __init__(self, x, y):
		self._x = x
		self._y = y
		self._radius = 5
		self._color = Color.Orange
		self._is_used = False

		self._direction = Dir.UP

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def radius(self):
		return self._radius

	@property
	def is_used(self):
		return self._is_used

	@property
	def color(self):
		return self._color

	@property
	def direction(self):
		return self._direction

	@x.setter
	def x(self, value):
		self._x = value

	@y.setter
	def y(self, value):
		self._y = value

	@color.setter
	def color(self, value):
		self._color = value

	@radius.setter
	def radius(self, value):
		self._radius = value

	@is_used.setter
	def is_used(self, value):
		self._is_used = value

	@direction.setter
	def direction(self, value):
		self._direction = value