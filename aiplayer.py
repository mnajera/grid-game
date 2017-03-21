import random
from player import Player
from enum import Enum


class Direction(Enum):
	NONE = 0
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4


class AIPlayer(Player):

	def __init__(self, grid, screen_width, screen_height):
		super(AIPlayer, self).__init__(grid, screen_width, screen_height)
		self.directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
		self.direction = random.choice(self.directions)
		self.target_positions = [(200, 325), (100, 325), (100, 375), (25, 375)]

	def update(self):

		# if we don't have any targets to navigate to, we just stand still
		if not self.target_positions:
			return

		# locate our current target position
		target_position = self.target_positions[-1]

		# check to see if we're already at our current target, and remove that
		# target from the list if we're there
		while self.x == target_position[0] and self.y == target_position[1]:
			self.target_positions.pop()
			if not self.target_positions:
				return
			target_position = self.target_positions[-1]

		self.direction = self.direction_to(target_position[0], target_position[1])

		distance = self.distance_to(target_position[0], target_position[1])

		original_speed = self.speed
		if distance < self.speed:
			self.speed = distance

		if self.direction == Direction.UP:
			self.move_up()
		if self.direction == Direction.DOWN:
			self.move_down()
		if self.direction == Direction.LEFT:
			self.move_left()
		if self.direction == Direction.RIGHT:
			self.move_right()

		self.speed = original_speed

	def direction_to(self, next_x, next_y):
		'''Based on the current position, what direction do I need
		to travel in order to get to this next position?'''
		if self.x < next_x:
			return Direction.RIGHT
		if self.x > next_x:
			return Direction.LEFT
		if self.y < next_y:
			return Direction.DOWN
		if self.y > next_y:
			return Direction.UP
		return Direction.NONE

	def distance_to(self, next_x, next_y):
		x_distance = abs(self.x - next_x)
		y_distance = abs(self.y - next_y)
		return int(x_distance + y_distance)
