import random
from player import Player
from enum import Enum


class Direction(Enum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4


class AIPlayer(Player):

	def __init__(self, grid, screen_width, screen_height):
		super(AIPlayer, self).__init__(grid, screen_width, screen_height)
		self.directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
		self.direction = random.choice(self.directions)

	def update(self):

		old_x = self.x
		old_y = self.y

		if self.direction == Direction.UP:
			self.move_up()
		if self.direction == Direction.DOWN:
			self.move_down()
		if self.direction == Direction.LEFT:
			self.move_left()
		if self.direction == Direction.RIGHT:
			self.move_right()

		if self.x == old_x and self.y == old_y:
			self.direction = random.choice(self.directions)
