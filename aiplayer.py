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
		self.target_positions = []

	def update(self):

		# if we don't have any targets to navigate to, we just stand still
		if not self.target_positions:
			return

		# locate our current target position
		target_position = self.target_positions[-1]

		# check to see if we're already at our current target, and remove that
		# target from the list if we're there
		while (self.x, self.y) == target_position:
			self.target_positions.pop()
			if not self.target_positions:
				return
			target_position = self.target_positions[-1]

		self.direction = self.direction_to(target_position)

		distance = self.distance_to(target_position)

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

	def direction_to(self, target):
		'''Based on our current position, what direction do I need
		to travel in order to get to this next position?'''
		if self.x < target[0]:
			return Direction.RIGHT
		if self.x > target[0]:
			return Direction.LEFT
		if self.y < target[1]:
			return Direction.DOWN
		if self.y > target[1]:
			return Direction.UP
		return Direction.NONE

	def distance_to(self, target):
		'''
		Determine the Manhattan distance between ourselves and
		the target position
		''' 
		return int(abs(self.x - target[0]) + abs(self.y - target[1]))

	def set_goal_grid_pos(self, goal_pos):
		# locate our current grid position
		pos = self.grid.pixel_to_grid(self.x, self.y)

		# generate a list of all the paths that will take us to the goal,
		# and determine the shortest path
		path = sorted(self.generate_path_list(pos, goal_pos), key=lambda l: len(l))[0]

		# generate a list of pixel-space target positions to navigate to
		self.target_positions = [self.grid.grid_to_pixel(*e) for e in path[::-1]]

	def generate_path_list(self, start, end):
		'''
		Generate all of the possible paths that lead from the start
		position to the end position
		'''
		results = []
		self.find_func(results, [], start, end)
		return results

	def find_func(self, results_list, working_list, current_pos, goal_pos):
		'''
		This helper function recursively generates all of the paths (in grid space)
		that lead from current_pos to goal_pos.
		'''
		# base case: we are at the goal position
		if current_pos == goal_pos:
			# add the current path to the result list
			results_list.append(working_list)
			return

		# if the current working list of moves is too long, cut off this
		# search, as it's likely off in the weeds
		# TODO: this limit should be empiricaly definied
		#if len(working_list) > 32:
		#	return

		# continue the search by branching off into each of the four directions
		for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:

			# if we follow this direction, what will our new postion be?
			new_pos = self.apply_direction(current_pos, d)

			# make sure this new position isn't beyond the bounds of the grid
			if (new_pos[0] < 0) or (new_pos[0] >= self.grid.w):
				continue
			if (new_pos[1] < 0) or (new_pos[1] >= self.grid.h):
				continue

			# we also want to make sure we haven't already visited this positon
			# before
			if new_pos in working_list:
				continue

			# finally, check to see if we've collided with a wall.  if not, we
			# add this new position to our path and continue searching for the
			# next move
			if self.grid.value(*new_pos) != 'x':
				new_working_list = copy(working_list)
				new_working_list.append(new_pos)
				self.find_func(results_list, new_working_list, new_pos, goal_pos)

	def apply_direction(self, pos, d):
		'''
		Given a position and a direction, determine what the new position
		will be once the player moves in that direction.
		'''
		if d == Direction.UP:
			return pos[0], pos[1] - 1
		if d == Direction.DOWN:
			return pos[0], pos[1] + 1
		if d == Direction.LEFT:
			return pos[0] - 1, pos[1]
		if d == Direction.RIGHT:
			return pos[0] + 1, pos[1]
		return x, y
