import random, sys
from player import Player
from enum import Enum
from copy import copy


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
		self.target_positions = []
		self.set_goal_grid_pos(9, 9)

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
				self.set_goal_grid_pos(15, 15)
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

	def set_goal_grid_pos(self, gx, gy):
		# locate our current grid position
		pos = self.grid.pixel_to_grid(self.x, self.y)

		# generate a list of all the paths that will take us to the goal,
		# and determine the shortest path
		path = sorted(self.gen_path_list(pos[0], pos[1], gx, gy), key=lambda l: len(l))[0]

		# generate a list of pixel-space target positions to navigate to
		self.target_positions = [self.grid.grid_to_pixel(*e) for e in path[::-1]]

	def gen_path_list(self, start_gx, start_gy, goal_gx, goal_gy):
		results = []
		self.find_func(results, [], goal_gx, goal_gy, start_gx, start_gy)
		return results

	def find_func(self, results_list, working_list, goal_grid_x, goal_grid_y, current_grid_x, current_grid_y):

		# base case: we are at the goal position
		if (current_grid_x == goal_grid_x) and (current_grid_y == goal_grid_y):
			results_list.append(working_list)
			return

		# if the current working list of moves is too long, cut off this
		# search, as it's likely off in the weeds
		# TODO: this limit should be empiricaly definied
		if len(working_list) > 32:
			return

		# continue the search by branching off into each of the four directions
		for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
			new_pos = self.apply_direction(current_grid_x, current_grid_y, d)
			if (new_pos[0] < 0) or (new_pos[0] >= self.grid.w):
				continue
			if (new_pos[1] < 0) or (new_pos[1] >= self.grid.h):
				continue
			if new_pos in working_list:
				continue
			if self.grid.value(*new_pos) != 'x':
				new_working_list = copy(working_list)
				new_working_list.append(new_pos)
				self.find_func(results_list, new_working_list, goal_grid_x, goal_grid_y, *new_pos)

	def apply_direction(self, x, y, d):
		if d == Direction.UP:
			return x, y - 1
		if d == Direction.DOWN:
			return x, y + 1
		if d == Direction.LEFT:
			return x - 1, y
		if d == Direction.RIGHT:
			return x + 1, y
		return x, y
