import math


class Player(object):

    def __init__(self, grid, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.xs = screen_width / grid.w
        self.ys = screen_height / grid.h
        self.x = self.xs
        self.y = self.ys
        self.speed = 3
        self.grid = grid
        self.nudge_limit = 2

    def move_up(self):
        for speed in range(self.speed, 0, -1):
            new_y = self.y - speed
            xs = [0]
            for inc in range(1, self.nudge_limit + 1):
                xs.append(inc)
                xs.append(-inc)
            for x in [self.x + e for e in xs]:
                if not self.hits_grid(x, new_y):
                    self.x = x
                    self.y = new_y
                    if self.y < 0:
                        self.y += self.screen_height
                    return

    def move_down(self):
        for speed in range(self.speed, 0, -1):
            new_y = self.y + speed
            xs = [0]
            for inc in range(1, self.nudge_limit + 1):
                xs.append(inc)
                xs.append(-inc)
            for x in [self.x + e for e in xs]:
                if not self.hits_grid(x, new_y):
                    self.x = x
                    self.y = new_y
                    if self.y >= self.screen_height:
                        self.y -= self.screen_height
                    return

    def move_left(self):
        for speed in range(self.speed, 0, -1):
            new_x = self.x - speed
            ys = [0]
            for inc in range(1, self.nudge_limit + 1):
                ys.append(inc)
                ys.append(-inc)
            for y in [self.y + e for e in ys]:
                if not self.hits_grid(new_x, y):
                    self.x = new_x
                    self.y = y
                    return 

    def move_right(self):
        for speed in range(self.speed, 0, -1):
            new_x = self.x + speed
            ys = [0]
            for inc in range(1, self.nudge_limit + 1):
                ys.append(inc)
                ys.append(-inc)
            for y in [self.y + e for e in ys]:
                if not self.hits_grid(new_x, y):
                    self.x = new_x
                    self.y = y
                    return 

    def hits_grid(self, x, y):
        offsets = [
            [x, y],
            [x + self.xs - 1, y],
            [x + self.xs - 1, y + self.ys - 1],
            [x, y + self.ys - 1]
        ]
        for p in offsets:
            if p[1] < 0:
                p[1] += self.screen_height
            if p[1] >= self.screen_height:
                p[1] -= self.screen_height
        index_pairs = set()
        for offset in offsets:
            x_index = math.floor((offset[0] / self.screen_width) * self.grid.w)
            y_index = math.floor((offset[1] / self.screen_height) * self.grid.h)
            index_pairs.add((x_index, y_index))
        for p in index_pairs:
            if self.grid.value(p[0], p[1]) == 'x':
                return True
        return False
