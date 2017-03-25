import random, time, sys
from concurrent.futures import ThreadPoolExecutor
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
		self.target_positions = []
		self.executor = ThreadPoolExecutor()
		self.active_search = None

	def update(self):

		# if a search is currently underway, check to see if it has
		# completed and retrieve the results
		if self.active_search and self.active_search.done():
			self.target_positions = self.active_search.result()
			self.active_search = None

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

		# how close are we to the next position?
		distance = self.distance_to(target_position)

		# if we are going too fast; meaning that a movement towards
		# the next position will take us past it, we will slow down
		# so that we won't pass it by
		original_speed = self.speed
		if distance < self.speed:
			self.speed = distance

		# move in the correct direction to take us to the next position
		self.direction = self.direction_to(target_position)
		if self.direction == Direction.UP:
			self.move_up()
		if self.direction == Direction.DOWN:
			self.move_down()
		if self.direction == Direction.LEFT:
			self.move_left()
		if self.direction == Direction.RIGHT:
			self.move_right()

		# restore our speed, because we might have changed it
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

	def find_shortest_path_to(self, goal_pos):

		start_time = time.time()

		# locate our current grid position
		pos = self.grid.pixel_to_grid(self.x, self.y)

		# generate a list of all the paths that will take us to the goal,
		# and determine the shortest path
		path = sorted(self.generate_path_list(pos, goal_pos), key=lambda l: len(l))[0]

		total_time = time.time() - start_time
		print('took %2.2f seconds' % total_time)
		sys.stdout.flush()

		# generate a list of pixel-space target positions to navigate to
		return [self.grid.grid_to_pixel(*e) for e in path[::-1]]

	def set_goal_grid_pos(self, goal_pos):
		# if we have an active search going, we don't want to start another one
		if self.active_search:
			return
		# submit a search to be run on another thread
		self.active_search = self.executor.submit(self.find_shortest_path_to, goal_pos)

	def generate_path_list(self, start, end):
		'''
		Generate all of the possible paths that lead from the start
		position to the end position
		'''
		results = []
		self.find_func(results, [], set(), start, end)
		return results

	def find_func(self, results_list, working_list, working_set, current_pos, goal_pos):
		'''
		This helper function recursively generates all of the paths (in grid space)
		that lead from current_pos to goal_pos.
		'''
		# base case: we are at the goal position
		if current_pos == goal_pos:
			# add the current path to the result list
			results_list.append([l for l in working_list])
			return

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
			if new_pos in working_set:
				continue

			# finally, check to see if we've collided with a wall.  if not, we
			# add this new position to our path and continue searching for the
			# next move
			if self.grid.value(*new_pos) != 'x':
				working_list.append(new_pos)
				working_set.add(new_pos)
				self.find_func(results_list, working_list, working_set, new_pos, goal_pos)
				# after we've considered all possible paths following this move, we
				# can remove it from our current path
				working_list.pop()
				working_set.remove(new_pos)

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
