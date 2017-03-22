import pygame, math
from player import Player
from aiplayer import AIPlayer
from grid import Grid


SCREEN_W, SCREEN_H = 640, 480


def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    font = pygame.font.SysFont('arialrounded', 12)

    clock = pygame.time.Clock()
    done = False

    grid_pixel_w, grid_pixel_h = 425, 425
    grid = Grid('level.txt', grid_pixel_w, grid_pixel_h)
    player = Player(grid, grid_pixel_w, grid_pixel_h)

    aiplayer = AIPlayer(grid, grid_pixel_w, grid_pixel_h)

    xscale = grid_pixel_w / grid.w
    yscale = grid_pixel_h / grid.h

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                aiplayer.set_goal_grid_pos(*player.get_grid_pos())

        aiplayer.update()

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]: player.move_up()
        if pressed[pygame.K_DOWN]: player.move_down()
        if pressed[pygame.K_LEFT]: player.move_left()
        if pressed[pygame.K_RIGHT]: player.move_right()

        # clear the screen
        screen.fill((0, 0, 0))

        x_offset = (SCREEN_W - grid_pixel_w) / 2
        y_offset = (SCREEN_H - grid_pixel_h) / 2

        # draw the maze
        grid.draw(screen, x_offset, y_offset)

        # determine which grid index the player is in

        offsets = [
            (player.x, player.y),
            (player.x + xscale * 0.99, player.y),
            (player.x + xscale * 0.99, player.y + yscale * 0.99),
            (player.x, player.y + yscale * 0.99)
        ]

        index_pairs = set()
        for offset in offsets:
            grid_x_index = math.floor((offset[0] / grid_pixel_w) * grid.w)
            grid_y_index = math.floor((offset[1] / grid_pixel_h) * grid.h)
            if grid_y_index >= grid.h:
                grid_y_index -= grid.h
            if grid_y_index < 0:
                grid_y_index += grid.h
            index_pairs.add((grid_x_index, grid_y_index))

        for p in index_pairs:
            pygame.draw.rect(screen, (16, 16, 16), pygame.Rect(p[0] * xscale + x_offset, p[1] * yscale + y_offset, xscale, yscale))

        # draw the "player"
        color = (0, 128, 255)
        pygame.draw.rect(screen, color, pygame.Rect(player.x + x_offset, player.y + y_offset, xscale, yscale))
        pygame.draw.rect(screen, color, pygame.Rect(player.x + x_offset, player.y + y_offset - (yscale * grid.h), xscale, yscale))

        color = (128, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(aiplayer.x + x_offset, aiplayer.y + y_offset, xscale, yscale))
        pygame.draw.rect(screen, color, pygame.Rect(aiplayer.x + x_offset, aiplayer.y + y_offset - (yscale * grid.h), xscale, yscale))

        # draw black rectangles on top and bottom of the grid to hide the player "warping"
        # beyond the edge of the screen
        pygame.draw.rect(screen, (0, 0, 0)
            , pygame.Rect(0, 0, SCREEN_W, y_offset))
        pygame.draw.rect(screen, (0, 0, 0)
            , pygame.Rect(0, y_offset + grid_pixel_h, SCREEN_W, SCREEN_H - (y_offset + grid_pixel_h)))

        text = '%d %d, %s' % (player.x, player.y, str(index_pairs))
        label = font.render(text, 1, (255, 255, 255))
        screen.blit(label, (5, 5))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
