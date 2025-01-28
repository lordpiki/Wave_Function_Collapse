import pygame
import sys
from grid import Grid
black_image = pygame.Surface((3, 3))
white_image = pygame.Surface((3, 3))
black_image.fill((0, 0, 0))
white_image.fill((255, 255, 255))
images = []


def render(grid_obj: Grid, scale: int = 40):
    pygame.init()
    grid = grid_obj.grid
    screen = pygame.display.set_mode((len(grid[0]) * scale, len(grid) * scale))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # the grid contains tiles, which contain images
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x].collapsed:
                    screen.blit(pygame.transform.scale(grid_obj.get_tiles()[grid[y][x].options[0]].img, (scale, scale)), (x*scale, y*scale))
                else:
                    # draw black image
                    screen.blit(pygame.transform.scale(white_image, (scale, scale)), (x*scale, y*scale))
                # draw the grid lines
                pygame.draw.rect(screen, (0, 0, 0), (x*scale, y*scale, scale, scale), 1)
        pygame.display.update()
        # pygame.time.delay(1000)


def load_image(path):
    # Load the image
    img = pygame.image.load(path)
    
    # Ensure the image is 9x9
    # img = pygame.transform.scale(img, (9, 9))
    
    # Convert the image to a Surface and get pixel data
    img_surface = pygame.Surface((9, 9))
    img_surface.blit(img, (0, 0))
    img_pixels = pygame.PixelArray(img_surface)

    # Iterate through every possible 3x3 grid
    for y in range(9):
        for x in range(9):
            # Create a new Surface for each 3x3 grid
            grid_surface = pygame.Surface((3, 3))

            # Fill the 3x3 grid with wrapped pixels
            for dy in range(3):
                for dx in range(3):
                    # Wrap around using modular arithmetic
                    wrapped_x = (x + dx) % 9
                    wrapped_y = (y + dy) % 9

                    # Get the color from the wrapped coordinates
                    color = img_pixels[wrapped_x, wrapped_y]

                    # Set the pixel in the new grid
                    grid_surface.set_at((dx, dy), color)

            # Append the 3x3 grid to the images list
            images.append(grid_surface)

    # Cleanup pixel array
    del img_pixels

    return images
