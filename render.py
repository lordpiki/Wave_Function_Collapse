import pygame
import sys
from grid import Grid
black_image = pygame.Surface((3, 3))
white_image = pygame.Surface((3, 3))
black_image.fill((0, 0, 0))
white_image.fill((255, 255, 255))
images = []


def render(grid_obj: Grid, scale: int = 50):
    pygame.init()
    grid = grid_obj.grid
    screen = pygame.display.set_mode((len(grid[0]) * scale, len(grid) * scale))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # the grid contains tiles, which contain images
        collapsed_cell = None
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                grid[y][x].checked = False
                if grid[y][x].collapsed:
                    collapsed_cell = grid[y][x]
                    screen.blit(pygame.transform.scale(grid_obj.get_tiles()[grid[y][x].options[0]].img, (scale, scale)), (x*scale, y*scale))
                else:
                    # draw black image
                    screen.blit(pygame.transform.scale(calculate_avg_color(grid[y][x].options, grid_obj.tiles), (scale, scale)), (x*scale, y*scale))
                    # display the entropy of the cell
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(grid[y][x].calculate_entropy()), True, (0, 255, 255))
                    # text = font.render(str(x+y*20), True, (0, 255, 255))
                    screen.blit(text, (x*scale, y*scale))
                    # draw the grid lines
                    pygame.draw.rect(screen, (255, 255, 255), (x*scale, y*scale, scale, scale), 1)

        pygame.display.update()
        # pygame.time.delay(100)
        # reduce the entropy of the grid
        if collapsed_cell is not None:
            grid_obj.reduce_entropy(collapsed_cell)
        grid_obj.wfc()

def calculate_avg_color(options, tiles) -> pygame.Surface:
    # create a 3x3 image
    img = pygame.Surface((3, 3))
    for y in range(3):
        for x in range(3):
            # get the color of the pixel
            color = (0, 0, 0)
            for tile_index in options:
                color = (color[0] + tiles[tile_index].img.get_at((x, y))[0], color[1] + tiles[tile_index].img.get_at((x, y))[1], color[2] + tiles[tile_index].img.get_at((x, y))[2])
            color = (color[0] // len(options), color[1] // len(options), color[2] // len(options))
            img.set_at((x, y), color)
    return img


def load_image(path):
    # Load the image
    img = pygame.image.load(path)
    
    # Ensure the image is 9x9
    # img = pygame.transform.scale(img, (9, 9))
    
    # Convert the image to a Surface and get pixel data
    img_surface = pygame.Surface((img.get_width(), img.get_width()))
    img_surface.blit(img, (0, 0))
    img_pixels = pygame.PixelArray(img_surface)

    # Iterate through every possible 3x3 grid
    for y in range(img.get_height()):
        for x in range(img.get_width()):
            # Create a new Surface for each 3x3 grid
            grid_surface = pygame.Surface((3, 3))

            # Fill the 3x3 grid with wrapped pixels
            for dy in range(3):
                for dx in range(3):
                    # Wrap around using modular arithmetic
                    wrapped_x = (x + dx) % img.get_width()
                    wrapped_y = (y + dy) % img.get_height()

                    # Get the color from the wrapped coordinates
                    color = img_pixels[wrapped_x, wrapped_y]

                    # Set the pixel in the new grid
                    grid_surface.set_at((dx, dy), color)

            # Append the 3x3 grid to the images list
            images.append(grid_surface)

    # Cleanup pixel array
    del img_pixels

    return images

def identical(imgA, imgB):
    for y in range(3):
        for x in range(3):
            if imgA.get_at((x, y)) != imgB.get_at((x, y)):
                return False
    return True